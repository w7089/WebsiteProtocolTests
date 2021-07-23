import unittest

from utils.constants import TestStatus
from website_tests.dns.tests import resolve
from website_tests.http.tests import latency


class DnsChecksTests(unittest.TestCase):
    def test_dns(self):
        res = resolve('google.com')
        self.assertEqual(TestStatus.SUCCESS, res.status)
        res = resolve('goosdfsfgle.com')
        self.assertEqual(TestStatus.FAILURE, res.status)


class HttpChecksTests(unittest.TestCase):
    def test_http_latency(self):
        res = latency('google.com')
        self.assertEqual(TestStatus.SUCCESS, res.status)
        res = resolve('goosdfsfgle.com')
        self.assertEqual(TestStatus.FAILURE, res.status)


class HttpsChecksTests(unittest.TestCase):
    def test_http_latency(self):
        res = latency('google.com')
        self.assertEqual(TestStatus.SUCCESS, res.status)
        res = resolve('goosdfsfgle.com')
        self.assertEqual(TestStatus.FAILURE, res.status)


if __name__ == '__main__':
    unittest.main()

