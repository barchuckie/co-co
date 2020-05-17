"""
Codebook creation module. 

Contains CodebookFactory class and all necessary functions for codebook creation.
"""
import numpy as np
import random
import time
from dataclasses import dataclass


from pixel_map import Pixel
from distances import get_closest_vector


@dataclass
class Partition:
    total_vector: np.ndarray
    total_distance: int = 0
    count: int = 0


class CodebookFactory:
    """Creates codebook for vector quantization using LBG algorithm."""

    def __init__(self, pixel_table, perturbation_vector, block_side, epsilon):
        """Initialize new instance with given properties. 
        
        Assign values to class properties, calculate vector length as squared block_side 
        and extract blocks from the pixel_table.
        
        -- pixel_table - PixelMap table containing picture pixels
        -- perturbation_vector - vector to perturbate codebook entries with
        -- block_side - length of the blocks sides of the picture
        -- epsilon - limit value to finish LBG algorithm
        """
        self.pixel_map = pixel_table
        self.perturbation_vector = perturbation_vector
        self.block_side = block_side
        self.vector_size = block_side**2
        self.blocks = pixel_table.get_blocks(self.block_side)
        self.epsilon = epsilon

    def get_first_point(self):
        """Return very first point in the splitting method creation of codebook."""
        return self.get_average_color(self.blocks)

    def get_average_color(self, blocks):
        """Calculate and return average color block from the partition of blocks.
        
        -- blocks - set of blocks
        """
        total = np.array([(0,0,0) for _ in range(self.vector_size)])
        count = 0
                
        for vector in blocks:
            total += vector
            count += 1

        if count == 0:
            return random.choice(self.blocks)

        return total//count

    def get_partition_mean(self, partition):
        if partition.count == 0:
            return random.choice(self.blocks)
        return partition.total_vector//partition.count

    def calculate_new_codebook(self, codebook, partitions):
        """Calculate codebook from the partitions.
        
        Codebook length is equal to the number of partitions.
        -- partitions - partitions used for codebook calculation
        """
        for i in range(len(partitions)):
            codebook[i] = self.get_partition_mean(partitions[i])

    def create_codebook(self, iterations):
        """Create new nodebook using blocks from the pixel table.
        
        Codebook's length is 2**iterations since it is doubled every iteration.
        -- iterations - number of iterations to perform
        """
        codebook = np.empty(2**iterations, dtype=object)
        codebook[0] = self.get_first_point()

        for it in range(iterations):
            length = 2**it
            for i in range(length):
                codebook[length + i] = (codebook[i]+self.perturbation_vector) % 256
            codebook = self.lbg(codebook, length*2)

        return codebook

    def lbg(self, codebook, codebook_size):
        """Perform LBG algorithm.
        
        Linde-Buz-Gray algorithm is used for codebook generation using specific learning set, 
        which is pixel table of the picture.
        -- codebook - initial codebook used in algorithm
        -- codebook_size - number of elements in codebook to consider
        """
        prev_distortion = float('inf')

        while True:
            partitions = self.generate_partitions(codebook, codebook_size)
            distortion = calculate_distortion(partitions)
            change = (prev_distortion - distortion)/distortion
            
            if change < self.epsilon:
                return codebook

            self.calculate_new_codebook(codebook, partitions)
            prev_distortion = distortion


    def generate_partitions(self, codebook, codebook_size):
        """Generate partitions of the blocks set.
        
        Paritions generation is performed by finding closest blocks for a given entry from the codebook.
        -- codebook - set of vectors used for blocks partitioning
        -- blocks - set to be partitioned
        -- codebook_size - number of elements in codebook to consider
        """
        partitions = np.array(
            [
                Partition(
                    np.array([(0,0,0) for _ in range(self.vector_size)], dtype=int), 
                    0, 
                    0
                ) for _ in range(codebook_size)
            ], 
            dtype=Partition
        )

        for block in self.blocks:
            min_val, min_idx = get_closest_vector(block, codebook, codebook_size)
            partition = partitions[min_idx]
            partition.total_vector += block
            partition.total_distance += min_val
            partition.count += 1

        return partitions

def calculate_distortion(partitions):
    """Calculate total distortion of partition set.
    
    Total distortion is a mean of all partition distortions. Partition distortion is a mean of its elements.
    -- partitions - set of blocks partitions
    """
    s = 0
    for partition in partitions:
        if partition.count > 0:
            s += partition.total_distance/partition.count
    return s/len(partitions)
