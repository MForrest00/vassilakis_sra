import unittest
from vassilakis_sra import Sinusoid, SRAModel


class TestSRAModel(unittest.TestCase):

    def setUp(self):
        self.sra1 = SRAModel([(444.0, 1.0), (466.1638, 1.0)])

    def test_construction(self):
        self.assertTrue(all(isinstance(s, Sinusoid) for s in self.sra1.sinusoids))

    def test_sinusoid_removal(self):
        sra1 = SRAModel([(444.0, 1.0), (466.1638, 1.0)])
        sra1.remove_sinusoid((440.0, 1.0))
        self.assertEqual(sra1.roughness, 0.0)
