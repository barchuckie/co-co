import argparse

from tga import TGAReader
from distortion import print_distortions


def parse_arguments():
    """
    Handle and parse program arguments.

    Returns:
        argparse.Namespace: namespace with 3 parsed arguments:
            - original -- original file
            - reconstructed -- reconstructed file
    """
    arg_parser = argparse.ArgumentParser(description='TGA compressor')

    arg_parser.add_argument(
        'original',
        help='Oryginalny plik TGA'
    )

    arg_parser.add_argument(
        'reconstructed',
        help='Plik TGA po odkodowaniu'
    )

    return arg_parser.parse_args()


def compress():
    """Compress input file to output file."""
    args = parse_arguments()
    original = TGAReader(args.original)
    reconstructed = TGAReader(args.reconstructed)
    print_distortions(original.pixel_map, reconstructed.pixel_map)


if __name__ == "__main__":
    compress()
