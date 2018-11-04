import os

DEFAULT_SETTINGS = dict(
    spritesheet_folder=os.path.join(os.getcwd(), 'spritesheets'),
    current_spritesheet=0,
    border_thickness=1,
    template_str='AddSprite("", BoundingBox({L}, {T}, {W}, {H}), texture);',
    auto_copy_to_clipboard=True,
)
