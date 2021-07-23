import importlib
import inspect
import logging
import os
from pathlib import Path

import coloredlogs

from utils.constants import WEBSITE_TESTS


def init_logger(cls, log_file_name='run.log', file_log_level=logging.DEBUG, screen_log_level=logging.DEBUG):
    log = logging.getLogger(cls)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')

    fh = logging.FileHandler(log_file_name, mode='w', encoding='utf-8')
    fh.setLevel(file_log_level)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(screen_log_level)
    ch.setFormatter(formatter)
    log.addHandler(ch)
    logger = logging.getLogger(cls)
    coloredlogs.install(level='DEBUG', logger=logger, fmt='%(asctime)s %(levelname)s %(message)s')
    return logger


def create_protocol_tests_mapping(websites_tests_package_path=Path(WEBSITE_TESTS)):
    mapping = dict()
    for prot_package_name in filter(lambda name: not name.startswith('__'), os.listdir(websites_tests_package_path)):
        module = importlib.import_module(f'{WEBSITE_TESTS}.{prot_package_name}.tests')
        functions = inspect.getmembers(module, inspect.isfunction)
        mapping[prot_package_name] = dict(functions)
    return mapping