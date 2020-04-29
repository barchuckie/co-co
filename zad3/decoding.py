"""Wrapers to decoding input."""
import fibonacci
from abc import ABC, abstractmethod


class Decoding(ABC):
    """Abstract class for encoding."""

    def __init__(self, inp):
        """Initialize with output to write to."""
        self.input = inp  # BitInputStream

    @abstractmethod
    def read(self):
        """Read from input and decode."""
        return NotImplementedError()


class Gamma(Decoding):
    """Elias gamma decoding."""

    def read(self):
        """Read from input and decode with Elias gamma coding."""
        zero_counter = 0
        bit = self.input.read_bit()
        while bit == 0:
            zero_counter += 1
            bit = self.input.read_bit()
        if bit == -1:
            return -1
        binary = str(bit)
        for _ in range(zero_counter):
            bit = self.input.read_bit()
            if bit == -1:
                raise EOFError()
            binary += str(bit)

        return int(binary, 2)


class Delta(Decoding):
    """Elias delta decoding."""

    def read(self):
        """Read from input and decode with Elias delta coding."""
        zero_counter = 0
        bit = self.input.read_bit()
        while bit == 0:
            zero_counter += 1
            bit = self.input.read_bit()
        if bit == -1:
            return -1
        len_binary = str(bit)
        for _ in range(zero_counter):
            bit = self.input.read_bit()
            if bit == -1:
                raise EOFError()
            len_binary += str(bit)
        binary = '1'
        for _ in range(int(len_binary, 2)-1):
            bit = self.input.read_bit()
            if bit == -1:
                raise EOFError()
            binary += str(bit)
        return int(binary, 2)


class Omega(Decoding):
    """Elias omega decoding."""

    def __init__(self, inp):
        """Initialize new instance with output stream and special flag.

        Flag is used to allow reading 1s at the beginning.
        """
        super().__init__(inp)
        self.flag = False

    def read(self):
        """Read from input and decode with Elias omega coding."""
        num = 1
        bit = self.input.read_bit()
        if bit == -1:
            return -1
        while bit != 0:
            binary = str(bit)
            for _ in range(num):
                bit = self.input.read_bit()
                if bit == -1:
                    return -1
                binary += str(bit)
            num = int(binary, 2)
            bit = self.input.read_bit()
            if bit == -1:
                return -1
        # if num > 1:
        #     self.flag = True
        return num


class Fibonacci(Decoding, fibonacci.Fibonacci):
    """Fibonacci decoding."""

    def __init__(self, inp):
        """Initialize with Fibonacci cache and input to read from."""
        fibonacci.Fibonacci.__init__(self)
        Decoding.__init__(self, inp)

    def read(self):
        """Read from input and decode with Fibonacci coding."""
        old_bit = self.input.read_bit()
        new_bit = self.input.read_bit()
        if new_bit == -1:
            return -1
        binary = str(old_bit)
        while not old_bit == new_bit == 1:
            old_bit = new_bit
            binary += str(old_bit)
            new_bit = self.input.read_bit()
            if new_bit == -1:
                return -1
        num = 0
        bin_len = len(binary)
        for i in range(bin_len):
            if binary[i] == '1':
                num += self.fib(i+1)
        return num
