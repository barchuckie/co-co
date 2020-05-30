"""Module implementing classes for reading and writing bits."""
import contextlib

import numpy as np

from pixels import PixelDifference


class BitInputStream:
    """Class handling streaming bits from the input."""

    def __init__(self, inp):
        """Initialize new instance with input and empty buffer."""
        self.input = inp
        self.bitbuffer = 0
        self.buffersize = 0

    def read_bit(self):
        """Stream bit from buffer.

        If buffer is empty, read from input.
        """
        if self.bitbuffer == -1:
            return -1
        if self.buffersize == 0:
            temp = self.input.read(1)
            if len(temp) == 0:
                self.bitbuffer = -1
                return -1
            self.bitbuffer = temp[0]
            self.buffersize = 8
        self.buffersize -= 1
        return (self.bitbuffer >> self.buffersize) & 1

    def read_byte(self):
        return self.input.read(1)[0]

    def read_bits(self, number_of_bits):
        value = 0
        for _ in range(number_of_bits):
            value <<= 1
            value += self.read_bit()
        return value

    def close(self):
        """Close stream by closing input and reseting buffer."""
        self.input.close()
        self.bitbuffer = -1
        self.buffersize = 0


class BitOutputStream:
    """Class handling streaming bits to the output."""

    def __init__(self, out):
        """Initialize new instance with output and empty buffer."""
        self.output = out
        self.bitbuffer = 0
        self.buffersize = 0
        self.totalbytes = 0

    def write_bit(self, bit):
        """Stream bit to the buffer.

        If buffer is full, write to input.
        """
        if bit not in (0, 1):
            raise ValueError("Argument must be 0 or 1")
        self.bitbuffer = (self.bitbuffer << 1) | bit
        self.buffersize += 1
        if self.buffersize == 8:
            towrite = bytes((self.bitbuffer,))
            self.output.write(towrite)
            self.totalbytes += 1
            self.bitbuffer = 0
            self.buffersize = 0

    def write_byte(self, byte):
        self.output.write(byte)

    def write_bits(self, value, bits):
        mask = (1 << bits) - 1
        for _ in range(bits):
            self.write_bit(value >> (bits-1))
            value = value << 1 & mask

    def close(self):
        """Close stream by flushing buffer and closing output."""
        while self.buffersize != 0:
            self.write_bit(0)
        self.output.close()

    def get_totalbytes(self):
        """Return total bytes written to the output."""
        return self.totalbytes


class CompressFileWriter:
    def __init__(self, filename, height, width, quantizer_bits):
        self.filename = filename
        self.height = height
        self.width = width
        self.quantizer_bits = quantizer_bits

    def write_header(self, bit_out):
        bit_out.write_byte(bytes((self.width % 256, self.width // 256)))
        bit_out.write_byte(bytes((self.height % 256, self.height // 256)))
        bit_out.write_byte(bytes((self.quantizer_bits,)))

    def write(self, high_quantizer, high_idx_sequence, low_quantizer, low_idx_sequence):
        with contextlib.closing(BitOutputStream(open(self.filename, "wb"))) as bit_out:
            self.write_header(bit_out)
            self.write_quantizer(bit_out, high_quantizer)
            self.write_quantizer(bit_out, low_quantizer)
            self.write_indexes(bit_out, high_idx_sequence)
            self.write_indexes(bit_out, low_idx_sequence)

    def write_quantizer(self, bit_out, quantizer):
        for entry in quantizer:
            bit_out.write_bits(encode_difference(entry.red), 9)
            bit_out.write_bits(encode_difference(entry.green), 9)
            bit_out.write_bits(encode_difference(entry.blue), 9)

    def write_indexes(self, bit_out, idx_sequence):
        for idx in idx_sequence:
            bit_out.write_bits(idx, self.quantizer_bits)


class CompressFileReader:
    def __init__(self, filename):
        self.filename = filename
        self.width = None
        self.height = None
        self.quantizer_bits = None
        self.high_quantizer = None
        self.low_quantizer = None
        self.high_idx_sequence = None
        self.low_idx_sequence = None

    def read(self):
        with contextlib.closing(BitInputStream(open(self.filename, "rb"))) as bit_in:
            self.read_header(bit_in)
            self.high_quantizer = self.read_quantizer(bit_in)
            self.low_quantizer = self.read_quantizer(bit_in)
            self.high_idx_sequence = self.read_sequence(bit_in)
            self.low_idx_sequence = self.read_sequence(bit_in)


    def read_header(self, bit_in):
        self.width = bit_in.read_byte() + (bit_in.read_byte() << 8)
        self.height = bit_in.read_byte() + (bit_in.read_byte() << 8)
        self.quantizer_bits = bit_in.read_byte()

    def read_quantizer(self, bit_in):
        quantizer = np.empty(1 << self.quantizer_bits, dtype=PixelDifference)

        for i in range(quantizer.size):
            quantizer[i] = PixelDifference(
                decode_difference(bit_in.read_bits(9)),
                decode_difference(bit_in.read_bits(9)),
                decode_difference(bit_in.read_bits(9))
            )

        return quantizer

    def read_sequence(self, bit_in):
        sequence = np.empty(self.width*self.height // 2, dtype=np.uint8)
        for i in range(sequence.size):
            sequence[i] = bit_in.read_bits(self.quantizer_bits)
        return sequence


def encode_difference(difference):
    if difference > 0:
        return (difference << 1) - 1
    return -2 * difference


def decode_difference(encoded_difference):
    if encoded_difference % 2 == 1:
        return (encoded_difference + 1) >> 1
    return - (encoded_difference >> 1)
