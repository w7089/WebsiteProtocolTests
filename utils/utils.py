import logging


def init_logger(cls, log_file_name='run.log', file_log_level=logging.INFO, screen_log_level=logging.INFO):
    # TODO handle log format
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
    return logger
