# Note:
#     메인 파일을 가능한한 건드리지 말것. 서브 펑션 안에서 다 해결할 것
#     서브 펑션은 csv 데이터를 수정가능하도록 셋팅할 것

import streamlit as st

# ====================================================================
## 셋업

st.set_page_config(layout="wide") # 페이지 설정을 wide 모드로 설정
st.header('GeoSohn - Web App') # 타이틀
password = st.sidebar.text_input('Please enter the :red[PASSWORD] \n Enter 'guest' to take tour') # 비번 확인

# ====================================================================
## 서브펑션

def bp_project_maps():
    from bp_project import sub_project_map
    sub_project_map()
    
def bp_mudmat_bearing():
    from bp_mudmat import sub_mudmat_bearing
    sub_mudmat_bearing()

def bp_mudmat_settlement():
    from bp_mudmat import sub_mudmat_settlement
    sub_mudmat_settlement()
    
# ====================================================================
## 메인

# 비밀번호가 맞으면 실행
if password == 'guest':
    st.write("Welcome to :blue[GeoSohn] digital twins system. Guest can tour the table of contents.")

elif password == st.secrets['DB_password']:
    st.write("Thanks for joining :blue[GeoSohn] digital twins system. Please click one of icons below.")


# 비밀번호가 틀리면 안내 메시지 출력
else:
    st.write(':blue[Purpose]: To develop engineering tools for innovative work automation')
    st.write('Author: Jung.Sohn')
    st.subheader(':blue[Features]')
    st.write('    1. :green[Confidential]: Data is protected by password, and the password will be updated regularly.')
    st.write('    2. :green[Verified]: All developed engineering tools will be verified with case studies.')
    st.write('    3. :green[Digital Twins]: Previous analoge data will be converted into digital to prepare the Data Science era.')

    st.image('https://geosohn.readthedocs.io/en/latest/_images/Canvas_of_Offshore_Geotech(Sep2023).png')
