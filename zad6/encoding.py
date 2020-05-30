import numpy as np

from bands import split_bands, BandSplit
from quantization import Quantization, assign_quantizers_indexes
from differential_coding import DifferentialEncoder


class BandEncoder:
    def __init__(self, pixel_table, quantizer_bits):
        self.pixel_table = pixel_table
        self.low_quantizer = None
        self.high_quantizer = None
        self.low_encoded_sequence = None
        self.high_encoded_sequence = None
        self.quantizer_bits = quantizer_bits
        self.quantizer_size = 1 << quantizer_bits
        self.height, self.width = pixel_table.pixels.shape

    def encode(self):
        bands = split_bands(self.pixel_table)
        self.encode_high_band(bands)
        self.encode_low_band(bands)

    def encode_high_band(self, bands):
        high_bands = np.array([band.high for band in bands], dtype=BandSplit)
        high_quantization = Quantization(high_bands)
        self.high_quantizer = high_quantization.create_nonuniform_quantizer(self.quantizer_size)
        self.high_encoded_sequence = assign_quantizers_indexes(self.high_quantizer, high_bands)

    def encode_low_band(self, bands):
        low_bands = np.array([band.low for band in bands], dtype=BandSplit)
        low_encoder = DifferentialEncoder(low_bands)
        self.low_quantizer, self.low_encoded_sequence = low_encoder.encode(self.quantizer_size)
