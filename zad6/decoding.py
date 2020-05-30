import numpy as np

from differential_coding import DifferentialDecoder
from pixels import get_pixel


class BandDecoder:
    def __init__(self, high_quantizer, low_quantizer):
        self.high_quantizer = high_quantizer
        self.low_quantizer = low_quantizer
        self.decoded_sequence = None
        assert high_quantizer.dtype == low_quantizer.dtype

    def decode(self, high_idx_sequence, low_idx_sequence):
        assert high_idx_sequence.size == low_idx_sequence.size
        decoded_high_sequence = np.array([self.high_quantizer[idx] for idx in high_idx_sequence])
        low_decoder = DifferentialDecoder(self.low_quantizer)
        decoded_low_sequence = low_decoder.decode(low_idx_sequence)

        self.decoded_sequence = np.empty(low_idx_sequence.size*2, dtype=self.low_quantizer.dtype)
        for i in range(0, decoded_low_sequence.size):
            self.decoded_sequence[i * 2] = get_pixel(decoded_low_sequence[i] - decoded_high_sequence[i])
            self.decoded_sequence[i * 2 + 1] = decoded_low_sequence[i] + decoded_high_sequence[i]
