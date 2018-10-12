import os

default_settings = dict(
    spritesheet_folder=os.path.join(os.getcwd(), 'spritesheets'),
    border_thickness=1,
    template_str='AddSprite("", BoundingBox({L}, {T}, {R}, {B}), texture);',
    auto_copy_to_clipboard=True,
)
