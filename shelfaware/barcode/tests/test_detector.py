import unittest
from shelfaware.barcode.detector import BarcodeDetector
import os
from PIL import Image


class TestBarcodeDetector(unittest.TestCase):
    
    def setUp(self):
        # Set up the actual model path and threshold for the test
        self.model_path = "models/barcodes.pt"  # Replace with your actual YOLO model path
        self.detector = BarcodeDetector(model_path=self.model_path, confidence_threshold=0.5)
        self.image_path = "samples/upc/20240918_075942.jpg"  # The image containing the barcode

    def test_find_barcodes(self):
        # Ensure the image exists before proceeding
        self.assertTrue(os.path.exists(self.image_path), "Test image not found")
        
        # Call the method to find barcodes
        result = self.detector.find_barcodes(self.image_path)
        
        # Assert that at least one barcode is found
        self.assertGreater(len(result), 0, "No barcodes detected in the image")
        
        # Ensure the result is a list of PIL images
        for img in result:
            self.assertIsInstance(img, Image.Image, "Output is not a PIL image")

    def test_decode_specific_barcode(self):
        # Ensure the image exists before proceeding
        self.assertTrue(os.path.exists(self.image_path), "Test image not found")

        # Extract and decode the barcodes from the image
        barcodes = self.detector.extract_and_decode(self.image_path)
        
        # Assert that the specific barcode '4099100207149' is present
        decoded_values = [barcode_data for _, barcode_data in barcodes]
        self.assertIn('4099100207149', decoded_values, "Expected barcode '4099100207149' not decoded")

    def test_extract_and_decode(self):
        # Ensure the image exists before proceeding
        self.assertTrue(os.path.exists(self.image_path), "Test image not found")

        # Extract and decode the barcodes from the image
        barcodes = self.detector.extract_and_decode(self.image_path)
        
        # Assert that at least one barcode is decoded
        self.assertGreater(len(barcodes), 0, "No barcodes were decoded in the image")
        
        # Ensure the decoded barcode has a valid type and data
        for barcode_type, barcode_data in barcodes:
            self.assertIsInstance(barcode_type, str, "Barcode type is not a string")
            self.assertIsInstance(barcode_data, str, "Barcode data is not a string")

if __name__ == '__main__':
    unittest.main()
