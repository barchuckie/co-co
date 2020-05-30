import argparse

from tga import TGAReader, write_tga_pixel_vector
from encoding import BandEncoder
from decoding import BandDecoder
from inout_bits import CompressFileWriter, CompressFileReader


def parse_arguments():
    """
    Handle and parse program arguments.

    Returns:
        argparse.Namespace: namespace with 3 parsed arguments:
            - input_file -- file to compress in TGA format
            - output_file -- compressed result file
            - quantizer_bits -- number of bits of quantizer
    """
    arg_parser = argparse.ArgumentParser(description='TGA compressor')

    arg_parser.add_argument(
        'input_file',
        help='Plik do kompresji w formacie TGA'
    )

    arg_parser.add_argument(
        'output_file',
        help='Wynikowy plik ze skompresowanym obrazkiem'
    )

    arg_parser.add_argument(
        'quantizer_bits',
        help='Liczba bitow kwantyzatora.',
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7]
    )

    return arg_parser.parse_args()


def compress():
    """Compress input file to output file."""
    args = parse_arguments()
    tga_reader = TGAReader(args.input_file)
    encoder = BandEncoder(tga_reader.pixel_map, args.quantizer_bits)
    encoder.encode()
    file_writer = CompressFileWriter(
        args.output_file,
        tga_reader.header['height'],
        tga_reader.header['width'],
        args.quantizer_bits
    )
    file_writer.write(
        encoder.high_quantizer,
        encoder.high_encoded_sequence,
        encoder.low_quantizer,
        encoder.low_encoded_sequence
    )


if __name__ == "__main__":
    compress()
