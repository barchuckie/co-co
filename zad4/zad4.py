import argparse
import math
from tga_reader import TGAReader
from predictors import *


def parse_arguments():
    """Handle program arguments."""
    arg_parser = argparse.ArgumentParser('TGA to JPEG_LS codes')

    arg_parser.add_argument(
        'input_file',
        help='Plik do kompresowania'
    )

    return arg_parser.parse_args()


def print_results(color, red, green, blue):
    """Print values of the whole RGB color and its values."""
    print('Color:', color)
    print('Red:', red)
    print('Green:', green)
    print('Blue:', blue)


def print_entropies(entropy):
    """Print all color entropies."""
    print_results(entropy.get_color(), entropy.get_red(), entropy.get_green(), entropy.get_blue())
    

def calculate_predictors(original_pixel_map):
    """Calculate entropies of all predictor standards and return dictionary of them."""
    entropies = {}
    entropies['W'] = PredictorW(original_pixel_map).codes.entropy
    entropies['N'] = PredictorN(original_pixel_map).codes.entropy
    entropies['NW'] = PredictorNW(original_pixel_map).codes.entropy
    entropies['N+W-NW'] = PredictorNAddWSubNW(original_pixel_map).codes.entropy
    entropies['N+(W-NW)/2'] = PredictorNAddHalfWSubNW(original_pixel_map).codes.entropy
    entropies['W+(N-NW)/2'] = PredictorWAddHalfNSubNW(original_pixel_map).codes.entropy
    entropies['(N+W)/2'] = PredictorHalfNAddW(original_pixel_map).codes.entropy
    entropies['NEW'] = PredictorNew(original_pixel_map).codes.entropy
    return entropies


def encode(pixel_map):
    """Encode pixels in the pixel map, look for the most optimal and print results."""
    entropies = calculate_predictors(pixel_map)
    entropies['ORIGINAL'] = pixel_map.entropy

    min_color = ('ORIGINAL', pixel_map.entropy.get_color())
    min_red = ('ORIGINAL', pixel_map.entropy.get_red())
    min_green = ('ORIGINAL', pixel_map.entropy.get_green())
    min_blue = ('ORIGINAL', pixel_map.entropy.get_blue())

    for key, entropy in entropies.items():
        print(key)
        print_entropies(entropy)

        if entropy.get_color() < min_color[1]:
            min_color = (key, entropy.get_color())
        if entropy.get_red() < min_red[1]:
            min_red = (key, entropy.get_red())
        if entropy.get_green() < min_green[1]:
            min_green = (key, entropy.get_green())
        if entropy.get_blue() < min_blue[1]:
            min_blue = (key, entropy.get_blue())

    print('BEST')
    print_results(min_color[0], min_red[0], min_green[0], min_blue[0])




def main():
    """Read file from the program rguments and perform coding."""
    args = parse_arguments()
    tga_reader = TGAReader(args.input_file)
    encode(tga_reader.pixel_map)


if __name__ == "__main__":
    main()
