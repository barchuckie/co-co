"""Program to decompress with LZW algorithm."""
import argparse
import contextlib

import decoding
from inout_bits import BitInputStream
from lzw import LZWDecoder


def parse_arguments():
    """Handle program arguments."""
    argparser = argparse.ArgumentParser(
        description='LZW')

    argparser.add_argument(
        "input_file",
        help='Plik do dekompresji.'
    )

    argparser.add_argument(
        "output_file",
        help='Nazwa zdekompresowanego pliku.'
    )

    argparser.add_argument(
        '-c',
        choices=['gamma', 'delta', 'omega', 'fib'],
        default='omega',
        help='Wybór kodowania skompresowanego pliku (default gamma)'
    )

    return argparser.parse_args()


def get_coding(arg):
    """Get proper class according to an argument."""
    if arg == 'gamma':
        return decoding.Gamma
    if arg == 'delta':
        return decoding.Delta
    if arg == 'fib':
        return decoding.Fibonacci
    return decoding.Omega


def main():
    """Perform compression of the input file."""
    args = parse_arguments()
    with open(args.output_file, 'wb') as output_file, contextlib.closing(
                BitInputStream(open(args.input_file, "rb"))) as input:
        dictionary = [bytes((x,)) for x in range(256)]
        dictionary.append(None)  # EOF
        dec = LZWDecoder(dictionary, output_file, get_coding(args.c)(input))
        dec.decode()


if __name__ == '__main__':
    main()
