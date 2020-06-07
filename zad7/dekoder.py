import argparse
import contextlib
import numpy as np

from inout_bits import BitInputStream, BitOutputStream


CORRECTION_MATRIX = np.array([[0, 0, 0, 1, 1, 1, 1],
                              [0, 1, 1, 0, 0, 1, 1],
                              [1, 0, 1, 0, 1, 0, 1]])


def parse_arguments():
    """
    Handle and parse program arguments.

    Returns:
        argparse.Namespace: namespace with 2 parsed arguments:
            - in1 -- one input file
            - in2 -- another input file
    """
    arg_parser = argparse.ArgumentParser(
        description='Kodowanie pliku korzystająć z rozszerzonego kodu Hamminga (8, 4)'
    )

    arg_parser.add_argument(
        'input_file',
        help='Plik wejściowy',

    )

    arg_parser.add_argument(
        'output_file',
        help='Zakodowany plik wyjściowy'
    )

    return arg_parser.parse_args()


class HammingDecoder:
    def __init__(self):
        self.doubleErrorCounter = 0

    def decode(self, bit_array):
        parity = bit_array[-1]
        bit_array = bit_array[:-1]
        wrong_bit = np.dot(CORRECTION_MATRIX, bit_array) % 2
        wrong_bit = int(f"0b{''.join(map(str, wrong_bit))}", 2)

        if wrong_bit > 0:
            if parity == 0:
                self.doubleErrorCounter += 1
            else:
                if wrong_bit < 5:
                    bit_array[wrong_bit-1] = int(not bit_array[wrong_bit-1])

        return bit_array[:4]


def decode():
    """Decode file with Hamming coding."""
    args = parse_arguments()
    hc = HammingDecoder()
    with contextlib.closing(BitInputStream(open(args.input_file, "rb"))) as bit_in, \
            contextlib.closing(BitOutputStream(open(args.output_file, "wb"))) as bit_out:
        bits = bit_in.bits_array(8)
        while bits.size > 0:
            bit_out.write_array(hc.decode(bits))
            bits = bit_in.bits_array(8)
    print("Zdekodowano")
    print("Liczba podwójnych błędów:", hc.doubleErrorCounter)


if __name__ == "__main__":
    decode()
