"""Implementation of JPEG-LS predictors.

Let N, W, NW, X be following:

 NW| N |
---|---|
 W | X |

where X is actual value.

There are 8 such predictor standards (X'):
-- N
-- W
-- NW
-- N + W - NW
-- N + (W - NW)/2
-- W + (N - NW)/2
-- (N + W)/2
-- New standard

Prediction is calculated by: X - X'.
"""


from pixel_map import PixelMap
from abc import ABC, abstractmethod



def get_red(color):
    return color.red


def get_green(color):
    return color.green


def get_blue(color):
    return color.blue


class Predictor(ABC):
    """Abstract class for prediction calculation of the whole pixel map."""

    def __init__(self, pixel_map):
        """Initialize new predictor instance with actual pixel map and build codes.
        
        -- pixel_map - original pixel map used for calculation
        """
        self.original_pixel_map = pixel_map
        self.codes = PixelMap(pixel_map.height, pixel_map.width)
        self.build_codes()

    def build_codes(self):
        """Build pixel map of predictions using methods for calculating each color ingredient."""
        for row in range(self.codes.height):
            for col in range(self.codes.width):
                self.codes.new_pixel(
                    row, col, 
                    self.get_prediction(row, col, get_red),
                    self.get_prediction(row, col, get_green),
                    self.get_prediction(row, col, get_blue)
                )

    @abstractmethod
    def get_prediction(self, row, column, color_extractor):
        """Calculate and return prediction on the specific coordinates.
        
        -- row - y-coordinate
        -- column - x-coordinate
        -- color_extractor -- function to extract specific color ingredient value
        """
        pass

    def n(self, row, col):
        """Return pixel on the north of the considered one."""
        return self.original_pixel_map[row-1, col]

    def w(self, row, col):
        """Return pixel on the west of the considered one."""
        return self.original_pixel_map[row, col-1]

    def nw(self, row, col):
        """Return pixel on the north-west of the considered one."""
        return self.original_pixel_map[row-1, col-1]


class PredictorN(Predictor):
    def get_prediction(self, row, column, color_extractor):
        return color_extractor(self.original_pixel_map[row, column]) - color_extractor(self.n(row, column))


class PredictorW(Predictor):
    def get_prediction(self, row, column, color_extractor):
        return color_extractor(self.original_pixel_map[row, column]) - color_extractor(self.w(row, column))


class PredictorNW(Predictor):
    def get_prediction(self, row, column, color_extractor):
        return color_extractor(self.original_pixel_map[row, column]) - color_extractor(self.nw(row, column))


class PredictorNAddWSubNW(Predictor):
    def get_prediction(self, row, column, color_extractor):
        return color_extractor(self.original_pixel_map[row, column]) - (color_extractor(self.n(row, column)) + color_extractor(self.w(row, column)) - color_extractor(self.nw(row, column)))


class PredictorNAddHalfWSubNW(Predictor):
    def get_prediction(self, row, column, color_extractor):
        return color_extractor(self.original_pixel_map[row, column]) - (color_extractor(self.n(row, column)) + (color_extractor(self.w(row, column)) - color_extractor(self.nw(row, column)))//2)


class PredictorWAddHalfNSubNW(Predictor):
    def get_prediction(self, row, column, color_extractor):
        return color_extractor(self.original_pixel_map[row, column]) - (color_extractor(self.w(row, column)) + (color_extractor(self.n(row, column)) - color_extractor(self.nw(row, column)))//2)


class PredictorHalfNAddW(Predictor):
    def get_prediction(self, row, column, color_extractor):
        return color_extractor(self.original_pixel_map[row, column]) - (color_extractor(self.w(row, column)) + color_extractor(self.n(row, column)))//2


class PredictorNew(Predictor):
    def get_prediction(self, row, column, color_extractor):
        n = color_extractor(self.n(row, column))
        w = color_extractor(self.w(row, column))
        nw = color_extractor(self.nw(row, column))
        m = max(w, n)
        if nw >= m:
            return m
        m = min(w, n)
        if nw <= m:
            return m
        return w + n - nw
