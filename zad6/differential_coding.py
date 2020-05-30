from quantization import *
from pixels import get_pixel


class DifferentialEncoder:
    def __init__(self, original_sequence):
        self.original_sequence = original_sequence
        self.data_size = self.original_sequence.size
        self.data_type = type(self.original_sequence[0])

    def encode(self, quantizer_size):
        initial_differential_sequence = self.get_differential_sequence()
        quantization = Quantization(initial_differential_sequence)
        quantizer = quantization.create_nonuniform_quantizer(quantizer_size)
        differential_sequence = np.empty(self.data_size, dtype=self.data_type)
        differential_sequence[0] = self.original_sequence[0]
        quantized_idx_sequence = np.empty(self.data_size, dtype=np.uint8)
        quantized_idx_sequence[0] = best_fit_idx(quantizer, differential_sequence[0])
        encoded_sequence = np.empty(self.data_size, dtype=self.data_type)
        encoded_sequence[0] = quantizer[quantized_idx_sequence[0]]

        for i in range(1, self.data_size):
            differential_sequence[i] = self.original_sequence[i] - encoded_sequence[i - 1]
            quantized_idx_sequence[i] = best_fit_idx(quantizer, differential_sequence[i])
            encoded_sequence[i] = encoded_sequence[i - 1] + quantizer[quantized_idx_sequence[i]]

        return quantizer, quantized_idx_sequence

    def get_differential_sequence(self):
        return np.array([self.original_sequence[0]]
                        + [
                            self.original_sequence[i] - self.original_sequence[i-1]
                            for i in range(1, len(self.original_sequence))
                        ])


class DifferentialDecoder:
    def __init__(self, quantizer):
        self.quantizer = quantizer

    def decode(self, idx_sequence):
        decoded_sequence = np.empty(idx_sequence.shape, dtype=self.quantizer.dtype)
        decoded_sequence[0] = get_pixel(self.quantizer[idx_sequence[0]])

        for i in range(1, idx_sequence.size):
            decoded_sequence[i] = get_pixel(decoded_sequence[i - 1] + self.quantizer[idx_sequence[i]])

        return decoded_sequence
