"""Module implementing classes for reading and writing bits."""
import math


class BitInputStream():
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

    def close(self):
        """Close stream by closing input and reseting buffer."""
        self.input.close()
        self.bitbuffer = -1
        self.buffersize = 0


class BitOutputStream():
    """Class handling streaming bits to the output."""

    def __init__(self, out):
        """Initialize new instance with output and empty buffer."""
        self.output = out
        self.bitbuffer = 0
        self.buffersize = 0
        self.totalbytes = 0
        self.sym_counter = [0 for _ in range(256)]

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
            self.sym_counter[self.bitbuffer] += 1
            self.bitbuffer = 0
            self.buffersize = 0

    def close(self):
        """Close stream by flushing buffer and closing output."""
        while self.buffersize != 0:
            self.write_bit(0)
        self.output.close()

    def get_totalbytes(self):
        """Return total bytes written to the output."""
        return self.totalbytes

    def get_output_entropy(self):
        """Calculate and return entropy of the output code."""
        return sum([x*(math.log(self.totalbytes, 2)-math.log(x, 2)) for x in self.sym_counter if x > 0])/self.totalbytes
