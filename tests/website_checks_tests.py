import unittest

from utils.constants import TestStatus
from website_tests.dns.tests import resolve


class DnsChecksTests(unittest.TestCase):
    def test_dns(self):
        res = resolve('google.com')
        self.assertEquals(TestStatus.SUCCESS, res.status)
        res = resolve('goosdfsfgle.com')
        self.assertEquals(TestStatus.FAILURE, res.status)


if __name__ == '__main__':
    unittest.main()
