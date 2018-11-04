"""
Image-related utilities
"""

from PIL import Image, ImageChops
from boundingbox import BoundingBox


def _get_bbox(image):
    bbox = image.getbbox()
    if bbox is None:
        return BoundingBox.empty_bbox()
    return BoundingBox(bbox[0], bbox[1], bbox[2], bbox[3])


def _get_main_image_bbox(image, bg):
    """ get bounding box of image without border https://stackoverflow.com/a/10986041 """
    background = Image.new(image.mode, image.size, bg)
    diff = ImageChops.difference(image, background)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    return _get_bbox(diff)


def have_border(image, border_color):
    """ return True if any sides has border """
    bbox = _get_main_image_bbox(image, border_color)
    return bbox != BoundingBox(0, 0, image.size[0], image.size[1])


def have_all_border(image, border_color, border_thickness=1):  # all sides has border
    """ return True if all sides have border """
    image_bbox = _get_bbox(image)
    main_image_bbox = _get_main_image_bbox(image, border_color)
    return (main_image_bbox.left == image_bbox.left + border_thickness and
            main_image_bbox.top == image_bbox.top + border_thickness and
            main_image_bbox.right == image_bbox.right - border_thickness and
            main_image_bbox.bottom == image_bbox.bottom - border_thickness)


def have_top_border(image, border_color, border_thickness=1):
    image_bbox = _get_bbox(image)
    main_image_bbox = _get_main_image_bbox(image, border_color)
    return main_image_bbox.top == image_bbox.top + border_thickness


def have_bottom_border(image, border_color, border_thickness=1):
    image_bbox = _get_bbox(image)
    main_image_bbox = _get_main_image_bbox(image, border_color)
    return main_image_bbox.bottom == image_bbox.bottom - border_thickness


def have_left_border(image, border_color, border_thickness=1):
    image_bbox = _get_bbox(image)
    main_image_bbox = _get_main_image_bbox(image, border_color)
    return main_image_bbox.left == image_bbox.left + border_thickness


def have_right_border(image, border_color, border_thickness=1):
    image_bbox = _get_bbox(image)
    main_image_bbox = _get_main_image_bbox(image, border_color)
    return main_image_bbox.right == image_bbox.right - border_thickness


def crop(image: Image, bbox: BoundingBox):
    return image.crop((bbox.left, bbox.top, bbox.right, bbox.bottom))
