#!/usr/bin/env python

import argparse
import contextlib
import random

from inout_bits import BitInputStream, BitOutputStream


def parse_arguments():
    """
    Handle and parse program arguments.

    Returns:
        argparse.Namespace: namespace with 3 parsed arguments:
            - p -- probability of bit to be changed
            - input_file -- input file
            - output_file -- noised result file
    """
    arg_parser = argparse.ArgumentParser(
        description='Zaszumianie pliku'
    )

    arg_parser.add_argument(
        'p',
        help='Prawdopodobieństwo podmiany bitu',
        type=float
    )

    arg_parser.add_argument(
        'input_file',
        help='plik wejściowy',

    )

    arg_parser.add_argument(
        'output_file',
        help='Zaszumiony plik wyjściowy'
    )

    return arg_parser.parse_args()


def random_swap(bit, probability):
    if random.random() > probability:
        return bit
    return int(not bit)


def noise():
    """Create output file by making noise to the input file."""
    args = parse_arguments()
    with contextlib.closing(BitInputStream(open(args.input_file, "rb"))) as bit_in, \
            contextlib.closing(BitOutputStream(open(args.output_file, "wb"))) as bit_out:
        bit = bit_in.read_bit()
        while bit > -1:
            bit_out.write_bit(random_swap(bit, args.p))
            bit = bit_in.read_bit()


if __name__ == "__main__":
    noise()
