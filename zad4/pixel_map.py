"""Implemenation of pixel map.

It is used for storing colors of image pixels and calculating their entropy.
"""
import numpy as np
from dataclasses import dataclass
from entropy import ColorEntropy


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


class PixelMap:
    """Map wrapper of the image pixels.
    
    Pixel Map stores pixels of the image and calculates entropy of the data.
    """

    def __init__(self, height, width):
        """Initialize new instance of Pixel Map with a given height and width of an image."""
        self.width = width
        self.height = height
        self.pixels = np.empty((height, width), dtype=Pixel)
        self.entropy = ColorEntropy()

    def __getitem__(self, idx):
        """Return pixel on the given idx coordinates.

        If given coordinates are out of map range, return black pixel.
        -- idx - tuple of (row, col)
        """
        row, col = idx
        if -1 < row < self.height or -1 < col < self.width:
            return self.pixels[row, col]
        return Pixel(0, 0, 0)

    def new_pixel(self, row, col, red, blue, green):
        """Assign new pixel to (row, col) with given RGB color ingredients.
        
        -- row - pixel row, y-coordinate
        -- col - pixel col, x-coordinates
        -- red - red ingredient
        -- green - green ingredient
        -- blue - blue ingredient
        """
        assert row < self.height and col < self.width, f"Out of range: [{row}, {col}]"
        pixel = Pixel(red % 256, blue % 256, green % 256)
        self.pixels[row, col] = pixel
        self.entropy.new_value(pixel.color)
        
    @property
    def size(self):
        """Size of the pixel map, which is height * width."""
        return self.height * self.width

    def __str__(self):
        return str(self.pixels)
