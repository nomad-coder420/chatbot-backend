import logging

LOG_LEVEL = "DEBUG"


def configure_logging():
    logging.basicConfig(level=LOG_LEVEL)


logger = logging.getLogger(__name__)
