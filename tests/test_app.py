import unittest

from app import calculate_subnet


class CalculateSubnetTests(unittest.TestCase):
    def test_ipv4_24(self):
        result = calculate_subnet("192.168.1.42", "24")
        self.assertEqual(result["cidr"], "192.168.1.0/24")
        self.assertEqual(result["broadcast"], "192.168.1.255")
        self.assertEqual(result["usable_hosts"], 254)
        self.assertEqual(result["first_host"], "192.168.1.1")
        self.assertEqual(result["last_host"], "192.168.1.254")

    def test_ipv4_32(self):
        result = calculate_subnet("203.0.113.7", "32")
        self.assertEqual(result["usable_hosts"], 1)
        self.assertEqual(result["first_host"], "203.0.113.7")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            calculate_subnet("not-an-ip", "24")


if __name__ == "__main__":
    unittest.main()
