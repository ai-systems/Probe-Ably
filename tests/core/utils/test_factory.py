import unittest
from loguru import logger
from probe_ably.core.utils import GridModelFactory


class FactoryTest(unittest.TestCase):
    def test_factory(self):
        # Add test he