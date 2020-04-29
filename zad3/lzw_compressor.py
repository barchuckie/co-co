"""Program to compress with LZW algorithm."""
import argparse
import contextlib

import encoding
from inout_bits import BitOutputStream
from lzw import LZWEncoder


def parse_arguments():
    """Handle program arguments."""
    argparser = argparse.ArgumentParser(
        description='LZW')

    argparser.add_argument(
        "input_file",
        help='Plik do skompresowania.'
    )

    argparser.add_argument(
        "output_file",
        help='Nazwa skompresowanego pliku.'
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
        return encoding.Gamma
    if arg == 'delta':
        return encoding.Delta
    if arg == 'fib':
        return encoding.Fibonacci
    return encoding.Omega


def print_compression_data(input_filename, coding, encoder, bit_output):
    """Print information about compression data.
    
    -- input_filename - input filename
    -- coding - name of the chosen coding
    -- encoder - LZW encoder used to encoding
    -- bit_output - output bit stream
    """
    print('Input file:', input_filename)
    print('Coding with:', coding)
    print('Input file size:', encoder.get_totalbytes(), 'bytes')
    print('Compressed file size:', bit_output.get_totalbytes(), 'bytes')
    print('Compression ratio:', encoder.get_totalbytes()/bit_output.get_totalbytes())
    print('Input file entropy:', encoder.get_input_entropy())
    print('Compressed file entropy:', bit_output.get_output_entropy())


def main():
    """Perform compression of the input file."""
    args = parse_arguments()
    with open(args.input_file, 'rb') as input_file, contextlib.closing(
                BitOutputStream(open(args.output_file, "wb"))) as bit_out:
        dictionary = [bytes((x,)) for x in range(256)]
        dictionary.append(None)  # EOF
        enc = LZWEncoder(dictionary, input_file, get_coding(args.c)(bit_out))
        enc.encode()
        print_compression_data(args.input_file, args.c, enc, bit_out)


if __name__ == '__main__':
    main()
