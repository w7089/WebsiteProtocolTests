import socket

from utils.constants import TestResult, TestStatus


def resolve(domain_name):
    try:
        ip = socket.gethostbyname(domain_name)
        return TestResult(status=TestStatus.SUCCESS, info=f"resolved ip {ip}", val=ip)
    except socket.gaierror:
        return TestResult()
