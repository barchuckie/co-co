import argparse
import contextlib

from inout_bits import BitInputStream, BitOutputStream


def parse_arguments():
    """
    Handle and parse program arguments.

    Returns:
        argparse.Namespace: namespace with 2 parsed arguments:
            - in1 -- one input file
            - in2 -- another input file
    """
    arg_parser = argparse.ArgumentParser(
        description='Porównanie plików'
    )

    arg_parser.add_argument(
        'in1',
        help='Pierwszy plik wejściowy',
    )

    arg_parser.add_argument(
        'in2',
        help='Drugi plik wejściowy'
    )

    return arg_parser.parse_args()


def compare_4bits(bit_in1, bit_in2):
    difference_counter = 0
    bits1 = bit_in1.read_bits(4)
    bits2 = bit_in2.read_bits(4)
    while True:
        if bits1 < 0:
            while bits2 > -1:
                difference_counter += 1
                bits2 = bit_in2.read_bits(4)
            break
        if bits2 < 0:
            while bits1 > -1:
                difference_counter += 1
                bits1 = bit_in1.read_bits(4)
            break
        if bits1 != bits2:
            difference_counter += 1
        bits1 = bit_in1.read_bits(4)
        bits2 = bit_in2.read_bits(4)
    return difference_counter


def check():
    """Compare two files with each other."""
    args = parse_arguments()
    with contextlib.closing(BitInputStream(open(args.in1, "rb"))) as bit_in1, \
            contextlib.closing(BitInputStream(open(args.in2, "rb"))) as bit_in2:
        different_blocks = compare_4bits(bit_in1, bit_in2)
    print("Liczba różnych bloków 4-bitowych:", different_blocks)


if __name__ == "__main__":
    check()
