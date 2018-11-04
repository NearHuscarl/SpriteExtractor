import os
from PIL import Image

from common import DEFAULT_SETTINGS
from imageutil import (
    have_all_border,
    have_top_border,
    have_bottom_border,
    have_left_border,
    have_right_border,
    crop,
)
from boundingbox import BoundingBox

debugging: bool = False


def get_sprite_bbox(coord, spritesheet, border_color, border_thickness=1):
    """ Return the bounding box of the sprite at <coord> in <spritesheet> with <border_color>
    is spritesheet background color. <border_thickness> is the size of the border surrounding the sprite """
    x, y = coord
    selected_pixel = spritesheet.getpixel((x, y))

    if selected_pixel == border_color:
        return None

    # get bounding box surrounding selected pixel
    bbox = BoundingBox(x-1, y-1, x+2, y+2)
    sprite = crop(spritesheet, bbox)

    while not have_all_border(sprite, border_color, border_thickness):

        if bbox.left <= 0 or bbox.top <= 0 or bbox.right > spritesheet.width or bbox.bottom > spritesheet.height:
            return None

        while not have_top_border(sprite, border_color, border_thickness) and bbox.top > 0:
            bbox.top -= 1
            sprite = crop(spritesheet, bbox)

        while not have_bottom_border(sprite, border_color, border_thickness) and bbox.bottom <= spritesheet.height:
            bbox.bottom += 1
            sprite = crop(spritesheet, bbox)

        while not have_left_border(sprite, border_color, border_thickness) and bbox.left > 0:
            bbox.left -= 1
            sprite = crop(spritesheet, bbox)

        while not have_right_border(sprite, border_color, border_thickness) and bbox.right <= spritesheet.width:
            bbox.right += 1
            sprite = crop(spritesheet, bbox)

    # after have_all_border() return False we have a bounding box that has extra one pixel border
    bbox = BoundingBox(bbox.left + 1, bbox.top + 1, bbox.right - 1, bbox.bottom - 1)

    if debugging:
        print(str(bbox))
        # sprite.show()

    return bbox


def main():
    spritesheet_path = os.path.join(DEFAULT_SETTINGS['spritesheet_folder'], 'simon2.png')
    spritesheet = Image.open(spritesheet_path).convert('RGB')
    border_color = spritesheet.getpixel((0, 0))

    get_sprite_bbox((347, 469), spritesheet, border_color)
    get_sprite_bbox((174, 31), spritesheet, border_color)
    get_sprite_bbox((169, 64), spritesheet, border_color)
    get_sprite_bbox((175, 266), spritesheet, border_color)


if __name__ == '__main__':
    debugging = True
    main()
