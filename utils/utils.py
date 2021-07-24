import importlib
import inspect
import json
import logging
import os
from collections import defaultdict
from pathlib import Path

import coloredlogs

from utils.constants import WEBSITE_TESTS, PREVIOUS_RUNS_JSON


def init_logger(cls, log_file_name='run.log', logging_level=logging.INFO):
    log = logging.getLogger(cls)
    log.setLevel(logging_level)
    formatter = logging.Formatter('%(message)s')

    fh = logging.FileHandler(log_file_name, mode='a', encoding='utf-8')
    fh.setLevel(logging_level)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    ch.setFormatter(formatter)
    log.addHandler(ch)
    logger = logging.getLogger(cls)
    coloredlogs.install(level=logging_level, logger=logger, fmt='%(asctime)s %(levelname)s %(message)s')
    return logger


def create_protocol_tests_mapping(websites_tests_package_path=Path(WEBSITE_TESTS)):
    mapping = dict()
    for prot_package_name in filter(lambda name: not name.startswith('__'), os.listdir(websites_tests_package_path)):
        module = importlib.import_module(f'{WEBSITE_TESTS}.{prot_package_name}.tests')
        functions = inspect.getmembers(module, inspect.isfunction)
        mapping[prot_package_name] = dict(functions)
    return mapping


def rec_dd():
    return defaultdict(rec_dd)


def get_previous_runs(runs_file_name=PREVIOUS_RUNS_JSON):
    if Path(runs_file_name).exists():
        with open(runs_file_name) as runs_file:
            previous_runs = json.load(runs_file)
            return previous_runs
    return rec_dd()


def save_latest_runs(latest_runs, latest_runs_file_name=PREVIOUS_RUNS_JSON):
    with open(latest_runs_file_name, 'w') as latest_runs_out_f:
        json.dump(latest_runs, latest_runs_out_f, indent=4, sort_keys=True)
