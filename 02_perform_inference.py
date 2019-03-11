import logging

from config.reader import read_json_config, validate_config
from logger import logger

# Initialise the module logger
logger.initialise_logger("perform-inference", log_level=logging.INFO)
module_logger = logging.getLogger('perform-inference')


def run_inference(config_path):
    """
    Perform inference.

    :param config_path: Location of the JSON config path.
    :return:
    """

    # Preconditions
    assert type(config_path) == str

    # Read the JSON config
    module_logger.info("Reading config from: %s" % config_path)
    config = read_json_config(config_path)

    # Check the config is valid
    validates = validate_config(config)
    if not validates:
        module_logger.error("Config is invalid")
        exit(-1)


if __name__ == '__main__':

    # Location of the config
    config_path = "./data/simple/config.json"

    # Run the inference engine
    run_inference(config_path)
