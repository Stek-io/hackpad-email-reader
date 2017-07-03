from __future__ import print_function

import json
import logging
import os

import redis
from oauth2client import tools

# Suppress cache warnings from gogogle api lib
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "Hackpad Import Job Queuer"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class RedisJobQueuer():
    """
    Queues Jobs
    """

    def __init__(self, config, logger):
        """
        Constructor
        :param config: Configuration dict
        :param logger: Python logger
        """

        self._logger = logger
        self._config = config

        self._redis_client = redis.Redis().from_url(url=self._config['redis']['url'])

    def queue_job(self, job):
        """

        :param job:
        :return:
        """
        job_str = json.dumps(job)

        self._logger.info(
            "Queueing job %s to queue  %s" % (job_str, self._config['redis']['queue_name']))
        self._redis_client.lpush(self._config['redis']['queue_name'], job_str)

    def queue_error(self, error):
        """

        :param error:
        :return:
        """
        job_str = json.dumps(error)

        self._logger.warning(
            "Queueing error %s to queue  %s" % (
                job_str, self._config['redis']['error_queue_name']))
        self._redis_client.lpush(self._config['redis']['error_queue_name'], job_str)
