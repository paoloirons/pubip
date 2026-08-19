# pubip

Piccola web app Flask che mostra l'IP pubblico e calcola i dati principali di una subnet IPv4/IPv6.

## Avvio con Docker Compose

```bash
docker compose up --build -d
```

Apri `http://localhost:5000`. L'endpoint `GET /healthz` restituisce lo stato del servizio.

## Avvio locale

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:5000 app:app
```

## Note

- La richiesta a ipify ha timeout e gestione errori: se il servizio esterno non risponde, l'app continua a funzionare.
- Il calcolo subnet non materializza l'intera lista degli host, quindi non esaurisce memoria su reti grandi.
- Il container gira come utente non-root.
