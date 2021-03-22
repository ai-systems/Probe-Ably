import unittest
from probe_ably.core.utils import GridModelFactory


class FactoryTest(unittest.TestCase):
    def test_create_models(self):
        thing = GridModelFactory.create_models('probe_ably.core.models.linear.LinearModel', num_models=2, param_args={'representation_size':768, 'n_classes':2})
        
        print(thing)

