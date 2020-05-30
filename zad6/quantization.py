import random
from dataclasses import dataclass

import numpy as np

from distortion import unit_error


DEFAULT_EPS = 1e-7
MAX_ITERATIONS = 256


@dataclass
class Partition:
    red: int = 0
    green: int = 0
    blue: int = 0
    total_error: float = .0
    count: int = 0


def get_error(partitions):
    return sum([partition.total_error for partition in partitions])


class Quantization:
    def __init__(self, input_sequence):
        self.input_sequence = input_sequence

    def initialize_quantizer(self, size):
        return np.array([random.choice(self.input_sequence) for _ in range(size)])

    def get_partition_mean(self, partition):
        if partition.count == 0:
            new_partition = random.choice(self.input_sequence)
            return new_partition.red, new_partition.green, new_partition.blue
        return partition.red//partition.count, partition.green//partition.count, partition.blue//partition.count

    def generate_new_quantizer(self, quantizer, partitions):
        for i, q in enumerate(quantizer):
            q.red, q.green, q.blue = self.get_partition_mean(partitions[i])

    def create_nonuniform_quantizer(self, quantizer_size, eps=DEFAULT_EPS):
        quantizer = self.initialize_quantizer(quantizer_size)
        partitions = self.get_partitions(quantizer)
        previous_error = get_error(partitions)

        for _ in range(MAX_ITERATIONS):
            self.generate_new_quantizer(quantizer, partitions)
            partitions = self.get_partitions(quantizer)

            error = get_error(partitions)
            change = (previous_error - error) / previous_error

            if abs(change) < eps or error == 0:
                break

            previous_error = error

        return quantizer

    def get_partitions(self, quantizer):
        partitions = np.array([Partition() for _ in range(quantizer.size)], dtype=Partition)

        for element in self.input_sequence:
            best_idx = best_fit_idx(quantizer, element)
            partition = partitions[best_idx]
            partition.red += element.red
            partition.green += element.green
            partition.blue += element.blue
            partition.total_error += unit_error(element, quantizer[best_idx])
            partition.count += 1

        return partitions


def best_fit_element(quantizer, original_pixel):
    return quantizer[best_fit_idx(quantizer, original_pixel)]


def best_fit_idx(quantizer, original_pixel):
    return min([(get_distance(original_pixel, x), i) for i, x in enumerate(quantizer)])[1]


def get_distance(original_pixel, candidate_pixel):
    d_red = abs(int(original_pixel.red) - int(candidate_pixel.red))
    d_green = abs(int(original_pixel.green) - int(candidate_pixel.green))
    d_blue = abs(int(original_pixel.blue) - int(candidate_pixel.blue))

    return d_red + d_green + d_blue


def assign_quantizers_elements(quantizer, original_sequence):
    return np.array([best_fit_element(quantizer, e) for e in original_sequence])


def assign_quantizers_indexes(quantizer, original_sequence):
    return np.array([best_fit_idx(quantizer, e) for e in original_sequence])
