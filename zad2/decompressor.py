"""Decompressor of arithmetic encoding."""
import contextlib
import argparse

from frequency_table import FlatFrequencyTable, SimpleFrequencyTable
from arithmetic_coding import ArithmeticDecoder
from inout_bits import BitInputStream


def parse_arguments():
    """Handle program arguments."""
    argparser = argparse.ArgumentParser(
        description='Dekompresja - Adaptacyjne kodowanie arytmetyczne ze skalowaniem')

    argparser.add_argument(
        "input_file",
        help='Plik do dekompresowania.'
    )

    argparser.add_argument(
        "output_file",
        help='Nazwa zdekompresowanego pliku.'
    )

    return argparser.parse_args()


def decompress(bit_input, output):
    """Perform decompression using arithmetic decoding."""
    initfreqs = FlatFrequencyTable(257)
    freq_tab = SimpleFrequencyTable(initfreqs)
    decoder = ArithmeticDecoder(32, bit_input)
    while True:
        sym = decoder.read(freq_tab)
        if sym == 256:
            break
        output.write(bytes((sym,)))
        freq_tab.increment(sym)


def main():
    """Perform decompression of input file to output file."""
    args = parse_arguments()
    with open(args.output_file, "wb") as output, \
            contextlib.closing(
                    BitInputStream(open(args.input_file, "rb"))) as input:
        decompress(input, output)


if __name__ == "__main__":
    main()
