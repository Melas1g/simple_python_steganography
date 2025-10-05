# Python Steganography Script

A simple script to hide text inside an image using steganography.

## Installation

You need Python 3 and the Pillow library:

```bash
pip install Pillow
```

## How to Use

### Hide text in an image:
```bash
python main.py -e <image_path> "text_to_hide"
```

This will create a new image named `<original_name>_encrypted.png` in the same folder.

### Extract hidden text from an image:
```bash
python main.py -d <image_path>
```

The hidden text will be printed in the console.

## Notes

- Works best with PNG images.
- Text is encoded in UTF-8.
- The maximum amount of text you can hide depends on the image width.
