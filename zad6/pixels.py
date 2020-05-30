"""Implemenation of pixel map.

It is used for storing colors of image pixels and calculating their entropy.
"""
import numpy as np
from dataclasses import dataclass


@dataclass
class Pixel:
    """Data class representing single pixel of the image.
    
    Pixel consist of three RGB colors.
    """
    red: np.uint8
    green: np.uint8
    blue: np.uint8

    @property
    def color(self):
        """Whole color value of the pixel."""
        return (self.red << 16) + (self.green << 8) + self.blue

    def __sub__(self, other):
        return PixelDifference(
            clamp(np.int16(self.red) - np.int16(other.red), -32768, 32767),
            clamp(np.int16(self.green) - np.int16(other.green), -32768, 32767),
            clamp(np.int16(self.blue) - np.int16(other.blue), -32768, 32767)
        )

    def __add__(self, other):
        return Pixel(
            clamp(self.red + other.red, 0, 255),
            clamp(self.green + other.green, 0, 255),
            clamp(self.blue + other.blue, 0, 255)
        )


def get_pixel(pixel_difference):
    return Pixel(
        clamp(pixel_difference.red, 0, 255),
        clamp(pixel_difference.green, 0, 255),
        clamp(pixel_difference.blue, 0, 255),
    )


def clamp(number, minimum, maximum):
    if number > maximum:
        return maximum
    if number < minimum:
        return minimum
    return number


@dataclass
class PixelDifference:
    """Data class representing difference between two pixels.

    PixelDifference consist of three RGB color values. However they can be bigger than 255 and negative.
    """
    red: np.int16
    green: np.int16
    blue: np.int16

    def __add__(self, other):
        return PixelDifference(
            self.red + other.red,
            self.green + other.green,
            self.blue + other.blue
        )

    def __sub__(self, other):
        return PixelDifference(
            self.red - other.red,
            self.green - other.green,
            self.blue - other.blue
        )


class PixelMap:
    """Map wrapper of the image pixels.
    
    Pixel Map stores pixels of the image.
    """

    def __init__(self, height, width):
        """
        Initialize new instance of Pixel Map with a given height and width of an image.

        Args:
            height (int): height of the pixel table to create
            width (int): width of the pixel table to create
        """
        self.width = width
        self.height = height
        self.pixels = np.empty((height, width), dtype=Pixel)

    def __getitem__(self, idx):
        """Return pixel on the given idx coordinates.
        
        -- idx - tuple of (row, col)
        """
        row, col = idx
        return self.pixels[row, col]

    @classmethod
    def from_vector(cls, vector, height, width):
        assert vector.size == height * width
        new_pixel_map = cls(height, width)
        for row in range(height):
            for col in range(width):
                pixel = vector[row*width + col]
                new_pixel_map.new_pixel(row, col, pixel.red, pixel.green, pixel.blue)

        return new_pixel_map

    def new_pixel(self, row, col, red, green, blue):
        """Assign new pixel to (row, col) with given RGB color ingredients.
        
        -- row - pixel row, y-coordinate
        -- col - pixel col, x-coordinates
        -- red - red ingredient
        -- green - green ingredient
        -- blue - blue ingredient
        """
        assert row < self.height and col < self.width, f"Out of range: [{row}, {col}]"
        pixel = Pixel(red % 256, green % 256, blue % 256)
        self.pixels[row, col] = pixel
        
    @property
    def size(self):
        """Size of the pixel map, which is height * width."""
        return self.height * self.width

    def __str__(self):
        return str(self.pixels)

    def get_blocks(self, block_side):
        """Divide pixel table into blocks and return them as vectors.
        
        Blocks are squared size with side length of block_side. They are flattened into vectors.
        -- block_side - the length of blocks sides"""
        blocks = []
        for row_idx in range(0, self.height, block_side):
            for col_idx in range(0, self.width, block_side):
                blocks.append([(pixel.red, pixel.green, pixel.blue) for pixel in np.ndarray.flatten(self.pixels[row_idx:row_idx+block_side, col_idx:col_idx+block_side])])
        return np.array(blocks, dtype=np.uint8)
