import json

from utils import utils
from utils.utils import create_protocol_tests_mapping

# TODO configure logger by cmd arg
# TODO add color to logs
class WebsiteTester:
    def __init__(self):
        self.protocol_tests_mapping = create_protocol_tests_mapping()

    def run_website_tests(self, config):
        for website_domain, website_tests_conf in config.items():
            logger.info(f'starting checks for {website_domain}')
            for protocol, protocol_tests in website_tests_conf.items():
                logger.info(f'starting checks for {website_domain} {protocol} protocol')
                # TODO check if protocol package exists
                for test, test_conf in protocol_tests.items():
                    # TODO check if function exists
                    logger.info(f'starting {test} check for {website_domain} {protocol} protocol')
                    test_method = self.protocol_tests_mapping[protocol][test]
                    test_passed = test_method(website_domain, **test_conf)
                    if test_passed:
                        logger.error(f'SUCCESSFUL {protocol} {test} check for {website_domain}')
                    else:
                        logger.error(f'FAILED {protocol} {test} check for {website_domain}')
                    logger.info(f'finishing {test} check for {website_domain} {protocol} protocol')
                logger.info(f'finishing checks for {website_domain} {protocol} protocol')
            logger.info(f'finishing checks for {website_domain}')

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

