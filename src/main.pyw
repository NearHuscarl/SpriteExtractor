import os
from glob import glob
import pathlib
import json
from tkinter import (
    Frame,
    Tk,
    PhotoImage,
    filedialog,
    StringVar,
    IntVar,
    BooleanVar,
)
from tkinter.ttk import (
    Button,
    Entry,
    Label,
    Labelframe,
    Combobox,
    Checkbutton,
)

from PIL import ImageTk, Image

from common import default_settings
from tkinterapp import Application
import spritesheet
from color import rgba_to_hex, hex_to_rgba


class App(Application):
    """ Spritesheet tool GUI """

    def __init__(self, master):
        super().__init__(master)

        self.init_ui()
        self.center_window()

    def init_ui(self):
        """ Initialize GUI layout and widgets """
        self.master.title("Sprite Extractor")
        self.settings_path = os.path.join(os.getcwd(), 'settings', 'settings.json')
        self.padding = '1m'
        self.assetpath = os.path.join(os.getcwd(), 'assets')
        self.copyImage = PhotoImage(file=os.path.join(self.assetpath, 'copy.png'))  # 16x16 pixels
        self.colorPickerImage = PhotoImage(file=os.path.join(self.assetpath, 'colorpicker.png'))
        self.openImage = PhotoImage(file=os.path.join(self.assetpath, 'open.png'))

        self.spritesheet_folder = StringVar()
        self.border_thickness = IntVar()
        self.template_str = StringVar()
        self.transparent_color = StringVar()
        self.bbox_left = IntVar()
        self.bbox_top = IntVar()
        self.bbox_right = IntVar()
        self.bbox_bottom = IntVar()
        self.template_str_out = StringVar()
        self.auto_copy_to_clipboard = BooleanVar()

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.previewFrame = Frame(self.master)
        self.infoFrame = Frame(self.master)

        self.settingFrame = Labelframe(self.infoFrame, text='Settings')
        self.bboxFrame = Labelframe(self.infoFrame, text='Bounding Box')
        self.spriteFrame = Labelframe(self.infoFrame, text='Sprite Preview')
        self.templateStrFrame = Labelframe(self.infoFrame, text='Template String')

        self.previewFrame.grid(row=0, column=0, sticky='nsew')
        self.previewFrame.grid_columnconfigure(0, weight=1)
        self.previewFrame.grid_columnconfigure(2, weight=1)
        self.previewFrame.grid_rowconfigure(0, weight=1)
        self.previewFrame.grid_rowconfigure(2, weight=1)

        self.infoFrame.grid(row=0, column=1, sticky='n')

        self.settingFrame.grid(row=0, column=0, columnspan=2, padx=self.padding, pady=(self.padding, 0), sticky='ew')
        self.settingFrame.grid_columnconfigure(1, weight=1)

        self.bboxFrame.grid(row=1, column=0, padx=self.padding, pady=(self.padding, 0), sticky='ew')
        self.bboxFrame.grid_columnconfigure(1, weight=1)

        self.spriteFrame.grid(row=1, column=1, padx=self.padding, pady=(self.padding, 0), sticky='nsw')
        self.spriteFrame.grid_columnconfigure(0, weight=1)
        self.spriteFrame.grid_columnconfigure(2, weight=1)
        self.spriteFrame.grid_rowconfigure(0, weight=1)
        self.spriteFrame.grid_rowconfigure(2, weight=1)

        self.templateStrFrame.grid(row=2, column=0, columnspan=2, padx=self.padding, pady=self.padding, sticky='ew')
        self.templateStrFrame.grid_columnconfigure(0, weight=1)
        self.templateStrFrame.grid_rowconfigure(0, weight=1)

        self.spritesheetPanel = Label(self.previewFrame)
        self.spritesheetPanel.bind('<Button 1>', self.on_click_image)

        self.spritesheetFolderLabel = Label(self.settingFrame, text='Spritesheet Folder')

        self.spritesheetFolderButton = Button(self.settingFrame, image=self.openImage,
                                              command=self.on_change_spritesheet_folder)
        self.spritesheetFolderEntry = Entry(self.settingFrame, state='readonly',
                                            textvariable=self.spritesheet_folder)

        self.spritesheetLabel = Label(self.settingFrame, text='Spritesheet')
        self.spritesheetCombobox = Combobox(self.settingFrame, state='readonly')
        self.spritesheetCombobox.bind('<<ComboboxSelected>>', self.on_select_spritesheet)

        self.transColorLabel = Label(self.settingFrame, text='Transparent Color')
        self.transColorEntry = Entry(self.settingFrame, width=10, state='readonly', textvariable=self.transparent_color)
        self.transColorPanel = Label(self.settingFrame)
        self.pickColorButton = Button(self.settingFrame, image=self.colorPickerImage, command=self.on_pick_bgcolor)

        validate_cmd = (self.master.register(self.validate_number_value), '%S')  # %S - char inserted
        self.borderThicknessLabel = Label(self.settingFrame, text='Border Thickness')
        self.borderThicknessEntry = Entry(self.settingFrame, validate='key', validatecommand=validate_cmd,
                                          textvariable=self.border_thickness)

        self.topLabel = Label(self.bboxFrame, text='top')
        self.bottomLabel = Label(self.bboxFrame, text='bottom')
        self.leftLabel = Label(self.bboxFrame, text='left')
        self.rightLabel = Label(self.bboxFrame, text='right')

        self.topEntry = Entry(self.bboxFrame, state='readonly', textvariable=self.bbox_top)
        self.bottomEntry = Entry(self.bboxFrame, state='readonly', textvariable=self.bbox_bottom)
        self.leftEntry = Entry(self.bboxFrame, state='readonly', textvariable=self.bbox_left)
        self.rightEntry = Entry(self.bboxFrame, state='readonly', textvariable=self.bbox_right)

        self.copyTopButton = Button(self.bboxFrame, image=self.copyImage,
                                    command=lambda: self.to_clipboard(self.bbox_top.get()))
        self.copyBottomButton = Button(self.bboxFrame, image=self.copyImage,
                                       command=lambda: self.to_clipboard(self.bbox_top.get()))
        self.copyLeftButton = Button(self.bboxFrame, image=self.copyImage,
                                     command=lambda: self.to_clipboard(self.bbox_top.get()))
        self.copyRightButton = Button(self.bboxFrame, image=self.copyImage,
                                      command=lambda: self.to_clipboard(self.bbox_top.get()))

        self.spritePanel = Label(self.spriteFrame, border=2)

        self.templateEntry = Entry(self.templateStrFrame, textvariable=self.template_str)
        self.outputStrEntry = Entry(self.templateStrFrame, state='readonly', textvariable=self.template_str_out)
        self.autoCopyCheckbutton = Checkbutton(self.templateStrFrame, text='Auto copy to clipboard',
                                               variable=self.auto_copy_to_clipboard)

        self.spritesheetPanel.grid(row=1, column=1)

        self.spritesheetFolderLabel.grid(row=0, column=0, sticky='e')
        self.spritesheetFolderEntry.grid(row=0, column=1, columnspan=2, padx=(self.padding, 0), sticky='ew')
        self.spritesheetFolderButton.grid(row=0, column=3, padx=self.padding, pady=(0, self.padding))

        self.spritesheetLabel.grid(row=1, column=0, sticky='e')
        self.spritesheetCombobox.grid(row=1, column=1, columnspan=3, padx=self.padding, pady=(0, self.padding),
                                      sticky='ew')

        self.transColorLabel.grid(row=2, column=0, sticky='e')
        self.transColorEntry.grid(row=2, column=1, sticky='ew', padx=(self.padding, 0))
        self.transColorPanel.grid(row=2, column=2)
        self.pickColorButton.grid(row=2, column=3, padx=self.padding, pady=(0, self.padding))

        self.borderThicknessLabel.grid(row=3, column=0, sticky='e')
        self.borderThicknessEntry.grid(row=3, column=1, columnspan=3, sticky='ew',
                                       padx=self.padding, pady=(0, self.padding))

        self.topLabel.grid(row=0, column=0, sticky='e', padx=self.padding, pady=self.padding)
        self.bottomLabel.grid(row=1, column=0, sticky='e', padx=self.padding, pady=self.padding)
        self.leftLabel.grid(row=2, column=0, sticky='e', padx=self.padding, pady=self.padding)
        self.rightLabel.grid(row=3, column=0, sticky='e', padx=self.padding, pady=self.padding)

        self.topEntry.grid(row=0, column=1, sticky='ew')
        self.bottomEntry.grid(row=1, column=1, sticky='ew')
        self.leftEntry.grid(row=2, column=1, sticky='ew')
        self.rightEntry.grid(row=3, column=1, sticky='ew')

        self.copyTopButton.grid(row=0, column=2, padx=self.padding)
        self.copyBottomButton.grid(row=1, column=2, padx=self.padding)
        self.copyLeftButton.grid(row=2, column=2, padx=self.padding)
        self.copyRightButton.grid(row=3, column=2, padx=self.padding)

        self.autoCopyCheckbutton.grid(row=0, column=0, sticky='w', padx=self.padding)
        self.templateEntry.grid(row=1, column=0, sticky='ew', padx=self.padding, pady=(self.padding, 0))
        self.outputStrEntry.grid(row=2, column=0, sticky='ew', padx=self.padding, pady=self.padding)

        self.spritePanel.grid(row=1, column=1, sticky='nsew')
        self.init_value()

    def init_value(self):
        """ Initialize default values on startup """
        self.picking_color = False

        if os.path.isfile(self.settings_path):
            with open(self.settings_path) as file:
                settings = json.load(file)
        else:
            settings = default_settings

        if os.path.isdir(settings['spritesheet_folder']):
            self.spritesheet_folder.set(settings['spritesheet_folder'])
            self.update_spritesheet_list()
        if glob(os.path.join(self.spritesheet_folder.get(), '*.png')):
            try:
                current_index = settings['current_spritesheet']
                self.spritesheetCombobox.current(current_index)
            except Exception:  # selection index out of range
                pass

            self.set_spritesheet_panel()
            self.set_transparent_color(self.get_default_transparent_color())

        self.border_thickness.set(settings['border_thickness'])

        self.auto_copy_to_clipboard.set(settings['auto_copy_to_clipboard'])
        self.template_str.set(settings['template_str'])

    def update_spritesheet_list(self):
        spritesheet_path = self.spritesheet_folder.get()
        spritesheets = []

        for filename in os.listdir(spritesheet_path):
            if filename.endswith('.png'):
                name = os.path.splitext(filename)[0]
                spritesheets.append(name)

        self.spritesheetCombobox.configure(value=spritesheets)
        if len(spritesheets) > 0:
            self.spritesheetCombobox.current(0)
        else:
            self.spritesheetCombobox.set('')

    def set_spritesheet_panel(self):
        selected_spritesheet = self.spritesheetCombobox.get()

        if selected_spritesheet != '':
            image_path = os.path.join(self.spritesheet_folder.get(), selected_spritesheet + '.png')
            self.spritesheet_image = Image.open(image_path).convert('RGBA')
            self.spritesheet_photo = ImageTk.PhotoImage(self.spritesheet_image)
            self.spritesheetPanel.configure(image=self.spritesheet_photo)

    def set_transparent_color(self, rgba_color):
        self.transparent_color.set(rgba_to_hex(rgba_color))
        self.trans_color_photo = ImageTk.PhotoImage(Image.new(self.spritesheet_image.mode, (19, 19), rgba_color))
        self.transColorPanel.configure(image=self.trans_color_photo)

    def get_default_transparent_color(self):
        return self.spritesheet_image.getpixel((0, 0))

    def resize(self):
        width = self.spritesheet_photo.width() + self.infoFrame.winfo_width()
        height = max(self.spritesheet_photo.height(), self.infoFrame.winfo_height())

        self.master.geometry('{}x{}'.format(width, height))

    def on_change_spritesheet_folder(self):
        spritesheet_path = filedialog.askdirectory(title='Select spritesheet folder')

        if spritesheet_path != '':
            self.spritesheet_folder.set(spritesheet_path)
            self.update_spritesheet_list()

    def on_select_spritesheet(self, e):
        self.set_spritesheet_panel()
        self.set_transparent_color(self.get_default_transparent_color())
        self.resize()
        self.center_window()

    def on_pick_bgcolor(self):
        self.picking_color = True
        self.master.config(cursor='tcross')

    def on_click_image(self, e):
        if self.picking_color:
            self.pick_bgcolor(e)
        else:
            self.update_sprite_bbox(e)

    def pick_bgcolor(self, e):
        selected_color = self.spritesheet_image.getpixel((e.x, e.y))
        self.set_transparent_color(selected_color)
        self.picking_color = False
        self.master.config(cursor='arrow')

    def update_sprite_bbox(self, e):
        bbox = spritesheet.get_sprite_bbox(
            (e.x, e.y),
            self.spritesheet_image,
            hex_to_rgba(self.transparent_color.get()),
            int(self.border_thickness.get()))

        if bbox is None:
            return

        left, top, right, bottom = bbox

        self.bbox_left.set(left)
        self.bbox_top.set(top)
        self.bbox_right.set(right)
        self.bbox_bottom.set(bottom)

        self.sprite_image = self.spritesheet_image.crop((left, top, right, bottom))
        self.sprite_photo = ImageTk.PhotoImage(self.sprite_image)
        self.spritePanel.configure(image=self.sprite_photo)

        if self.auto_copy_to_clipboard.get():
            self.template_str_out.set(self.template_str.get()
                                      .replace('{L}', str(left))
                                      .replace('{T}', str(top))
                                      .replace('{R}', str(right))
                                      .replace('{B}', str(bottom)))
            self.to_clipboard(self.template_str_out.get())

    def on_closing(self):
        try:
            settings = dict(
                spritesheet_folder=self.spritesheet_folder.get(),
                current_spritesheet=self.spritesheetCombobox.current(),
                border_thickness=self.border_thickness.get(),
                template_str=self.template_str.get(),
                auto_copy_to_clipboard=self.auto_copy_to_clipboard.get(),
            )
            settings_dir = os.path.dirname(self.settings_path)
            if not os.path.isdir(settings_dir):
                pathlib.Path(settings_dir).mkdir(parents=True, exist_ok=True)

            with open(self.settings_path, 'w') as file:
                json.dump(settings, file, sort_keys=True, indent=4)
        finally:
            self.master.destroy()


def main():
    root = Tk()

    app = App(root)
    app.mainloop()


if __name__ == '__main__':
    main()
