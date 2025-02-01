import streamlit as st

def set_page_config():
    """
    Configure the Streamlit page settings.
    
    Sets the page title, icon, and layout for the application.
    """
    st.set_page_config(
        page_title="圖片簡轉繁工具 - 簡體字轉繁體中文",
        page_icon="🔄",
        layout="centered",
    )
