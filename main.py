import argparse
import json
import logging
from csv import DictWriter, DictReader
from pathlib import Path

from utils import utils
from utils.constants import TestStatus, FIELDS, OUT_FILE_NAME, TestResult
from utils.utils import create_protocol_tests_mapping


# TODO add ts for each run to results store
# TODO split main function


class WebsiteTester:
    def __init__(self):
        self.protocol_tests_mapping = create_protocol_tests_mapping()

    def run_website_tests(self, config, previous_runs, output_file=OUT_FILE_NAME):
        with open(output_file, 'a') as out:
            out_writer = DictWriter(out, fieldnames=FIELDS, dialect='excel-tab')
            size = Path(OUT_FILE_NAME).stat().st_size
            if size == 0:
                out_writer.writeheader()
            for website_domain, website_tests_conf in config.items():
                logger.debug(f'starting checks for {website_domain}')
                for protocol, protocol_tests in website_tests_conf.items():
                    logger.debug(f'starting checks for {website_domain} {protocol} protocol')
                    if protocol not in self.protocol_tests_mapping:
                        logger.warning(f"{protocol} protocol tests don't exist")
                        continue
                    for test, test_conf in protocol_tests.items():
                        if test not in self.protocol_tests_mapping[protocol]:
                            logger.warning(f"test {test} doesn't exist for protocol {protocol}")
                            continue
                        logger.debug(f'starting {test} check for {website_domain} {protocol} protocol')
                        test_method = self.protocol_tests_mapping[protocol][test]
                        test_args = test_conf['args'] if 'args' in test_conf else {}  # support custom test args (add them to config file)
                        # running website check
                        try:
                            test_res = test_method(website_domain, **test_args)
                        except Exception as ex:
                            # don't allow single website exceptions crash entire script
                            logger.error(f'exception happened while running {protocol} {test} check for {website_domain}')
                            logger.exception(ex)
                            test_res = TestResult()  # fail the test
                        res_row = dict()
                        res_row['domain_name'] = website_domain
                        res_row['protocol'] = protocol
                        if test_res.status == TestStatus.SUCCESS:
                            logger.info(
                                f'SUCCESSFUL {protocol} {test} check for {website_domain}, more details: {test_res.info}')
                            res_row['test_result'] = 'success'
                            res_row[test] = test_res.val
                            try:
                                previous_run = previous_runs[website_domain][protocol][test]
                            except KeyError:
                                previous_run = None
                            if previous_run is not None and 'threshold' in config[website_domain][protocol][test]:
                                website_protocol_test_threshold = config[website_domain][protocol][test]['threshold']
                                logger.debug(f'{protocol} {test} check for {website_domain} current run result: {test_res.val}')
                                logger.debug(f'{protocol} {test} check for {website_domain} previous run result: {previous_run}')
                                if test_res.val - previous_run > website_protocol_test_threshold:
                                    logger.warning(
                                        f'{protocol} {test} check for {website_domain} exceeds previous run by more than configured threshold of {website_protocol_test_threshold} seconds')
                            else:
                                if website_domain not in previous_runs:
                                    previous_runs[website_domain] = utils.rec_dd()
                                elif protocol not in previous_runs[website_domain]:
                                    previous_runs[website_domain][protocol] = utils.rec_dd()
                                elif test not in previous_runs[website_domain][protocol]:
                                    previous_runs[website_domain][protocol][test] = utils.rec_dd()

                            previous_runs[website_domain][protocol][test] = test_res.val

                        else:
                            logger.error(f'FAILED {protocol} {test} check for {website_domain}')
                            res_row['test_result'] = 'failure'
                        out_writer.writerow(res_row)
                        logger.debug(f'finishing {test} check for {website_domain} {protocol} protocol')
                    logger.debug(f'finishing checks for {website_domain} {protocol} protocol')
                logger.debug(f'finishing checks for {website_domain}')
        return previous_runs

    def read_config(self, config_json='config.json'):
        with open(config_json) as conf_file:
            contents = conf_file.read()
            config = json.loads(contents)
        return config


def keep_max_lines_in_out_file(output_file=OUT_FILE_NAME, max_lines=50):
    with open(output_file) as out:
        out_reader = DictReader(out, fieldnames=FIELDS, dialect='excel-tab')
        rows = [r for r in out_reader]
    if len(rows) < max_lines:
        return
    with open(output_file, 'w') as out:
        out_writer = DictWriter(out, fieldnames=FIELDS, dialect='excel-tab')
        out_writer.writeheader()
        out_writer.writerows(rows[-max_lines:])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs different protocol tests on websites according to configuration')
    parser.add_argument('--verbose', action='store_true', help='dispays debug log messages')
    args = parser.parse_args()
    if args.verbose:
        logger = utils.init_logger(WebsiteTester.__name__, logging_level=logging.DEBUG)
    else:
        logger = utils.init_logger(WebsiteTester.__name__)
    tester = WebsiteTester()
    config = tester.read_config()
    # TODO think about relatives paths to module
    previous_runs = utils.get_previous_runs()
    latest_runs = tester.run_website_tests(config, previous_runs)
    utils.save_latest_runs(latest_runs)
    keep_max_lines_in_out_file()  # avoid disk explosion, keep only max lines in output file
