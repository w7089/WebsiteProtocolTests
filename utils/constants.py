from dataclasses import dataclass
from enum import Enum

WEBSITE_TESTS = 'website_tests'
OUT_FILE_NAME = 'out.tsv'

class TestStatus(Enum):
    SUCCESS = 0
    FAILURE = 1


@dataclass
class TestResult:
    """Keeps track of website check result"""
    status: TestStatus = TestStatus.FAILURE
    info: str = ""
    val: str = ""

FIELDS = ['domain_name', 'protocol', 'test_result', 'resolve', 'latency', 'bandwidth']
