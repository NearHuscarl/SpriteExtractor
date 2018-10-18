import os

default_settings = dict(
    spritesheet_folder=os.path.join(os.getcwd(), 'spritesheets'),
    current_spritesheet=0,
    border_thickness=1,
    template_str='AddSprite("", BoundingBox({L}, {T}, {R}, {B}), texture);',
    auto_copy_to_clipboard=True,
)
