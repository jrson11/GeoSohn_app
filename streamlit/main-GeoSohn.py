import streamlit as st

# ====================================================================
## 셋업

st.set_page_config(layout="wide") # 페이지 설정을 wide 모드로 설정
st.header('GeoSohn - Web App') # 타이틀

def main():
    st.write(':blue[Purpose]: To develop engineering tools for innovative work automation')
    st.write(':blue[Author]: :green[Jung.Sohn]')
    st.subheader(':blue[Features]')
    st.write('    1. :green[Confidential]: Apps are protected by password, and the password will be updated regularly.')
    st.write('    2. :green[Verified]: All apps will be verified with case studies.')
    st.write('    3. :green[Digital Twins]: Previous data will be converted into digital to prepare the Data Science era.')
    #
    st.image('https://geosohn.readthedocs.io/en/latest/_images/Canvas_of_Offshore_Geotech(Sep2023).png')

main()
