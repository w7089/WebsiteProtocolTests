import unittest

from website_tests.dns.tests import resolve


class DnsChecksTests(unittest.TestCase):
    def test_dns(self):
        self.assertTrue(resolve('google.com'))
        self.assertFalse(resolve('goosdfsfgle.com'))


if __name__ == '__main__':
    unittest.main()
