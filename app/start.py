#!/usr/bin/env python3

import os

import click

import common
from gmail_reader import GmailReader
from hackpad_mail_processor import HackpadMailProcessor
from job_queuer import RedisJobQueuer

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "Hackpad Migration Email Importer"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))
__default_config_file__ = "%s/../config/config.yml" % __abs_dirpath__

# If modifying these scopes, delete your previously saved credentials
APPLICATION_NAME = 'Hackpad Gmail Reader'
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CREDENTIALS_DIR = os.path.join(__abs_dirpath__, '.credentials')
CLIENT_SECRET_FILE = os.path.join(CREDENTIALS_DIR, 'client_secret.json')
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, 'hackpad-gmail-reader.json')


@click.command()
@click.option('--config-file', required=False, default=__default_config_file__,
              help='Path to config file')
def fetch_email(config_file):
    """
    Start Backup Service
    """
    # Load config
    config = common.load_config_file(config_file)

    # Load logging config
    common.setup_logging_config("%s/../config/" % __abs_dirpath__)

    # Get logger
    logger = common.get_logger("app")

    logger.info("Starting mail parsing...")
    credentials_dir = os.path.join(__abs_dirpath__, '../.credentials')

    # Enhance configuration
    config['credentials_dir'] = credentials_dir

    # Instantiate services
    mail_reader = GmailReader(config=config, logger=logger)
    job_queuer = RedisJobQueuer(config=config, logger=logger)

    hackpad_processor = HackpadMailProcessor(config=config, mail_reader=mail_reader,
                                             job_queuer=job_queuer, logger=logger)
    hackpad_processor.fetch_and_process_emails()


if __name__ == '__main__':
    app = fetch_email()
