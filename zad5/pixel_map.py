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


class PixelMap:
    """Map wrapper of the image pixels.
    
    Pixel Map stores pixels of the image.
    """

    def __init__(self, height, width):
        """Initialize new instance of Pixel Map with a given height and width of an image."""
        self.width = width
        self.height = height
        self.pixels = np.empty((height, width), dtype=Pixel)

    def __getitem__(self, idx):
        """Return pixel on the given idx coordinates.
        
        -- idx - tuple of (row, col)
        """
        row, col = idx
        return self.pixels[row, col]

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
