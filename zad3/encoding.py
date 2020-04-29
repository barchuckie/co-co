"""Wrapers to encoding output."""
import fibonacci
from abc import ABC, abstractmethod


class Encoding(ABC):
    """Abstract class for encoding."""

    def __init__(self, out):
        """Initialize with output to write to."""
        self.output = out  # BitOutputStream

    def write(self, num):
        """Encode a number and write to output."""
        code = self.encode(num)
        for bit in code:
            self.output.write_bit(int(bit))

    @abstractmethod
    def encode(self, num):
        """Abstract method encoding a number."""
        return NotImplementedError()


def _gamma_encode(num):
    """Encode a number with Elias gamma coding."""
    binary = bin(num)
    prefix_len = len(binary) - 3
    return prefix_len*'0' + binary[2:]


class Gamma(Encoding):
    """Elias gamma encoding."""

    def encode(self, num):
        """Encode a number with Elias gamma coding."""
        return _gamma_encode(num)


class Delta(Encoding):
    """Elias delta encoding."""

    def encode(self, num):
        """Encode a number with Elias delta coding."""
        binary = bin(num)
        bin_len = len(binary) - 2
        prefix = _gamma_encode(bin_len)
        return prefix + binary[3:]


class Omega(Encoding):
    """Elias omega encoding."""

    def encode(self, num):
        """Encode a number with Elias omega coding."""
        if num == 0:
            print(num)
        result = '0'
        k = num
        while k > 1:
            binary_k = bin(k)
            result = binary_k[2:] + result
            k = len(binary_k) - 3
        return result


class Fibonacci(Encoding, fibonacci.Fibonacci):
    """Fibonacci encoding."""

    def __init__(self, out):
        """Initialize with Fibonacci cache and output to write to."""
        fibonacci.Fibonacci.__init__(self)
        Encoding.__init__(self, out)

    def encode(self, num):
        """Encode a number with Fibonacci coding."""
        i = 1
        while self.fib(i+1) <= num:
            i += 1
        binary = ''
        while i > 0:
            if self.fib(i) <= num:
                binary = '1' + binary
                num -= self.fib(i)
            else:
                binary = '0' + binary
            i -= 1
        return binary + '1'
