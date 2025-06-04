import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s'
    )

def get_logger(name):
    setup_logging()
    return logging.getLogger(name)