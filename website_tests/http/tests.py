import requests

from utils.constants import TestResult, TestStatus


def latency(website_domain):
    res = requests.get(f"http://{website_domain}")
    if res.status_code == 200:
        lat = res.elapsed.total_seconds()
        return TestResult(status=TestStatus.SUCCESS, info=f'latency: {lat} seconds', val=lat)
    else:
        return TestResult()