import streamlit as st

def customized_uploader():
    """
    Customize the Streamlit file uploader with localized text and styling.
    
    Currently supports Traditional Chinese (TW) language configuration.
    Can be extended to support multiple languages in the future.
    """
    languages = {
        "TW": {
            "button": "選擇圖片",
            "instructions": "拖拉圖片或是點擊上傳",
            "limits": "檔案大小上限為 200 MB",
        },
    }
    # Can add multi-language if needed
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
