from bisect import bisect_left, insort_left
from itertools import combinations
from math import e
from vassilakis_sra.sinusoid import Sinusoid


class SRAModel:

    def __init__(self, sinusoids):
        self._sinusoids = self.create_sinusoid_list(sinusoids)
        self._roughness_pairs = self.generate_roughness()

    @property
    def sinusoids(self):
        return self._sinusoids
    
    @property
    def roughness_pairs(self):
        return self._roughness_pairs

    @property
    def roughness(self):
        return sum(v for v in self.roughness_pairs.values())

    @staticmethod
    def generate_sinusoid_object(sinusoid):
        if isinstance(sinusoid, Sinusoid):
            return sinusoid
        frequency, amplitude = sinusoid
        return Sinusoid(frequency, amplitude)

    def generate_sinusoid_objects(self, sinusoids):
        for sinusoid in sinusoids:
            yield self.generate_sinusoid_object(sinusoid)

    def create_sinusoid_list(self, sinusoids):
        sinusoid_list = list()
        for sinusoid in self.generate_sinusoid_objects(sinusoids):
            index = bisect_left(sinusoid_list, sinusoid)
            if index == len(sinusoid_list):
                sinusoid_list.insert(index, sinusoid)
            else:
                try:
                    sinusoid_list[index] = sinusoid_list[index] + sinusoid
                except ValueError:
                    sinusoid_list.insert(index, sinusoid)
        return sinusoid_list

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

    def generate_roughness(self):
        roughness_pairs = dict()
        for pair in combinations(self.sinusoids, 2):
            sinusoid_1, sinusoid_2 = pair
            roughness_value = self.generate_roughness_value_from_pair(sinusoid_1, sinusoid_2)
            roughness_pairs.update({(sinusoid_1, sinusoid_2): roughness_value})
        return roughness_pairs

    def remove_sinusoid(self, sinusoid):
        sinusoid = self.generate_sinusoid_object(sinusoid)
        index = bisect_left(self.sinusoids, sinusoid)
        if index < len(self.sinusoids) and sinusoid.frequency == self.sinusoids[index].frequency:
            new_sinusoid = None
            for k in self.roughness_pairs:
                sinusoid_1, sinusoid_2 = k
                if sinusoid_1 == sinusoid:
                    existing_sinusoid, paired_sinusoid = sinusoid_1, sinusoid_2
                elif sinusoid_2 == sinusoid:
                    existing_sinusoid, paired_sinusoid = sinusoid_2, sinusoid_1
                else:
                    continue
                del self.roughness_pairs[k]
                if new_sinusoid is not None:
                    new_sinusoid = existing_sinusoid - sinusoid
                if new_sinusoid:
                    roughness_value = self.generate_roughness_value_from_pair(new_sinusoid, paired_sinusoid)
                    self.roughness_pairs.update({(new_sinusoid, paired_sinusoid): roughness_value})
            del self.sinusoids[bisect_left(self.sinusoids, existing_sinusoid)]
            if new_sinusoid:
                insort_left(self.sinusoids, new_sinusoid)

    def remove_sinusoids(self, sinusoids):
        for sinusoid in sinusoids:
            self.remove_sinusoid(sinusoid)

    def remove_sinusoid_by_frequency(self, frequency):
        index = bisect_left(self.sinusoids, Sinusoid(frequency, 1.0))
        if index < len(self.sinusoids) and frequency == self.sinusoids[index].frequency:
            self.remove_sinusoid(self.sinusoids[index])

    def add_sinusoid(self, sinusoid):
        sinusoid = self.generate_sinusoid_object(sinusoid)
        index = bisect_left(self.sinusoids, sinusoid)
        if index < len(self.sinusoids) and sinusoid.frequency == self.sinusoids[index].frequency:
            self.remove_sinusoid(self.sinusoids[index])
        for existing_sinusoid in self.sinusoids:
            roughness_value = self.generate_roughness_value_from_pair(sinusoid, existing_sinusoid)
            self.roughness_pairs.update({(sinusoid, existing_sinusoid): roughness_value})
        insort_left(self.sinusoids, sinusoid)

    def add_sinusoids(self, sinusoids):
        for sinusoid in sinusoids:
            self.add_sinusoid(sinusoid)

    def __str__(self):
        return 'SRA model with {} sinusoids and roughness value of {:.2f}'.format(len(self.sinusoids), self.roughness)
    
    def __repr__(self):
        return 'SRAModel([{}])'.format(', '.join(repr(sinusoid) for sinusoid in self.sinusoids))

    def __lt__(self, other):
        return self.roughness < other.roughness

    def __gt__(self, other):
        return self.roughness > other.roughness

    def __eq__(self, other):
        return self.sinusoids == other.sinusoids

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
