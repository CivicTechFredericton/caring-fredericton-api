import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logging.getLogger(__name__).setLevel(logging.INFO)


def init_app():
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    logging.basicConfig(format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s',
                        level=os.getenv('LOG_LEVEL', 'INFO'))

