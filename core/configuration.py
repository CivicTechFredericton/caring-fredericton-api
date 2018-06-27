# Standard imports
import os

# Third party imports
import yaml

# Local imports
from core import utils

settings = {}


def init_settings():
    """
    * Read the environment config
    * Merge environment variables in (overwriting environment config)
    """
    config_file = 'configs/%s.yaml' % os.environ['STAGE']

    if os.path.exists(config_file):
        with open(config_file) as f:
            utils.deep_merge(yaml.load(f), settings)
    else:
        print("File doesn't exist: %s" % config_file)

    # Deep merge any environment variables
    utils.deep_merge(os.environ, settings)


def get_setting(name):
    if name not in settings:
        raise Exception("Required setting '{}' was not specified".format(name))

    return settings[name]


def set_setting(name, value):
    settings[name] = value
