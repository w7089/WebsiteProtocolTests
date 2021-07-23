import json

from utils import utils
from utils.constants import TestStatus
from utils.utils import create_protocol_tests_mapping

# TODO configure logger level by cmd arg
# TODO support custom args for each check
# TODO don't allow single website exceptions crash entire test
class WebsiteTester:
    def __init__(self):
        self.protocol_tests_mapping = create_protocol_tests_mapping()

    def run_website_tests(self, config):
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
                    if test_res.status == TestStatus.SUCCESS:
                        logger.info(f'SUCCESSFUL {protocol} {test} check for {website_domain}, more details: {test_res.info}')
                    else:
                        logger.error(f'FAILED {protocol} {test} check for {website_domain}')
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

