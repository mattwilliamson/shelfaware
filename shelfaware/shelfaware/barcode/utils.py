# barcode/utils.py

import matplotlib.pyplot as plt
import cv2

def show_barcodes(image, boxes, barcodes):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.imshow(image)
    for (box, barcode) in zip(boxes, barcodes):
        x1, y1, x2, y2 = box
        barcode_type, barcode_data = barcode
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        ax.text(x1, y1 - 10, f"{barcode_type}: {barcode_data}", color='red', fontsize=12, backgroundcolor='white')
    plt.show()
