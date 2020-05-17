"""Distances module.

It contains all functions for calculation of distances between colors and blocks.
"""
def taxicab_norm(vector):
    """Calculate taxicab (manhattan) norm of the vector."""
    return sum(abs(vector))


def get_distance(x, r):
    """Calculate distance between x and r blocks of colors.
    
    Distance is the sum of the distances between colors on the same position. 
    Colors are tuples.
    """
    return sum(taxicab_norm(x - r))


def get_closest_vector(vector, codebook, m=-1):
    """Find closest entry from the codebook to the vector.
    
    Find a proper entry and return its index (i) and distance (d) from the vector as tuple: (d, i)."""
    if m == -1:
        m = len(codebook)

    return min(map(lambda c: (get_distance(vector, c[1]), c[0]), enumerate(codebook[:m])))
