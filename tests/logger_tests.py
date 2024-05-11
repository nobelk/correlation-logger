import logging

import pytest
import unittest
import uuid
from src.prod_logger.logger import Logger, LogSink


class LoggerTests(unittest.TestCase):

    def test_console_logging(self):
        logger = Logger(name='default logger', log_level=logging.DEBUG)
        logger.debug('Debug log message', str(uuid.uuid4()))
        assert True

    def test_file_logging(self):
        logger = Logger(name='default logger', sink=LogSink.LOCAL_FILE, log_level=logging.DEBUG,
                        log_file_name='test_log')
        logger.debug('Debug log message', str(uuid.uuid4()))
