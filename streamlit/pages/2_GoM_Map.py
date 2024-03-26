import streamlit as st
# ====================================================================
## 셋업

st.set_page_config(layout="wide") # 페이지 설정을 wide 모드로 설정
st.header('GeoSohn - GoM Map') # 타이틀
password = st.text_input("Please enter the :red[PASSWORD]") # 비번 확인

