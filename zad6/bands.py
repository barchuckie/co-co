from dataclasses import dataclass

import numpy as np

from pixels import Pixel, PixelDifference, PixelMap


def get_low_band(current, previous):
    """
    Calculate low band filter as a mean of two elements.

    Args:
        current (Pixel): current element
        previous (Pixel): previous element

    Returns:
        Pixel: pixel representing band
    """
    return Pixel(
        mean_uint8(current.red, previous.red),
        mean_uint8(current.green, previous.green),
        mean_uint8(current.blue, previous.blue)
    )


def get_high_band(current, previous):
    """
    Calculate high band filter as a deviation of two elements.

    Args:
        current (Pixel): current element
        previous (Pixel): previous element

    Returns:
        PixelDifference: pixel representing band
    """
    return PixelDifference(
        deviation(current.red, previous.red),
        deviation(current.green, previous.green),
        deviation(current.blue, previous.blue)
    )


def mean_uint8(current, previous):
    return np.uint8(((np.int(current) + np.int(previous)) // 2) % 256)


def deviation(current, previous):
    return (current - previous) // 2


def split_bands(pixel_map):
    """
    Split pixel table into two bands.

    Args:
        pixel_map (PixelMap): table of pixels to split into bands

    Returns:
        np.ndarray[BandSplit]: array containing BandSplit with low and high split
    """
    bands = np.empty(pixel_map.size // 2, dtype=BandSplit)
    pixel_input = pixel_map.pixels.flatten()

    for i in range(0, bands.size):
        bands[i] = BandSplit(
            low=get_low_band(pixel_input[i * 2 + 1], pixel_input[i * 2]),
            high=get_high_band(pixel_input[i * 2 + 1], pixel_input[i * 2])
        )

    return bands


@dataclass
class BandSplit:
    low: Pixel
    high: PixelDifference
