"""Module implementing arithmetic coding."""
from abc import ABC, abstractmethod


class ArithmeticCoder(ABC):
    """Base class for arithmetic coding."""

    def __init__(self, numbits):
        """Construct an arithmetic coder, which initializes the code range.
        
        -- numbits - number of state bits"""
        if numbits < 1:
            raise ValueError("State size out of range")

        self.num_state_bits = numbits
        self.full_range = 1 << self.num_state_bits
        self.half_range = self.full_range >> 1
        self.quarter_range = self.half_range >> 1
        self.minimum_range = self.quarter_range + 2
        self.maximum_total = self.minimum_range
        self.state_mask = self.full_range - 1

        self.low = 0
        self.high = self.state_mask

    def update(self, freqs, symbol):
        """Update code range."""
        low = self.low
        high = self.high
        if low >= high or (low & self.state_mask) != low or (high & self.state_mask) != high:
            raise AssertionError("Low or high out of range")
        rng = high - low + 1
        if not self.minimum_range <= rng <= self.full_range:
            raise AssertionError("Range out of range")

        total = freqs.get_total()
        symlow = freqs.get_low(symbol)
        symhigh = freqs.get_high(symbol)
        if symlow == symhigh:
            raise ValueError("Symbol has zero frequency")
        if total > self.maximum_total:
            raise ValueError("Cannot code symbol because total is too large")

        newlow = low + symlow * rng // total
        newhigh = low + symhigh * rng // total - 1
        self.low = newlow
        self.high = newhigh

        while ((self.low ^ self.high) & self.half_range) == 0:
            self.shift()
            self.low = ((self.low << 1) & self.state_mask)
            self.high = ((self.high << 1) & self.state_mask) | 1

        while (self.low & ~self.high & self.quarter_range) != 0:
            self.underflow()
            self.low = (self.low << 1) ^ self.half_range
            self.high = ((self.high ^ self.half_range) << 1) | self.half_range | 1

    @abstractmethod
    def shift(self):
        """Handle the situation when the top bit of 'low' and 'high' are equal."""
        raise NotImplementedError()

    @abstractmethod
    def underflow(self):
        """Handle the situation when low=01(...) and high=10(...)."""
        raise NotImplementedError()


class ArithmeticEncoder(ArithmeticCoder):
    """Class handling arithmetic encoding."""

    def __init__(self, numbits, bitout):
        """Construct an arithmetic coding encoder based on the given bit output stream."""
        super(ArithmeticEncoder, self).__init__(numbits)
        self.output = bitout
        self.num_underflow = 0

    def write(self, freqs, symbol):
        """Encode the given symbol based on the given frequency table.

        This updates this arithmetic coder's state and may write out some bits.
        """
        self.update(freqs, symbol)

    def finish(self):
        """Terminate the arithmetic coding.

        Terminates the arithmetic coding by flushing any buffered bits,
        so that the output can be decoded properly. It is important that
        this method must be called at the end of the each encoding process.
        """
        self.output.write_bit(1)

    def shift(self):
        """Shift bits."""
        bit = self.low >> (self.num_state_bits - 1)
        self.output.write_bit(bit)

        for _ in range(self.num_underflow):
            self.output.write_bit(bit ^ 1)
        self.num_underflow = 0

    def underflow(self):
        """Increment underflow."""
        self.num_underflow += 1


class ArithmeticDecoder(ArithmeticCoder):
    """Reads from an arithmetic-coded bit stream and decodes symbols."""

    def __init__(self, numbits, bitin):
        """Construct an arithmetic coding decoder based on the given bit input stream and fills the code bits."""
        super(ArithmeticDecoder, self).__init__(numbits)
        self.input = bitin
        self.code = 0
        for _ in range(self.num_state_bits):
            self.code = self.code << 1 | self.read_code_bit()

    def read(self, freqs):
        """Decode the next symbol based on the given frequency table and return it.

        Also update this arithmetic coder's state and may read in some bits.
        """

        total = freqs.get_total()
        if total > self.maximum_total:
            raise ValueError("Cannot decode symbol because total is too large")
        rng = self.high - self.low + 1
        offset = self.code - self.low
        value = ((offset + 1) * total - 1) // rng

        start = 0
        end = freqs.get_symbol_limit()
        while end - start > 1:
            middle = (start + end) >> 1
            if freqs.get_low(middle) > value:
                end = middle
            else:
                start = middle

        symbol = start
        self.update(freqs, symbol)
        if not (self.low <= self.code <= self.high):
            raise AssertionError("Code out of range")
        return symbol

    def shift(self):
        self.code = ((self.code << 1) & self.state_mask) | self.read_code_bit()

    def underflow(self):
        self.code = (self.code & self.half_range) | ((self.code << 1) & (self.state_mask >> 1)) | self.read_code_bit()

    def read_code_bit(self):
        """Return the next bit (0 or 1) from the input stream.

        The end of stream is treated as an infinite number of trailing zeros.
        """
        temp = self.input.read_bit()
        if temp == -1:
            temp = 0
        return temp
