#!/usr/bin/env python

import argparse
import contextlib
import numpy as np

from inout_bits import BitInputStream, BitOutputStream


GEN_MATRIX = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1],
                       [0, 1, 1, 1],
                       [1, 0, 1, 1],
                       [1, 1, 0, 1]])


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


def hamming_encode(bit_array):
    encoded_bits = np.dot(GEN_MATRIX, bit_array) % 2
    parity = sum(encoded_bits) % 2
    return np.append(encoded_bits, parity)


def encode():
    """Compare two files with each other."""
    args = parse_arguments()
    with contextlib.closing(BitInputStream(open(args.input_file, "rb"))) as bit_in, \
            contextlib.closing(BitOutputStream(open(args.output_file, "wb"))) as bit_out:
        raw_bits = bit_in.bits_array(4)
        while raw_bits.size > 0:
            bit_out.write_array(hamming_encode(raw_bits))
            raw_bits = bit_in.bits_array(4)
    print("Zakodowano")


if __name__ == "__main__":
    encode()
