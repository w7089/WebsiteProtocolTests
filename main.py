import json
from csv import DictWriter
from pathlib import Path

from utils import utils
from utils.constants import TestStatus, FIELDS, OUT_FILE_NAME
from utils.utils import create_protocol_tests_mapping

# TODO configure logger level by cmd arg
# TODO support custom args for each check
# TODO don't allow single website exceptions crash entire test


class WebsiteTester:
    def __init__(self):
        self.protocol_tests_mapping = create_protocol_tests_mapping()

    def run_website_tests(self, config, output_file=OUT_FILE_NAME):
        with open(output_file,'a') as out:
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
                        test_res = test_method(website_domain, **test_conf)
                        res_row = dict()
                        res_row['domain_name'] = website_domain
                        res_row['protocol'] = protocol
                        if test_res.status == TestStatus.SUCCESS:
                            logger.info(f'SUCCESSFUL {protocol} {test} check for {website_domain}, more details: {test_res.info}')
                            res_row['test_result'] = 'success'
                            res_row[test] = test_res.val
                        else:
                            logger.error(f'FAILED {protocol} {test} check for {website_domain}')
                            res_row['test_result'] = 'failure'
                        out_writer.writerow(res_row)
                        logger.debug(f'finishing {test} check for {website_domain} {protocol} protocol')
                    logger.debug(f'finishing checks for {website_domain} {protocol} protocol')
                logger.debug(f'finishing checks for {website_domain}')

    def read_config(self, config_json='config.json'):
        with open(config_json) as conf_file:
            contents = conf_file.read()
            config = json.loads(contents)
        return config


if __name__ == '__main__':
    global logger
    logger = utils.init_logger(WebsiteTester.__name__)
    tester = WebsiteTester()
    config = tester.read_config()
    tester.run_website_tests(config)

