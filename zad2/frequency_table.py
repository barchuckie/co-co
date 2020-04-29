"""Frequency table implementation."""
import math
import numpy as np
from abc import ABC, abstractmethod


class FrequencyTable(ABC):
    """Base class for handling a table of sybol frequences."""

    @abstractmethod
    def get_symbol_limit(self):
        """Return the number of symbols in this frequency table.

        Returned value is a positive number.
        """
        raise NotImplementedError()

    @abstractmethod
    def get(self, symbol):
        """Return the frequency of the given symbol.

        The returned value is at least 0.
        """
        raise NotImplementedError()

    @abstractmethod
    def set(self, symbol, freq):
        """Set the frequency of the given symbol to the given value.

        The frequency value must be at least 0.
        """
        raise NotImplementedError()

    @abstractmethod
    def increment(self, symbol):
        """Increment the frequency of the given symbol."""
        raise NotImplementedError()

    @abstractmethod
    def get_total(self):
        """Return the total of all symbol frequencies.

        The returned value is at least 0 and is always equal to
        get_high(get_symbol_limit() - 1).
        """
        raise NotImplementedError()

    @abstractmethod
    def get_low(self, symbol):
        """Return the lower boundary.

        Lower boundary is a sum of the frequencies of all the symbols strictly
        below the given symbol value. The returned value is at least 0.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_high(self, symbol):
        """Return the upper boundary.

        Upper boundary is a sum of the frequencies of the given symbol
        and all the symbols below. The returned value is at least 0.
        """
        raise NotImplementedError()


class FlatFrequencyTable(FrequencyTable):
    """An immutable frequency table where every symbol has the same frequency of 1."""

    def __init__(self, numsyms):
        """Construct a flat frequency table with the given number of symbols."""
        if numsyms < 1:
            raise ValueError("Number of symbols must be positive")
        self.numsymbols = numsyms

    def get_symbol_limit(self):
        """Return the number of symbols in this table (> 1)."""
        return self.numsymbols

    def get(self, symbol):
        """Return the frequency of the given symbol, which is always 1."""
        self._check_symbol(symbol)
        return 1

    def get_total(self):
        """Return total sum of all symbol frequencies, which is number of symbols."""
        return self.numsymbols

    def get_low(self, symbol):
        """Return lower boundary, which is equal to symbol."""
        self._check_symbol(symbol)
        return symbol

    def get_high(self, symbol):
        """Return lower boundary, which is equal to symbol + 1."""
        self._check_symbol(symbol)
        return symbol + 1

    def _check_symbol(self, symbol):
        """Return silently if 0 <= symbol < numsymbols, otherwise raise an exception."""
        if 0 <= symbol < self.numsymbols:
            return
        raise ValueError("Symbol out of range")

    def set(self, symbol, freq):
        """Not implemented since this table is immutable."""
        raise NotImplementedError()

    def increment(self, symbol):
        """Not implemented since this table is immutable."""
        raise NotImplementedError()


class SimpleFrequencyTable(FrequencyTable):
    """A mutable table of symbol frequencies.

    However, the number of symbols cannot be changed after construction.
    """

    def __init__(self, freqs):
        """Construct a simple frequency table in two ways.

        Table can be build from FrequencyTable object or simple sequence.
        Number of the elements must be at least 1.
        """
        if isinstance(freqs, FrequencyTable):
            numsym = freqs.get_symbol_limit()
            self.frequencies = np.array([freqs.get(i) for i in range(numsym)])
        else:
            self.frequencies = np.array(freqs)  # list(freqs)

        if len(self.frequencies) < 1:
            raise ValueError("At least 1 symbol needed")
        for freq in self.frequencies:
            if freq < 0:
                raise ValueError("Negative frequency")

        self.total = sum(self.frequencies)
        self.cumulative = None

    def get_symbol_limit(self):
        """Return the number of symbols in this frequency table."""
        return len(self.frequencies)

    def get(self, symbol):
        """Return the frequency of the given symbol."""
        self._check_symbol(symbol)
        return self.frequencies[symbol]

    def set(self, symbol, freq):
        """Set the frequency of the given symbol to the given value."""
        self._check_symbol(symbol)
        if freq < 0:
            raise ValueError("Negative frequency")
        temp = self.total - self.frequencies[symbol]
        self.total = temp + freq
        self.frequencies[symbol] = freq
        self.cumulative = None

    def increment(self, symbol):
        """Increments the frequency of the given symbol."""
        self._check_symbol(symbol)
        self.total += 1
        self.frequencies[symbol] += 1
        self.cumulative = None

    def get_total(self):
        """Return the total of all symbol frequencies."""
        return self.total

    def get_low(self, symbol):
        """Return the lower boundary.

        Lower boundary is a sum of the frequencies of all the symbols strictly
        below the given symbol value. It is stored in the cumulative list.
        The returned value is at least 0.
        """
        self._check_symbol(symbol)
        if self.cumulative is None:
            self._init_cumulative()
        return self.cumulative[symbol]

    def get_high(self, symbol):
        """Return the upper boundary.

        Upper boundary is a sum of the frequencies of the given symbol
        and all the symbols below. It is stored in the cumulative list.
        The returned value is at least 0.
        """
        self._check_symbol(symbol)
        if self.cumulative is None:
            self._init_cumulative()
        return self.cumulative[symbol + 1]

    def _init_cumulative(self):
        """Recompute the array of cumulative symbol frequencies."""
        cumul = [0]
        sum = 0
        for freq in self.frequencies:
            sum += freq
            cumul.append(sum)
        assert sum == self.total
        self.cumulative = cumul

    def _check_symbol(self, symbol):
        """Return silently if 0 <= symbol < len(frequencies), otherwise raises an exception."""
        if 0 <= symbol < len(self.frequencies):
            return
        raise ValueError("Symbol out of range")

    def entropy(self):
        """Return entropy of the data in the table."""
        return sum([(x-1)*(math.log(self.get_in_size(), 2)-math.log((x-1), 2)) for x in self.frequencies if x > 1])/self.get_in_size()

    def get_in_size(self):
        """Return size of the input data."""
        return self.total - len(self.frequencies)
