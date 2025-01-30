import re
from enum import Enum
import numpy as np
import easyocr
import cv2
from opencc import OpenCC
from PIL import Image, ImageDraw, ImageFont

class FontColorType(Enum):
    "Font color type for generated text"
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    AUTO = None

class ImageTranslator:
    "Translate image to Traditional Chinese"

    reader = easyocr.Reader(["ch_sim"])

    prob_threshold = 0.9
    "OCR probability threshold"

    contrast_factor = 0.5
    "preprocess contrast factor"

    beta = 0
    "preprocess beta"

    font_path = "assets/NotoSansTC-VariableFont_wght.ttf"

    # Variations:
    # [ b'Thin', b'ExtraLight', b'Light', b'Regular',
    #  b'Medium', b'SemiBold', b'Bold', b'ExtraBold', b'Black' ]
    font_variation = "Bold"


    def __init__(self, cc_type="s2twp"):
        "s2twp: 簡體到繁體（臺灣正體標準）並轉換爲臺灣常用詞彙"
        self.cc = OpenCC(cc_type)

    def translate_image(self, rgb_image, font_color_type = FontColorType.WHITE):
        "Translate the text in image to Traditional Chinese"
        preprocessed_img = self._preprocess(rgb_image)

        pil_image = Image.fromarray(rgb_image)

        draw = ImageDraw.Draw(pil_image)

        results = self.reader.readtext(preprocessed_img)

        for bbox, text, prob in results:

            if prob < self.prob_threshold:
                continue

            # if text do not have chinese, skip it
            if not self.has_chinese(text):
                continue

            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))

            width = bottom_right[0] - top_left[0]
            height = bottom_right[1] - top_left[1]

            # Calculate font size
            font_size = self.get_font_size_fit_box(width, height, self.font_path, text)

            font = ImageFont.truetype(self.font_path, font_size)
            font.set_variation_by_name(self.font_variation)

            # Decide the font color
            font_color = font_color_type.value
            if font_color == FontColorType.AUTO.value:
                # Cropped image
                bbox = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
                cropped_img = rgb_image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                cropped_preprocessed= preprocessed_img[bbox[1]:bbox[3], bbox[0]:bbox[2]]

                font_color = self.find_dominant_text_color(cropped_img, cropped_preprocessed)

            traditional_text = self.cc.convert(text)

            # Find the position to draw the text
            x = top_left[0] + width // 2
            y = top_left[1] + height // 2

            # Adjust the position to the baseline
            ascent, descent = font.getmetrics()
            baseline_adjustment = (ascent - descent) / 2
            y -= baseline_adjustment

            stroke_color = self.get_high_contrast_color(font_color)
            draw.text(
                (x, y),
                traditional_text,
                font=font,
                fill=font_color,
                stroke_width=3,
                stroke_fill=stroke_color,
                anchor="mt",
            )

        return pil_image

    def _preprocess(self, rgb_image):
        "Preprocess the image for recognition"
        img = cv2.convertScaleAbs(rgb_image, alpha=self.contrast_factor, beta=self.beta)
        return img

    @staticmethod
    def get_font_size_fit_box(
    width: int, height: int, font_path: str, text: str, font_variation="Bold"
    ) -> int:
        "Find the target font size to fit the text in the given box"
        font_size = min(width, height)

        while font_size > 4: # Too small font size is meaningless
            font = ImageFont.truetype(font_path, font_size)
            if font_variation is not None:
                font.set_variation_by_name(font_variation)

            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Check if the font size fits the box
            if text_width <= width and text_height <= height:
                return font_size

            font_size -= 1

        return font_size

    @staticmethod
    def has_chinese(text):
        "Check if the text contains any Chinese characters."
        return re.compile("[\u4e00-\u9fff]").search(text) is not None

    @staticmethod
    def find_dominant_text_color(image, preprocessed_img):
        """Find the most common color of text inside bbox

        Args:
            image: for selecting the original color
            preprocessed_img: for better performance in shape recognition

        Returns:
            color
        """
        gray = cv2.cvtColor(preprocessed_img, cv2.COLOR_RGB2GRAY)

        # Adaptive histogram equalization
        clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8,8))
        gray = clahe.apply(gray)

        _, text_mask = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)

        # Inverse the color of text if the white pixel more than the black
        # A better way is to use shape recognition to find the shape color
        white_pixels = np.sum(text_mask == 255)
        total_pixels = text_mask.shape[0] * text_mask.shape[1]
        if white_pixels > total_pixels - white_pixels:
            text_mask = cv2.bitwise_not(text_mask)

        masked_pixels = cv2.bitwise_and(image, image, mask=text_mask)
        region_pixels = masked_pixels[text_mask > 0]

        # Find most common color
        if len(region_pixels) > 0:
            unique, counts = np.unique(region_pixels, axis=0, return_counts=True)
            dominant_color = unique[counts.argmax()]
            return tuple(dominant_color)

        # Somehow it cannot find any pixel, so using black as default
        return (0, 0, 0)

    @staticmethod
    def get_high_contrast_color(color):
        "Get the high contrast color for better readability"
        # Calculate luminance
        luminance = 0.299*color[0] + 0.587*color[1] + 0.114*color[2]
        return (0, 0, 0) if luminance > 128 else (255, 255, 255)
