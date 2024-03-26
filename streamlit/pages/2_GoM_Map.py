import streamlit as st
# ====================================================================
## 셋업

st.set_page_config(layout="wide") # 페이지 설정을 wide 모드로 설정
st.header('GeoSohn - GoM Map') # 타이틀
password = st.text_input("Please enter the :red[PASSWORD]") # 비번 확인

#@st.cache_data()
# ====================================================================
## 서브펑션

# ====================================================================
## 메인

# 비밀번호가 맞으면 실행
if password == st.secrets['DB_password']:
    st.write("Thanks for joining :blue[GeoSohn] digital twins system. Please click one of icons below.")

else:
    st.write("Welcome to :blue[GeoSohn] digital twins system. Guest can tour the table of contents.")
