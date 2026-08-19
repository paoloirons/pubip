import ipaddress
import os
from typing import Any

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

IPIFY_URL = os.getenv("IPIFY_URL", "https://api.ipify.org?format=json")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "5"))


def get_public_ip() -> str | None:
    """Return the public IP reported by ipify, or None if it cannot be resolved."""
    try:
        response = requests.get(IPIFY_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        value = response.json().get("ip", "")
        return str(ipaddress.ip_address(value))
    except (requests.RequestException, ValueError, TypeError):
        return None


def calculate_subnet(ip: str, subnet: str) -> dict[str, Any]:
    """Calculate subnet metadata without materializing every host address."""
    network = ipaddress.ip_network(f"{ip}/{subnet}", strict=False)

    if network.version == 4 and network.prefixlen <= 30:
        usable_hosts = max(network.num_addresses - 2, 0)
        first_host = network.network_address + 1
        last_host = network.broadcast_address - 1
    else:
        usable_hosts = network.num_addresses
        first_host = network.network_address
        last_host = network.broadcast_address

    return {
        "version": network.version,
        "cidr": str(network),
        "network": str(network.network_address),
        "broadcast": str(network.broadcast_address),
        "netmask": str(network.netmask),
        "prefixlen": network.prefixlen,
        "num_addresses": network.num_addresses,
        "usable_hosts": usable_hosts,
        "first_host": str(first_host),
        "last_host": str(last_host),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    public_ip = get_public_ip()
    subnet_info = None
    error = None

    if request.method == "POST":
        ip = request.form.get("ip", "").strip()
        subnet = request.form.get("subnet", "").strip()
        try:
            subnet_info = calculate_subnet(ip, subnet)
        except ValueError as exc:
            error = f"Indirizzo IP o subnet non validi: {exc}"

    return render_template(
        "index.html",
        public_ip=public_ip,
        subnet_info=subnet_info,
        error=error,
    )


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
