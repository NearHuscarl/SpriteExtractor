"""
Color helper functions. Copy from https://github.com/dylanaraps/pywal/blob/master/pywal/util.py
"""


def rgba_to_hex(color):
    """ Convert an rgb color to hex """
    return "#%02x%02x%02x%02x" % (*color,)


def hex_to_rgba(color):
    """ Convert a hex color to rgb """
    return tuple(bytes.fromhex(color.strip("#")))
