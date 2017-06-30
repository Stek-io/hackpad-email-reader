import json
import logging
import logging.config
import os
import yaml

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "Azure Backups Common Python Lib"

__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))

# Holds the logging_config
logging_config = None


def load_config(config_files_csv):
    """
    Loads configuration from multiple files provided via a comma separated set of files.
    The order of loading is preserved: the latter files will replace properties of earlier files.

    :param config_files_csv: A comma separated list of config files
    :return: A dictionary with the loaded configuration
    """

    # Initialize the config file
    config = {}

    # Get a list of files
    config_files = [config_file.strip() for config_file in config_files_csv.split(',')]

    # Update the config dictionary
    for config_file in config_files:
        config = merge_dicts(config, load_config_file(config_file))

    return config


def setup_logging_config(config_dir):
    """
    Load config given an environment.
    :param config_dir: Path to configuration directory
    :return: The configuration object
    """
    global logging_config

    config_file_csv = "{0}/logging.yml".format(config_dir)

    # Load config
    logging_config = load_config(config_file_csv)


def load_config_file(config_file):
    """
    Loads a config file formatted either in yaml or json

    :param config_file: The path to the config file
    :return: The configuration dictionary
    """

    # Initialize the return object
    config = None

    # Extract the file extension
    filename, extension = os.path.splitext(config_file)

    # Pick the right deserializer
    try:
        if not os.path.isfile(config_file):
            raise IOError("%s is not a file." % config_file)

        deserializer = {
            ".yaml": yaml,
            ".yml": yaml,
            ".json": json
        }[extension]

        # Deserialize the config
        config = deserializer.load(open(config_file))

    except KeyError:
        # TODO: use a logger here
        print("Invalid configuration file type: %s" % extension)

    return config


def get_logger(module_name, default_level=logging.DEBUG):
    """
    Retrieves a logger from the logging config if one exists for the given module; otherwise, it creates a basic  one.

    :param module_name:
    :param default_level: The default logging level
    :return: a logger object
    """

    # Try using the config first
    if logging_config:

        logging.config.dictConfig(logging_config)
        logger = logging.getLogger(module_name)
    else:

        # Create a custom logger
        logger = logging.getLogger(module_name)
        logger.setLevel(default_level)

        ch = logging.StreamHandler()
        ch.setLevel(default_level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add formatter to ch
        ch.setFormatter(formatter)

        # Add a logger
        logger.addHandler(ch)

    return logger


def merge_dicts(origin, patch):
    """
    Merge two dictionaries, w/o overwriting missing keys

    :param origin: The origin dictionary
    :param patch: The dictionary containing the diffs
    :return: The result of the merge: a new dictionary
    """

    if patch:
        for key in patch:
            if key in origin and isinstance(origin[key], dict) and isinstance(patch[key], dict):
                merge_dicts(origin[key], patch[key])
            else:
                origin[key] = patch[key]
    return origin


class Struct:
    """
    Class used as a convertor between objects and dictionaries
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)


def dict_to_object(dict):
    """
    Convert a dictionary to object
    :param dict: The dictionary to convert
    :return: the converted object
    """
    return Struct(**dict)
