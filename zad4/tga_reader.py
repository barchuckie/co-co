"""Module for reading TGA image files."""


from pixel_map import PixelMap


def extract_header(file):
    """Read header of the file and return dictionary with specific header values.
    
    -- file - opened file stream to read from
    """
    header = {}
    header['id-length'] = file.read(1)[0]
    header['color-map-type'] = file.read(1)[0]
    header['image-type'] = file.read(1)[0]
    header['color-map-first-entry-index'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['color-map-length'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['color-map-entry-size'] = file.read(1)[0]
    header['x-origin'] = file.read(1)[0] << 8 + file.read(1)[0]
    header['y-origin'] = file.read(1)[0] << 8 + file.read(1)[0]
    header['width'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['height'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['pixel-depth'] = file.read(1)[0]
    header['descriptor'] = file.read(1)[0]
    return header


def read_image(file, height, width):
    """Read image from the file.

    Create PixelMap and store there read pixels from the file stream.

    -- file - opende file stream to read from
    -- height - height of the image in pixels
    -- width - width of the image in pixels
    """
    pixel_map = PixelMap(height, width)
    for row in range(height-1, -1, -1):
        for col in range(width):
            blue = file.read(1)[0]
            green = file.read(1)[0]
            red = file.read(1)[0]
            pixel_map.new_pixel(row, col, red, green, blue)
    
    return pixel_map


class TGAReader:
    """Reader of TGA files."""

    def __init__(self, filename):
        """Initialize new instance of TGA reader and read from file.

        -- filename - nam of the file to read
        """
        self.filename = filename
        self.header, self.pixel_map = self.read_file()

    def read_file(self):
        """Read TGA file and return its header and image as PixelMap."""
        with open(self.filename, 'rb') as file:
            header = extract_header(file)
            assert header['id-length'] == header['color-map-length'] == 0, "ID or Color Map length > 0"
            assert header['pixel-depth'] == 24, "Pixel depth != 24 (3 bytes)"
            pixel_map = read_image(file, header['height'], header['width'])
        return header, pixel_map
