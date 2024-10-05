import cv2
from PIL import Image
from pyzbar.pyzbar import decode
from ultralytics import YOLO


class BarcodeDetector:
    """
    A class to detect and decode barcodes from images using YOLO and pyzbar.

    Attributes:
        model (YOLO): The YOLO model used for detecting barcodes.
        confidence_threshold (float): The confidence threshold for barcode detection.
    """

    def __init__(self, model_path, confidence_threshold=0.5):
        """
        Initializes the BarcodeDetector with the given model path and confidence threshold.

        Args:
            model_path (str): Path to the YOLO model weights.
            confidence_threshold (float): The confidence threshold for barcode detection.
        """
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def _load_image(self, input_image):
        """
        Load and process an image, which can be either a path, a cv2 image, or a PIL image.

        Args:
            input_image (str or np.ndarray or PIL.Image): The input image which can be a file path, 
            a cv2 image (numpy array), or a PIL Image.

        Returns:
            np.ndarray: The image in RGB format as a numpy array.
        """
        if isinstance(input_image, str):
            # Load image from file path
            image = cv2.imread(input_image)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif isinstance(input_image, np.ndarray):
            # If the input is a cv2 image (numpy array)
            image_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        elif isinstance(input_image, Image.Image):
            # If the input is a PIL image, convert it to numpy array in RGB format
            image_rgb = np.array(input_image.convert('RGB'))
        else:
            raise ValueError("Invalid input image type. Expected file path, cv2 image, or PIL image.")

        return image_rgb

    def find_barcodes(self, input_image):
        """
        Detects barcodes in the provided image and returns the cropped regions containing the barcodes.

        Args:
            input_image (str or np.ndarray or PIL.Image): The input image which can be a file path, 
            a cv2 image (numpy array), or a PIL Image.

        Returns:
            list: A list of cropped images (PIL.Image) where barcodes are detected. 
                  If no cropping is performed, the entire image is returned if barcodes are detected.
        """
        image_rgb = self._load_image(input_image)

        # Perform YOLOv8 detection
        results = self.model(image_rgb, conf=self.confidence_threshold)
        cropped_images = []

        # If results are found, add the full image (cropping disabled for better performance)
        if len(results) > 0:
            cropped_images.append(Image.fromarray(image_rgb))

        # Cropping logic is disabled due to better performance when using the entire image.
        # Uncomment the code below to enable cropping of detected barcodes.
        #
        # for result in results:
        #     boxes = result.boxes.xyxy  # Bounding boxes
        #     for box in boxes:
        #         x1, y1, x2, y2 = map(int, box)  # Convert to integer
        #         cropped_image = image_rgb[y1:y2, x1:x2]
        #         cropped_image = Image.fromarray(cropped_image)
        #         cropped_images.append(cropped_image)
                
        return cropped_images

    def decode_barcodes(self, cropped_images):
        """
        Decodes barcodes from a list of cropped images using pyzbar.

        Args:
            cropped_images (list): A list of cropped images (PIL.Image) from which barcodes will be decoded.

        Returns:
            list: A list of tuples where each tuple contains the barcode type and the decoded barcode data.
        """
        barcodes = []
        for cropped_image in cropped_images:
            decoded_barcodes = decode(cropped_image)
            for barcode in decoded_barcodes:
                barcode_data = barcode.data.decode('utf-8')  # EAN-13 data
                barcode_type = barcode.type  # Type of barcode (EAN13, CODE128, etc.)
                barcodes.append((barcode_type, barcode_data))
        return barcodes

    def extract_and_decode(self, input_image):
        """
        Detects and decodes barcodes from an image. It is a combination of find_barcodes and decode_barcodes.

        Args:
            input_image (str or np.ndarray or PIL.Image): The input image which can be a file path, 
            a cv2 image (numpy array), or a PIL Image.

        Returns:
            list: A list of tuples where each tuple contains the barcode type and the decoded barcode data.
        """
        cropped_images = self.find_barcodes(input_image)
        barcodes = self.decode_barcodes(cropped_images)
        return barcodes
