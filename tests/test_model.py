import unittest
from vassilakis_sra import Sinusoid, SRAModel


class TestSRAModel(unittest.TestCase):

    def setUp(self):
        self.sra1 = SRAModel([(440.0, 1.0)])
        self.sra2 = SRAModel([(440.0, 1.0), (466.1638, 1.0)])
        self.sra3 = SRAModel([(440.0, 2.0), (466.1638, 1.0)])
        self.sra4 = SRAModel([(440.0, 2.0), (466.1638, 1.0), (493.8833, 1.0)])

    def test_construction(self):
        self.assertTrue(all(isinstance(s, Sinusoid) for s in self.sra4.sinusoids))

    def test_sinusoid_removal(self):
        sra = SRAModel([(440.0, 1.0), (466.1638, 1.0)])
        sra.remove_sinusoid((466.1638, 1.0))
        self.assertEqual(sra, self.sra1)

    def test_sinusoid_removal_by_frequency(self):
        sra = SRAModel([(440.0, 1.0), (466.1638, 1.0)])
        sra.remove_sinusoid_by_frequency(466.1638)
        self.assertEqual(sra, self.sra1)

    def test_sinusoid_partial_removal(self):
        sra = SRAModel([(440.0, 1.0), (466.1638, 2.0)])
        sra.remove_sinusoid((466.1638, 1.0))
        self.assertEqual(sra, self.sra2)

    def test_new_sinusoid_addition(self):
        sra = SRAModel([(440.0, 1.0)])
        sra.add_sinusoid((466.1638, 1.0))
        self.assertEqual(sra, self.sra2)

    def test_existing_sinusoid_addition(self):
        sra = SRAModel([(440.0, 1.0), (466.1638, 1.0)])
        sra.add_sinusoid((440.0, 1.0))
        self.assertEqual(sra, self.sra3)
