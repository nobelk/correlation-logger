import pytest
import unittest
import uuid
from src.prod_logger.logger import Logger


class LoggerTests(unittest.TestCase):

    def test_console_logger(self):
        logger = Logger('default logger')
        logger.debug('Debug log message', str(uuid.uuid4()))
        assert True
