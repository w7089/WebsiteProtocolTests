import time

import requests

from utils.constants import TestResult, TestStatus


def latency(website_domain, runs=1, wait_between_run=0):
    latencies = list()
    for _ in range(runs):
        res = requests.get(f"http://{website_domain}")
        if res.status_code == 200:
            latencies.append(res.elapsed.total_seconds())
        time.sleep(wait_between_run)
    if not latencies:
        return TestResult()
    lat = round(sum(latencies) / len(latencies), 6)
    return TestResult(status=TestStatus.SUCCESS, info=f'latency: {lat} seconds', val=lat)
