"""LZW algorithm."""
import math


EOF_CODE = 257


class LZWEncoder():
    """Class encoding files with LZW algorithm."""

    def __init__(self, dictionary, input_file, output_encoder):
        """Initialize new instance.

        -- dictionary - beginning dictionary with alphabet
        -- input_file - file to encode
        -- output_encoder - encoder to encode output
        """
        self.dict = dictionary
        self.input = input_file
        self.output_encoder = output_encoder
        self.totalbytes = 0
        self.sym_counter = [0 for _ in range(257)]

    def encode(self):
        """Perform LZW compression."""
        prefix = b''
        byte = self.input.read(1)
        while byte:
            self.totalbytes += 1
            self.sym_counter[byte[0]] += 1
            if prefix + byte in self.dict:
                prefix += byte
            else:
                self.output_encoder.write(self.dict.index(prefix)+1)
                self.dict.append(prefix+byte)
                prefix = byte
            byte = self.input.read(1)
        self.output_encoder.write(self.dict.index(prefix)+1)
        self.output_encoder.write(EOF_CODE)  # EOF

    def get_totalbytes(self):
        """Return total number of read bytes (size of the input file)."""
        return self.totalbytes

    def get_input_entropy(self):
        """Calculate and return entropy of the input file."""
        return sum([x*(math.log(self.totalbytes,2)-math.log(x,2)) for x in self.sym_counter if x > 0])/self.totalbytes


class LZWDecoder():
    """Class decoding files with LZW algorithm."""

    def __init__(self, dictionary, output_file, input_decoder):
        """Initialize new instance.

        -- dictionary - beginning dictionary with alphabet
        -- output_file - decoded result file
        -- input_decoder - decoder to decode input
        """
        self.dict = dictionary
        self.output = output_file
        self.input_decoder = input_decoder

    def decode(self):
        """Perform LZW decompression."""
        old_input = self.input_decoder.read()-1
        if old_input < 0:
            return
        s = self.dict[old_input]
        self.output.write(s)
        new_input = self.input_decoder.read()
        c = bytes((s[0],))
        while new_input > 0:
            new_input -= 1
            if new_input < 0 or new_input >= len(self.dict):
                s = self.dict[old_input]
                s += c
            else:
                s = self.dict[new_input]
            self.output.write(s)
            c = bytes((s[0],))
            self.dict.append(self.dict[old_input]+c)
            old_input = new_input
            new_input = self.input_decoder.read()
            if new_input == EOF_CODE:
                break
