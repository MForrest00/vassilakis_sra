class Sinusoid:

    def __init__(self, frequency, amplitude):
        self.frequency = frequency
        self.amplitude = amplitude
    
    def __check_valid_number_argument(self, argument):
        if not isinstance(argument, int) and not isinstance(argument, float):
            raise TypeError('Frequency and amplitude values must be an integers or floats')
        if argument <= 0:
            raise ValueError('Frequency and amplitude values must be greater than 0')

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        self.__check_valid_number_argument(frequency)
        self._frequency = float(frequency)

    @property
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, amplitude):
        self.__check_valid_number_argument(amplitude)
        self._amplitude = float(amplitude)

    def __str__(self):
        return 'Sinusoid with frequency of {} and amplitude of {}'.format(self.frequency, self.amplitude)
    
    def __repr__(self):
        return 'Sinusoid({}, {})'.format(self.frequency, self.amplitude)

    def __add__(self, other):
        if self.frequency != other.frequency:
            raise ValueError('Only Sinusoids with the same frequency can be added')
        return self.__class__(self.frequency, self.amplitude + other.amplitude)

    def __sub__(self, other):
        if self.frequency != other.frequency:
            raise ValueError('Only Sinusoids with the same frequency can be subtracted')
        if self.amplitude > other.amplitude:
            return self.__class__(self.frequency, self.amplitude - other.amplitude)
        return None

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __gt__(self, other):
        return self.frequency > other.frequency

    def __eq__(self, other):
        return self.frequency == other.frequency and self.amplitude == other.amplitude

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __hash__(self):
        return hash((self.frequency, self.amplitude))
