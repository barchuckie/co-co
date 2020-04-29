"""Package for calculating entropy of image pixel colors.

There is possibility of calculating full RGB colors and each of their ingredients, too.
"""
import math


def get_red(value):
    """Extract RED ingredient from the RGB color value."""
    return value >> 16


def get_green(value):
    """Extract GREEN ingredient from the RGB color value."""
    return value >> 8 & 255


def get_blue(value):
    """Extract BLUE ingredient from the RGB color value."""
    return value & 255


def update_counter(counter, value):
    """Increment the counter of specific value.
    
    Counter is incremented if the value was already read. Otherwise new counter is created."""
    if value not in counter.keys():
        counter[value] = 1
    else:
        counter[value] += 1


class ColorEntropy:
    """Wrapper of all color entropies: full color, red, green, blue."""

    def __init__(self):
        """Initialize all color entropies."""
        self.color_entropy = Entropy()
        self.red_entropy = Entropy()
        self.green_entropy = Entropy()
        self.blue_entropy = Entropy()

    def new_value(self, value):
        """Update all entropies with value."""
        self.color_entropy.new_value(value)
        self.red_entropy.new_value(get_red(value))
        self.green_entropy.new_value(get_green(value))
        self.blue_entropy.new_value(get_blue(value))

    def get_color(self):
        """Return entropy of full colors."""
        return self.color_entropy.get()

    def get_red(self):
        """Return entropy of red ingredient."""
        return self.red_entropy.get()

    def get_green(self):
        """Return entropy of green ingredient."""
        return self.green_entropy.get()

    def get_blue(self):
        """Return entropy of blue ingredient."""
        return self.blue_entropy.get()


class Entropy:
    """Class for calculating entropy."""

    def __init__(self):
        """Inititize new entropy calculator instance with empty value dictionary."""
        self.total = 0
        self.value_counter = {}

    def new_value(self, value):
        """Update entropy calulation with value occurence."""
        self.total += 1
        update_counter(self.value_counter, value)

    def get(self):
        """Calculate entropy of inserted values."""
        return sum([x*(math.log(self.total,2)-math.log(x,2)) for x in self.value_counter.values()])/self.total
        
        
