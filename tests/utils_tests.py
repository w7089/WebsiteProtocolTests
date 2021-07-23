import unittest
from pathlib import Path

import utils.utils
from utils.constants import WEBSITE_TESTS


class UtilsTests(unittest.TestCase):
    def test_create_protocol_tests_mapping(self):
        module_path = Path(f'{WEBSITE_TESTS}')
        mapping = utils.utils.create_protocol_tests_mapping(module_path)
        self.assertIsNotNone(mapping)


if __name__ == '__main__':
    unittest.main()
