import json

from utils import utils


class WebsiteTester:

    def run_website_tests(self, config):
        for website_domain, website_tests_conf in config.items():
            logger.info(f'starting checks for {website_domain}')
            for protocol, protocol_tests in website_tests_conf.items():
                logger.info(f'starting checks for {website_domain} {protocol} protocol')
                for test, test_conf in protocol_tests.items():
                    logger.info(f'starting {test} check for {website_domain} {protocol} protocol')
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

