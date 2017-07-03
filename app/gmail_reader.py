from __future__ import print_function

import logging
import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# Suppress cache warnings from gogogle api lib
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "Gmail Reader"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class GmailReader():
    """
    Reads email from Gmail
    """

    def __init__(self, config, logger):
        """
        Constructor
        :param config: Configuration dict
        :param logger: Python logger
        """

        # Suppress cache warnings from gogogle api lib
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

        self._logger = logger
        self._config = config
        self._credentials = self._get_credentials()

        # Bootstrap the Gmail client service
        http = self._credentials.authorize(httplib2.Http())
        self._service = discovery.build('gmail', 'v1', http=http)

    def _get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        if not os.path.exists(self._config['credentials_dir']):
            os.makedirs(self._config['credentials_dir'])

        credential_path = self._config['credentials_file']

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self._config['client_secret_file'],
                                                  self._config['oauth2_scopes'])
            flow.user_agent = self._config['application_name']
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            self._logger.info('Storing credentials to ' + credential_path)
        return credentials

    def fetch_mails(self, q='', max_results=10):
        """
        Fetch new Emails mathching the given query
        """

        # Fetch mail from Gmail
        results = self._service.users().messages().list(userId='me', q=q,
                                                        maxResults=max_results).execute()
        # Load messages
        messages = results.get('messages', [])

        # Fetch each mail separately
        mail_data = [self.fetch_mail_by_id(mail_id=m['id']) for m in messages]

        self._logger.info('Located %s email(s) matching %s' % (len(mail_data), q))

        return mail_data

    def fetch_mail_by_id(self, mail_id):
        """
        Fetch a single email bu mail id

        :param mail_id: The Id of the email
        :return: The message payload
        """

        results = self._service.users().messages().get(userId='me', id=mail_id).execute()
        payload = results.get('payload', {})
        payload['from'] = self.locate_sender(payload)
        payload['mail_id'] = mail_id
        return payload

    def mark_email_as_read(self, mail_id):
        """
        Marks a given email as read

        :param mail_id: The Id of the email
        """

        # Removing label "Unread"
        modify_payload = {
            "removeLabelIds": ["UNREAD"]
        }

        self._logger.info("Marking email #%s as read" % mail_id)
        self._service.users().messages().modify(userId='me', id=mail_id,
                                                body=modify_payload).execute()

    def locate_sender(self, email):
        """
        Locate the From header
        :param email: The body of the email
        :return: The sender email
        """
        for header in email.get('headers', []):
            if header.get('name', None) == 'From':
                return header.get('value')
