from __future__ import print_function

import argparse
import logging
import os

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import common

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "Updates Oauth 2.0 Credentiasl for GMail"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))


class GmailAuth():
    """
    Updates Oauth 2.0 Credentiasl for GMail
    """

    def __init__(self, config, oauth2_flags, logger):
        """
        Constructor
        :param config: Configuration dict
        :param oauth2_flags: Result of parser.parse_args(argv) using
        :param logger: Python logger

        """

        # Suppress cache warnings from gogogle api lib
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

        # Crete paths to client secret and credentials storage file
        self._client_secret_file = os.path.join(config['credentials_dir'],
                                                config['client_secret_file_name'])
        self._credentials_file = os.path.join(config['credentials_dir'],
                                              config['credentials_file_name'])
        self._logger = logger
        self._config = config
        self._oauth2_flags = oauth2_flags

    def update_credentials(self):
        """Gets valid user credentials from Gmail using Oauth 2.0

        Returns:
            Credentials, the obtained credential.
        """

        if not os.path.exists(self._config['credentials_dir']):
            os.makedirs(self._config['credentials_dir'])

        store = Storage(self._credentials_file)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self._client_secret_file,
                                                  self._config['oauth2_scopes'])
            flow.user_agent = self._config['application_name']
            credentials = tools.run_flow(flow, store, self._oauth2_flags)
            self._logger.info('Storing credentials to ' + self._credentials_file)
        else:
            self._logger.info("Credentials exist.")
        return credentials


if __name__ == '__main__':
    # Setup argument parser (we need to use Argparse for Gmail's Oauth 2.0 lib
    default_config_file = "%s/../config/config.yml" % __abs_dirpath__
    parser = argparse.ArgumentParser(parents=[tools.argparser])

    # Add our single option
    parser.add_argument('-c', '--config-file', help='Config file location', required=False,
                        default=default_config_file)
    parser_namespace = parser.parse_args()
    arguments = vars(parser_namespace)

    # Load config
    config = common.load_config_file(arguments['config_file'])

    # Load logging config
    common.setup_logging_config("%s/../config/" % __abs_dirpath__)

    # Get logger
    logger = common.get_logger("gmail_auth")

    logger.info("Fetching Gmail Credentials...")
    credentials_dir = os.path.join(__abs_dirpath__, '../', config['credentials_dir_name'])

    # Enhance configuration
    config['credentials_dir'] = credentials_dir

    gmail_auth = GmailAuth(config=config, logger=logger, oauth2_flags=parser_namespace)
    gmail_auth.update_credentials()
