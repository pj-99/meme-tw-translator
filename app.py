import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO
from main import translate_img_to_zhtw

def set_page_config():
    st.set_page_config(
        page_title="圖片繁體化小工具 - 簡體字轉繁體中文",
        page_icon="🔄",
        layout="centered"
    )

def customized_uploader():
    "Customized the uploader text"

    languages = {
        "EN": {
            "button": "Browse Files",
            "instructions": "Drag and drop files here",
            "limits": "Limit 200MB per file",
        },
        "TW": {
            "button": "選擇圖片",
            "instructions": "拖拉圖片或是點擊上傳",
            "limits": "檔案大小上限為 200 MB",
        },
    }
    # Can add multi-language if need
    # lang = st.radio("", options=["TW", "EN"], horizontal=True)
    lang = "TW"

    customized_uploader_label = (
    """
    <style>
        [data-testid="stFileUploaderDropzone"] div div::before {content:"INSTRUCTIONS_TEXT"}
        [data-testid="stFileUploaderDropzone"] div div span {display:none;}
        [data-testid="stFileUploaderDropzone"] div div::after {color:rgba(55, 55, 55, 0.6); font-size: .8em; content:"FILE_LIMITS"}
        [data-testid="stFileUploaderDropzone"] div div small{display:none;}
        [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] { font-size: 0px;}
        [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]::after {content: "BUTTON_TEXT";  font-size: 16px;}
    </style>
    """.replace(
            "BUTTON_TEXT", languages.get(lang).get("button")
        )
        .replace("INSTRUCTIONS_TEXT", languages.get(lang).get("instructions"))
        .replace("FILE_LIMITS", languages.get(lang).get("limits"))
    )
    st.markdown(customized_uploader_label, unsafe_allow_html=True)


def main():
    set_page_config()

    # Header section
    st.title("🔄圖片繁體化")
    st.markdown("將圖片裡的簡體字自動轉換成繁體中文，上傳圖片即可轉換")

    # Setup customized uploader
    # https://discuss.streamlit.io/t/how-to-customize-drag-and-drop-text-in-streamlit-file-uploader/54938/2
    customized_uploader()

    uploaded_file = st.file_uploader(
        label="上傳圖片",
        type=["jpg", "jpeg", "png"],
        help="支援 JPG、JPEG 和 PNG 格式的圖片",
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
            try:
                image = Image.open(uploaded_file)
                img_array = np.array(image)

                # Show progress
                with st.spinner("轉換中，請稍候..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    processed_image = translate_img_to_zhtw(img_array)
                    progress_bar.empty()

                # 顯示處理後的圖片
                st.markdown("#### 轉換結果")
                st.image(processed_image, use_container_width=True)

                # Download button
                buffered = BytesIO()
                processed_image.save(buffered, format="PNG")

                st.download_button(
                    label="下載圖片",
                    data=buffered.getvalue(),
                    file_name=uploaded_file.name,
                    mime="image/PNG",
                )
            except Exception as e:
                st.error(f"處理圖片時發生錯誤：{str(e)}")
                st.info("請確保上傳的圖片格式正確，並重新嘗試。")


    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>💡分享此工具</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
