from io import BytesIO
from pathlib import Path
from PIL import Image
import numpy as np
import streamlit as st
from page_config import set_page_config
from uploader_config import customized_uploader
from image_translator import ImageTranslator, FontColorType
from share_button import create_share_buttons
from debug import debug_environment


translator = ImageTranslator()


def main():

    set_page_config()

    # Header section
    st.title("🔄圖片簡轉繁")
    st.markdown("將圖片裡的簡體字自動轉換成繁體字，上傳圖片即可轉換")

    # Setup customized uploader
    customized_uploader()

    with st.container(border=True):
        uploaded_file = st.file_uploader(
            label="上傳圖片",
            type=["jpg", "jpeg", "png"],
            help="支援 JPG、JPEG 和 PNG 格式的圖片",
        )

        font_type = st.radio(
            "字體顏色",
            [FontColorType.WHITE, FontColorType.BLACK, FontColorType.AUTO],
            format_func=lambda x: (
                "白色"
                if x == FontColorType.WHITE
                else "黑色" if x == FontColorType.BLACK else "自動"
            ),
            horizontal=True,
            index=0,
        )

    upload_col, result_col = st.columns(2)

    with upload_col:
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            img_array = np.array(image)

            st.markdown("#### 原始圖片")
            st.image(image, use_container_width=True)

    with result_col:

        if uploaded_file is not None:
            st.markdown("#### 轉換結果")
            try:
                image = Image.open(uploaded_file)
                img_array = np.array(image)

                # Add caching for image processing
                @st.cache_data(show_spinner=False)
                def process_image(img_array, font_type):
                    return translator.translate_image(
                        img_array, font_color_type=font_type
                    )

                with st.spinner("轉換中，請稍候..."):
                    debug_environment()
                    processed_image = process_image(img_array, font_type)

                st.image(processed_image, use_container_width=True)

                buffered = BytesIO()
                # example: .png -> png
                img_format = Path(uploaded_file.name).suffix[1:]
                if img_format == "jpg":
                    img_format = "jpeg"

                processed_image.save(buffered, format=img_format)

                st.download_button(
                    label="下載圖片",
                    data=buffered.getvalue(),
                    file_name=uploaded_file.name,
                    mime=f"image/{img_format}",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"處理圖片時發生錯誤：{str(e)}")
                st.info("請確保上傳的圖片格式正確，並重新嘗試。")

    # Footer
    st.markdown("---")
    create_share_buttons()


if __name__ == "__main__":
    main()
