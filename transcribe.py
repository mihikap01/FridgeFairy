

import pytesseract
import cv2
import os

class transcribe:
    def __init__(self, d='receipts/'):
        self.d = d

    def image_to_text(self, f):
        full_path = os.path.join(self.d, f)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"The file {full_path} does not exist.")
        im = cv2.imread(full_path)
        if im is None:
            raise ValueError(f"Could not read the image file {full_path}.")
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        return pytesseract.image_to_string(im)
