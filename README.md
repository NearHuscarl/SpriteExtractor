# Sprite Extractor

A small program to quickly get sprite's bounding box (left, top, right, bottom position) on your spritesheet

![Animated demonstration](demo.gif)

## Template string

Here are all the available placholders to populate template string

| Placeholder | Description                         |
|:-----------:|-------------------------------------|
| {L}         | Left position of the bounding box   |
| {T}         | Top position of the bounding box    |
| {R}         | Right position of the bounding box  |
| {B}         | Bottom position of the bounding box |
| {W}         | Width of the bounding box           |
| {H}         | Height of the bounding box          |

## Download

You can either download [here] or build from source

## Build from source

* Install [pyinstaller](https://www.pyinstaller.org/)
* Open your terminal and execute the following commands
```
git clone https://github.com/NearHuscarl/SpriteExtractor
cd SpriteExtractor
pyinstaller build.spec
```
* After that, a new application will be created in the dist/ folder

[here]: https://github.com/NearHuscarl/SpriteExtractor/releases