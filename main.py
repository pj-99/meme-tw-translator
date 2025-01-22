"""
將梗圖的簡體字翻譯成繁體中文
"""

import re
import glob
import easyocr
import cv2
from opencc import OpenCC
from PIL import Image, ImageDraw, ImageFont

reader = easyocr.Reader(["ch_sim"])

# s2twp 簡體到繁體（臺灣正體標準）並轉換爲臺灣常用詞彙
cc = OpenCC("s2twp")

def preprocess(img, contrast_factor=1.5, beta=0):
    "Preprocess the image"
    img = cv2.convertScaleAbs(img, alpha=contrast_factor, beta=beta)
    return img


def has_chinese(text):
    "Check if the text contains any Chinese characters."
    return re.compile("[\u4e00-\u9fff]").search(text) is not None


def get_font_size_fit_box(
    width: int, height: int, font_path: str, text: str, font_variation="Bold"
) -> int:
    """
    找出能讓指定文字完全符合目標寬高的字型大小

    Args:
        width (int): 目標寬度
        height (int): 目標高度
        font_path (str): 字體文件路徑
        text (str): 要測量的文字

    Returns:
        int: 合適的字型大小
    """
    font_size = min(width, height)  # 從較小的邊長開始

    while font_size > 4:
        font = ImageFont.truetype(font_path, font_size)
        if font_variation is not None:
            font.set_variation_by_name(font_variation)

        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 檢查是否符合目標大小
        if text_width <= width and text_height <= height:
            return font_size

        font_size -= 1

    return font_size


def translate_img_to_zhtw(
    rgb_image,
    font_path="assets/NotoSansTC-VariableFont_wght.ttf",
    font_size=32,
):
    """
    translate text in image
    """

    preprocessed_img = preprocess(rgb_image, 0.5)

    # # show image
    # cv2.imshow("image", preprocessed_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    pil_image = Image.fromarray(rgb_image)
    draw = ImageDraw.Draw(pil_image)

    font = ImageFont.truetype(font_path, font_size)
    font.set_variation_by_name("Thin")

    results = reader.readtext(preprocessed_img)
    for bbox, text, prob in results:
        print("text:", text, "prob:", prob)

        # if text is not chinese, skip
        if not has_chinese(text):
            continue

        if prob > 0.9:
            # 計算文字區域
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))

            width = bottom_right[0] - top_left[0]
            height = bottom_right[1] - top_left[1]

            # Draw detection box
            # draw.rectangle([top_left, bottom_right], outline=(255, 0, 0), width=2)

            # Calculate font size
            adjusted_font_size = get_font_size_fit_box(width, height, font_path, text)
            font = ImageFont.truetype(font_path, adjusted_font_size)

            # Variations:
            # [ b'Thin', b'ExtraLight', b'Light', b'Regular',
            #  b'Medium', b'SemiBold', b'Bold', b'ExtraBold', b'Black' ]
            font.set_variation_by_name("Bold")

            traditional = cc.convert(text)

            ascent, descent = font.getmetrics()

            x = top_left[0] + width // 2
            y = top_left[1] + height // 2

            baseline_adjustment = (ascent - descent) / 2
            y -= baseline_adjustment

            draw.text(
                (x, y),
                traditional,
                font=font,
                fill=(0, 0, 0),
                stroke_width=2,
                stroke_fill=(255, 255, 255),
                anchor="mt",
            )

    return pil_image.convert("RGB")


def main():
    """
    local test translation
    """

    input_folder = "data/input"
    output_folder = "data/output"

    # Read input images from folder using glob
    input_images = glob.glob(input_folder + "/*.jpg")
    for image_path in input_images:
        try:
            print(f"Converting {image_path}...")

            # Convert to RGB
            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            output_image = image_path.replace(input_folder, output_folder)
            img = translate_img_to_zhtw(rgb_image)
            img.save(output_image)
        except Exception as e:
            print(f"Error when converting {img}: {str(e)}")


if __name__ == "__main__":
    main()
