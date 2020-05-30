import argparse

from decoding import BandDecoder
from inout_bits import CompressFileReader
from tga import write_tga_pixel_vector, get_default_header, get_default_footer


def parse_arguments():
    """
    Handle and parse program arguments.

    Returns:
        argparse.Namespace: namespace with 3 parsed arguments:
            - input_file -- compressed input file
            - output_file -- decompressed result file in TGA format
    """
    arg_parser = argparse.ArgumentParser(description='TGA compressor')

    arg_parser.add_argument(
        'input_file',
        help='Wejściowy plik do dekompresji'
    )

    arg_parser.add_argument(
        'output_file',
        help='Wynikowy plik ze zdeskompresowanym obrazkiem w formacie TGA'
    )

    return arg_parser.parse_args()


def decompress():
    """Decompress input file to output file."""
    args = parse_arguments()
    file_reader = CompressFileReader(args.input_file)
    file_reader.read()
    decoder = BandDecoder(file_reader.high_quantizer, file_reader.low_quantizer)
    decoder.decode(file_reader.high_idx_sequence, file_reader.low_idx_sequence)
    write_tga_pixel_vector(
        args.output_file,
        get_default_header(file_reader.width, file_reader.height),
        decoder.decoded_sequence,
        get_default_footer()
    )


if __name__ == "__main__":
    decompress()
