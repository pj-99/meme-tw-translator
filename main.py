import easyocr
import cv2
from opencc import OpenCC
from PIL import Image, ImageDraw, ImageFont
import glob


def convert_text_lightweight(
    image_path,
    output_path,
    font_path="assets/NotoSansTC-VariableFont_wght.ttf",
    font_size=32,
):
    """
    使用輕量級模型進行圖片文字轉換

    Parameters:
    image_path (str): 輸入圖片路徑
    output_path (str): 輸出圖片路徑
    font_path (str): 字體檔案路徑
    font_size (int): 基礎字體大小
    """
    # 初始化 EasyOCR
    reader = easyocr.Reader(["ch_sim"])

    # 讀取圖片
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 使用 EasyOCR 檢測文字
    results = reader.readtext(rgb_image)

    # 創建 OpenCC 轉換器
    cc = OpenCC("s2t")

    # 創建 PIL 圖片用於繪製
    pil_image = Image.fromarray(rgb_image)
    draw = ImageDraw.Draw(pil_image)

    font = ImageFont.truetype(font_path, font_size)
    font.set_variation_by_name("Thin")
    # [b'Thin', b'ExtraLight', b'Light', b'Regular',
    # b'Medium', b'SemiBold', b'Bold', b'ExtraBold', b'Black']

    # 處理每個檢測到的文字區域
    for bbox, text, prob in results:
        if prob > 0.9:
            # 只處理置信度高的文字
            # 計算文字區域
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))

            # 獲取區域寬高
            width = bottom_right[0] - top_left[0]
            height = bottom_right[1] - top_left[1]

            # 動態調整字體大小
            adjusted_font_size = min(int(height * 0.8), font_size)
            font = ImageFont.truetype(font_path, adjusted_font_size)
            font.set_variation_by_name("Bold")

            traditional = cc.convert(text)

            # 獲取文字大小
            text_bbox = draw.textbbox((0, 0), traditional, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # 計算文字位置（置中）
            x = top_left[0] + (width - text_width) // 2
            y = top_left[1] + (height - text_height) // 2

            # Offset for font
            y -= 10

            draw.text(
                (x, y),
                traditional,
                font=font,
                fill=(0, 0, 0),
                stroke_width=2,
                stroke_fill=(255, 255, 255),
            )

    # 儲存結果
    pil_image.convert("RGB").save(output_path)
    print(f"已將轉換後的圖片儲存至 {output_path}")


def main():
    input_folder = "data/input"
    output_folder = "data/output"

    # Read input images from folder using glob
    input_images = glob.glob(input_folder + "/*.jpg")
    for img in input_images:
        try:
            print(f"Converting {img}...")
            output_image = img.replace(input_folder, output_folder)
            convert_text_lightweight(img, output_image)

        except Exception as e:
            print(f"Error when converting {img}: {str(e)}")


if __name__ == "__main__":
    main()
