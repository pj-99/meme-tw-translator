import streamlit as st
import numpy as np
from PIL import Image
from main import translate_img_to_zhtw


def main():
    st.title("梗圖繁中化")

    # 上傳圖片
    uploaded_file = st.file_uploader("選擇一張圖片", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 讀取圖片
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        # 顯示原始圖片
        st.image(image, caption="原始圖片")

        # # 選擇處理方式
        # option = st.selectbox(
        #     "選擇圖片處理方式", ("邊緣檢測", "灰階處理", "高斯模糊", "二值化")
        # )
        processed_image = translate_img_to_zhtw(img_array)


        # 顯示處理後的圖片
        st.image(processed_image, caption="處理後的圖片")


def process_image(image, option, **kwargs):

    return image


if __name__ == "__main__":
    main()
