from itertools import combinations
from math import e
from vassilakis_sra.sinusoid import Sinusoid


class SRAModel:

    def __init__(self, sinusoids):
        self.roughness_pairs = self.generate_roughness(sinusoids)

    @property
    def roughness(self):
        return sum(v for v in self.roughness_pairs.values())

    @staticmethod
    def generate_roughness_value_from_pair(sinusoid_1, sinusoid_2):
        b1 = 3.5
        b2 = 5.75
        s1 = 0.0207
        s2 = 18.96
        frequency_min = min(sinusoid_1.frequency, sinusoid_2.frequency)
        frequency_max = max(sinusoid_1.frequency, sinusoid_2.frequency)
        amplitude_min = min(sinusoid_1.amplitude, sinusoid_2.amplitude)
        amplitude_max = max(sinusoid_1.amplitude, sinusoid_2.amplitude)
        s = 0.24 / ((s1 * frequency_min) + s2)
        X = amplitude_min * amplitude_max
        Y = (2 * amplitude_min) / (amplitude_min + amplitude_max)
        Z = pow(e, -1 * b1 * s * (frequency_max - frequency_min)) - \
            pow(e, -1 * b2 * s * (frequency_max - frequency_min))
        return pow(X, 0.1) * 0.5 * pow(Y, 3.11) * Z

    @staticmethod
    def generate_sinusoid_objects(sinusoids):
        for sinusoid in sinusoids:
            if isinstance(sinusoid, Sinusoid):
                yield sinusoid
            else:
                frequency, amplitude = sinusoid
                yield Sinusoid(frequency, amplitude)

    def generate_roughness(self, sinusoids):
        roughness_pairs = dict()
        for pair in combinations(self.generate_sinusoid_objects(sinusoids), 2):
            sinusoid_1, sinusoid_2 = pair
            roughness_value = self.generate_roughness_value_from_pair(sinusoid_1, sinusoid_2)
            roughness_pairs.update({(sinusoid_1, sinusoid_2): roughness_value})
        return roughness_pairs
