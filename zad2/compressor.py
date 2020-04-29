"""Compressor of arithmetic encoding."""
import argparse
import contextlib

from frequency_table import FlatFrequencyTable, SimpleFrequencyTable
from arithmetic_coding import ArithmeticEncoder
from inout_bits import BitOutputStream


def parse_arguments():
    """Handle program arguments."""
    argparser = argparse.ArgumentParser(
        description='Kompresja - Adaptacyjne kodowanie arytmetyczne ze skalowaniem')

    argparser.add_argument(
        "input_file",
        help='Plik do skompresowania.'
    )

    argparser.add_argument(
        "output_file",
        help='Nazwa skompresowanego pliku.'
    )

    return argparser.parse_args()


def compress(input, bit_out):
    """Perform compression using arithmetic decoding."""
    initfreqs = FlatFrequencyTable(257)
    freqs = SimpleFrequencyTable(initfreqs)
    enc = ArithmeticEncoder(32, bit_out)
    sym = input.read(1)

    while sym:
        sym = sym[0]
        enc.write(freqs, sym)
        freqs.increment(sym)
        sym = input.read(1)

    enc.write(freqs, 256)
    enc.finish()

    print_result(freqs, bit_out)


def print_result(freqs, bit_out):
    """Print data about compression"""
    print('Entropy:', freqs.entropy())
    print('Input file size:', freqs.get_in_size(), 'bytes')
    print('Compressed file size:', bit_out.get_totalbytes(), 'bytes')
    print('Compression ratio:', freqs.get_in_size()/bit_out.get_totalbytes())
    print('Average code length:', bit_out.get_totalbytes()*8/freqs.get_in_size())


def main():
    """Perform compression of input file to output file."""
    args = parse_arguments()
    with open(args.input_file, "rb") as input, \
            contextlib.closing(
                    BitOutputStream(open(args.output_file, "wb"))) as output:
        print('Input file:', args.input_file)
        compress(input, output)


if __name__ == "__main__":
    main()
