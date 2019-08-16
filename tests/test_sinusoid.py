import unittest
from vassilakis_sra import Sinusoid


class TestSinusoid(unittest.TestCase):

    def setUp(self):
        self.s1 = Sinusoid(440.0, 1.0)
        self.s2 = Sinusoid(440.0, 2.0)
        self.s3 = Sinusoid(466.1638, 1.0)
        self.s4 = Sinusoid(466.1638, 2.0)

    def test_construction(self):
        with self.assertRaises(TypeError):
            Sinusoid('string', 1.0)
        with self.assertRaises(ValueError):
            Sinusoid(0.0, 1.0)
            Sinusoid(1.0, -1.0)

    def test_comparison(self):
        self.assertEqual(self.s1, Sinusoid(440.0, 1.0))
        self.assertNotEqual(self.s1, self.s2)
        self.assertLess(self.s1, self.s3)
        self.assertLessEqual(self.s1, self.s3)
        self.assertGreater(self.s3, self.s1)
        self.assertGreaterEqual(self.s3, self.s1)

    def test_operators(self):
        with self.assertRaises(ValueError):
            self.s1 + self.s3
            self.s1 - self.s3
        self.assertEqual(self.s1 + self.s1, self.s2)
        self.assertEqual(self.s2 - self.s1, self.s1)
        self.assertIs(self.s1 - self.s1, None)
        self.assertEqual(self.s1 * 2, self.s2)
        self.assertEqual(self.s2 / 2, self.s1)

    def test_hash(self):
        self.assertEqual(hash(self.s1), hash((440.0, 1.0)))
