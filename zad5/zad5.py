import argparse

from tga import TGAReader, write_tga
from vector_quantization import VectorQuantization
from distortion import DistortionCalculator


def parse_arguments():
    """Handle program arguments."""
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
        'color_number_exp',
        help='Liczba kolorów będąca dwójkową potęgą tej liczby.',
        type=int
    )

    return arg_parser.parse_args()


def print_distortions(original_pixel_table, reconstructed_pixel_table):
    dc = DistortionCalculator(original_pixel_table, reconstructed_pixel_table)
    print('MSE:', dc.mse())
    print('SNR:', dc.snr())
    print('SNR(dB):', dc.snr_db())


def quantize():
    """Perfrom quantization."""
    args = parse_arguments()
    tga_reader = TGAReader(args.input_file)
    vq = VectorQuantization(tga_reader.pixel_map, args.color_number_exp)
    reconstructed_pixel_table = vq.perform()

    write_tga(
        args.output_file, 
        tga_reader.header, 
        reconstructed_pixel_table, 
        tga_reader.footer
    )

    print_distortions(tga_reader.pixel_map, reconstructed_pixel_table)


if __name__ == "__main__":
    quantize()
