import unittest
from vassilakis_sra import Sinusoid


class TestSinusoid(unittest.TestCase):

    def test_construction(self):
        with self.assertRaises(TypeError):
            Sinusoid('string', 1.0)
        with self.assertRaises(ValueError):
            Sinusoid(0.0, -1.0)

    def test_comparison(self):
        self.assertEqual(Sinusoid(440.0, 1.0), Sinusoid(440.0, 1.0))
        self.assertNotEqual(Sinusoid(440.0, 1.0), Sinusoid(466.1638, 1.0))
        self.assertLess(Sinusoid(440.0, 2.0), Sinusoid(466.1638, 1.0))
        self.assertLessEqual(Sinusoid(440.0, 1.0), Sinusoid(440.0, 1.0))
        self.assertGreater(Sinusoid(466.1638, 1.0), Sinusoid(44.0, 2.0))
        self.assertGreaterEqual(Sinusoid(440.0, 1.0), Sinusoid(440.0, 1.0))

    def test_operators(self):
        with self.assertRaises(ValueError):
            Sinusoid(440.0, 1.0) + Sinusoid(466.1638, 1.0)
            Sinusoid(440.0, 1.0) - Sinusoid(466.1638, 1.0)
        self.assertEqual(Sinusoid(440.0, 1.0) + Sinusoid(440.0, 1.0), Sinusoid(440.0, 2.0))
        self.assertEqual(Sinusoid(440.0, 2.0) - Sinusoid(440.0, 1.0), Sinusoid(440.0, 1.0))
        self.assertIs(Sinusoid(440.0, 1.0) - Sinusoid(440.0, 2.0), None)

    def test_hash(self):
        s = Sinusoid(440.0, 1.0)
        self.assertEqual(hash(s), hash((440.0, 1.0)))
