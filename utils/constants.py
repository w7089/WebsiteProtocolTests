from dataclasses import dataclass
from enum import Enum

WEBSITE_TESTS = 'website_tests'


class TestStatus(Enum):
    SUCCESS = 0
    FAILURE = 1


@dataclass
class TestResult:
    """Keeps track of website check result"""
    status: TestStatus = TestStatus.FAILURE
    info: str = ""
