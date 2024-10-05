# Barcode Detector Library

This library provides a reusable Python API for detecting and decoding barcodes from images. It leverages YOLOv8 for object detection and `pyzbar` for decoding barcodes.

## Features

- Detect barcodes in images using a pre-trained YOLO model.
- Decode barcodes (EAN-13, CODE128, etc.) using `pyzbar`.
- Supports batch processing of images from a directory.

## Installation

```sh
sudo apt-get install libzbar0
```

## Usage

```python
from barcode.detector import BarcodeDetector

# Initialize the detector with the model path
detector = BarcodeDetector(model_path="path_to_your_yolo_model.pt")

# Detect and decode barcodes from an image
barcodes = detector.detect_and_decode("path_to_image.jpg")

# Print the detected barcodes
for barcode_type, barcode_data in barcodes:
    print(f"Detected {barcode_type} with data: {barcode_data}")

```

## Testing

```sh
python -m unittest discover -s shelfaware/barcode/tests
```