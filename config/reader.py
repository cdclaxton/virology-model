import json
import logging
import os
from json import JSONDecodeError

from logger import logger
from jsonschema import validate, ValidationError

logger.initialise_logger("config-reader", log_level=logging.INFO)
module_logger = logging.getLogger('config-readere')


def load_schema(filepath="./config/config.schema"):
    """
    Load the schema.

    :param filepath: Location of the schema file.
    :return: Schema.
    """

    # Preconditions
    assert type(filepath) == str

    # Read the schema
    return read_json_config(filepath)


def read_json_config(path):
    """
    Read the JSON-formatted config file.

    :param path: Path to the JSON config.
    :return: Dict containing the config or None if it is invalid.
    """

    # Preconditions
    assert type(path) == str

    # Check the path exists
    if not os.path.exists(path):
        module_logger.error("Path does not exist: %s" % path)
        return None

    # Try to read the config
    try:
        with open(path, 'r') as fp:
            config = json.load(fp)
    except JSONDecodeError:
        module_logger.error("Unable to parse file: %s" % path)
        config = {}

    # Postconditions
    assert type(config) == dict

    # Return the config
    return config


def validate_config(config):
    """
    Validate the config.

    :param config: Dictionary representing the config.
    :return: True if the config passes validation, otherwise False.
    """

    # Preconditions
    assert type(config) == dict

    # Load the schema
    schema = load_schema()

    # Perform validation
    correctly_validated = True
    try:
        validate(instance=config, schema=schema)
    except ValidationError as e:
        module_logger.error("Config validation error: %s" % str(e.message))
        correctly_validated = False

    return correctly_validated
