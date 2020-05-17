"""Distortion module.

Implementation of the class for calculating distortions: MSE and SNR.
"""
import math


class DistortionCalculator:
    """Calculator of distortions values."""

    def __init__(self, original, reconstructed):
        """Initialize new instance with original and recontructed sets."""
        self.original = original
        self.reconstructed = reconstructed
        self.height = len(self.original.pixels)
        if self.height > 0:
            self.width = len(self.original.pixels[0])
        else:
            self.width = 0

    def mse(self):
        """Calculate MSE.
        
        MSE is Mean Squared Error.
        """
        s = 0
        for row in range(self.height):
            for col in range(self.width):
                o = self.original[row, col]
                r = self.reconstructed[row, col]
                s += (o.red-r.red)**2 + (o.green-r.green)**2 + (o.blue-r.blue)**2
        return s/(self.height*self.width*3)

    def snr(self):
        """Calculate SNR.
        
        SNR is Signal to Noise Ratio.
        """
        s = 0
        for row in self.original.pixels:
            for pixel in row:
                s += pixel.red**2
                s += pixel.green**2
                s += pixel.blue**2

        mse = self.mse()

        if mse == 0:
            return float('inf')

        return (s/(3*self.height*self.width))/mse

    def snr_db(self):
        """Calculate SNR in the dB form."""
        return 10*math.log10(self.snr())
