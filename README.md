# NumPy Image Editor

A small image editing tool built using **only NumPy array operations** — no OpenCV, no PIL filters, no `scipy.ndimage`. Every effect (grayscale, brightness, contrast, flip, crop, invert, blend, blur) is implemented as raw array math, to practice and demonstrate core NumPy skills: slicing, broadcasting, and vectorized operations.

## Features
- **Grayscale** — weighted RGB-to-gray conversion
- **Brightness** — add/subtract a constant to every pixel
- **Contrast** — scale pixels around the midpoint
- **Flip** — horizontal and vertical, via array slicing
- **Crop** — rectangular region selection via slicing
- **Invert** — color negative
- **Blend** — combine two images with a weighted average
- **Blur** — simple neighbor-averaging blur using `np.roll` (no loops)

## Project structure
```
numpy-image-editor/
├── edit_image.py       # the main tool (function + CLI)
├── image 1             # add image
├── image 2             # add image
├── README.md
├── notebooks/
│   └── image-edit.ipynb      # step-by-step development notebook
```

## Installation
```bash
pip install numpy pillow
```

## Usage


```bash
python edit_image_interactive.py
```
```
Image path: photo.jpg
Type an operation (...): grayscale
Saved: out_grayscale.jpg

Type an operation (...): crop
  top,bottom,left,right: 100,300,200,500
Saved: out_crop.jpg

Type an operation (...): quit
```

## How it works (brief)
- **Grayscale:** `0.299*R + 0.587*G + 0.114*B`, applied across the whole image via broadcasting.
- **Brightness/Contrast:** pixel math with `np.clip(..., 0, 255)` to keep values in valid range.
- **Flip:** `arr[:, ::-1]` (horizontal) and `arr[::-1, :]` (vertical) — reversed slicing, no built-in flip function.
- **Blur:** shifts the whole image up/down/left/right with `np.roll` and averages with the original — this averages every pixel with its 4 neighbors in one vectorized pass, no per-pixel loop.




