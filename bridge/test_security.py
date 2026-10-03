import unittest

from security import authorized, validate_binding


class BridgeSecurityTests(unittest.TestCase):
    def test_loopback_without_key_is_allowed(self):
        validate_binding("127.0.0.1", "")
        validate_binding("localhost", "")

    def test_non_loopback_requires_api_key(self):
        with self.assertRaisesRegex(ValueError, "BRIDGE_API_KEY is required"):
            validate_binding("0.0.0.0", "")

    def test_non_loopback_with_api_key_is_allowed(self):
        validate_binding("0.0.0.0", "example-key")

    def test_bearer_key_is_checked_exactly(self):
        self.assertTrue(authorized("Bearer example-key", "example-key"))
        self.assertFalse(authorized("example-key", "example-key"))
        self.assertFalse(authorized("Bearer example-key-extra", "example-key"))


if __name__ == "__main__":
    unittest.main()
