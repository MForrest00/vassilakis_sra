from bisect import bisect_left, insort_left
from collections import namedtuple
from itertools import combinations
from math import e
from vassilakis_sra.sinusoid import Sinusoid


RoughnessContribution = namedtuple('RoughnessContribution', ['roughness', 'percentage'])


class VassilakisSRAModel:
    """A stateful representation of the Vassilakis SRA model applied to a set of sinusoids

    Arguments:
        sinusoids (list): list of Sinusoid objects or two-item tuples (with the items representing the frequency and
            amplitude of the sinusoid)
    """

    def __init__(self, sinusoids):
        self.sinusoids = self.create_sinusoid_list(sinusoids)
        self.roughness_pairs = self.generate_roughness()

    @property
    def sinusoids(self):
        return self._sinusoids

    @sinusoids.setter
    def sinusoids(self, sinusoids):
        self._sinusoids = sinusoids

    @property
    def roughness_pairs(self):
        return self._roughness_pairs

    @roughness_pairs.setter
    def roughness_pairs(self, roughness_pairs):
        self._roughness_pairs = roughness_pairs

    @property
    def roughness(self):
        return sum(v for v in self.roughness_pairs.values())

    @property
    def roughness_contributions(self):
        sinusoid_roughness = {s: 0 for s in self.sinusoids}
        for k, v in self.roughness_pairs.items():
            sinusoid_1, sinusoid_2 = k
            sinusoid_roughness[sinusoid_1] += v
            sinusoid_roughness[sinusoid_2] += v
        return {
            k: RoughnessContribution(roughness=v, percentage=v / self.roughness)
            for k, v in sinusoid_roughness.items()
        }

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
        x = amplitude_min * amplitude_max
        y = (2 * amplitude_min) / (amplitude_min + amplitude_max)
        z = pow(e, -1 * b1 * s * (frequency_max - frequency_min)) - \
            pow(e, -1 * b2 * s * (frequency_max - frequency_min))
        return pow(x, 0.1) * 0.5 * pow(y, 3.11) * z

    def generate_roughness(self):
        roughness_pairs = dict()
        for pair in combinations(self.sinusoids, 2):
            sinusoid_1, sinusoid_2 = pair
            roughness_value = self.generate_roughness_value_from_pair(sinusoid_1, sinusoid_2)
            roughness_pairs.update({(sinusoid_1, sinusoid_2): roughness_value})
        return roughness_pairs

    def add_sinusoid(self, sinusoid):
        """Add a sinusoid to the SRAModel

        Arguments:
            sinusoid (Sinusoid or tuple): Sinusoid object or two-item tuple (with the items representing the frequency
                and amplitude of the sinusoid)
        """
        sinusoid = self.generate_sinusoid_object(sinusoid)
        index = bisect_left(self.sinusoids, sinusoid)
        if index < len(self.sinusoids) and sinusoid.frequency == self.sinusoids[index].frequency:
            sinusoid += self.sinusoids[index]
            self.remove_sinusoid(self.sinusoids[index])
        for existing_sinusoid in self.sinusoids:
            roughness_value = self.generate_roughness_value_from_pair(sinusoid, existing_sinusoid)
            self.roughness_pairs.update({(sinusoid, existing_sinusoid): roughness_value})
        insort_left(self.sinusoids, sinusoid)

    def add_sinusoids(self, sinusoids):
        """Add sinusoids to the SRAModel

        Arguments:
            sinusoids (list): list of Sinusoid objects or two-item tuples (with the items representing the frequency and
                amplitude of the sinusoid)
        """
        for sinusoid in sinusoids:
            self.add_sinusoid(sinusoid)

    def remove_sinusoid(self, sinusoid):
        """Remove a sinusoid from the SRAModel

        Arguments:
            sinusoid (Sinusoid or tuple): Sinusoid object or two-item tuple (with the items representing the frequency
                and amplitude of the sinusoid)
        """
        sinusoid = self.generate_sinusoid_object(sinusoid)
        index = bisect_left(self.sinusoids, sinusoid)
        if index < len(self.sinusoids) and sinusoid.frequency == self.sinusoids[index].frequency:
            new_sinusoid = self.sinusoids[index] - sinusoid
            for k in list(self.roughness_pairs.keys()):
                sinusoid_1, sinusoid_2 = k
                if sinusoid_1.frequency == sinusoid.frequency or sinusoid_2.frequency == sinusoid.frequency:
                    del self.roughness_pairs[k]
            del self.sinusoids[index]
            if new_sinusoid:
                self.add_sinusoid(new_sinusoid)

    def remove_sinusoids(self, sinusoids):
        """Remove sinusoids from the SRAModel

        Arguments:
            sinusoids (list): list of Sinusoid objects or two-item tuples (with the items representing the frequency and
                amplitude of the sinusoid)
        """
        for sinusoid in sinusoids:
            self.remove_sinusoid(sinusoid)

    def remove_sinusoid_by_frequency(self, frequency):
        """Remove a sinusoid from the SRAModel with the specified frequency

        Arguments:
            frequency (int or float): frequency of the Sinusoid object to remove
        """
        index = bisect_left(self.sinusoids, Sinusoid(frequency, 1.0))
        if index < len(self.sinusoids) and frequency == self.sinusoids[index].frequency:
            self.remove_sinusoid(self.sinusoids[index])

    def __str__(self):
        sinusoid_count = len(self.sinusoids)
        return 'Vassilakis SRA model with {} sinusoids and roughness value of {:.2f}'.format(sinusoid_count,
                                                                                             self.roughness)

    def __repr__(self):
        return 'VassilakisSRAModel([{}])'.format(', '.join(repr(sinusoid) for sinusoid in self.sinusoids))

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

    def __bool__(self):
        if len(self.sinusoids) > 0:
            return True
        return False

    def __copy__(self):
        return self.__class__(self.sinusoids.copy())
