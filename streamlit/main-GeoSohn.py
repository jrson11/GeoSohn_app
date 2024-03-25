# Note:
#     메인 파일을 가능한한 건드리지 말것. 서브 펑션 안에서 다 해결할 것
#     서브 펑션은 csv 데이터를 수정가능하도록 셋팅할 것

import streamlit as st

# ====================================================================
## 셋업

st.set_page_config(layout="wide") # 페이지 설정을 wide 모드로 설정
st.header('GeoSohn - Web App') # 타이틀
password = st.sidebar.text_input('Please enter the :red[PASSWORD]','guest') # 비번 확인

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
if password == st.secrets['DB_password']:
    st.write("Thanks for joining :blue[Jung]'s database. Please click one of icons below.")

    # ---------------------------------------------------------------------------
    # 열을 나누어 아이콘 버튼 추가
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('#### Project')
        on_icon_project_maps = st.toggle(':world_map: Map')

    with col2:
        st.markdown('#### Mudmat')
        on_icon_mudmat_bearing = st.toggle(':fire: Mudmat: Bearing Capacity')

    with col3:
        st.markdown('#### Pile')
        on_icon4 = st.toggle(':rocket: Pile: Bearing Capacity')

    with col4:
        st.markdown('#### API')
        on_icon4 = st.toggle(':book: API and ISO')

    # ---------------------------------------------------------------------------
    # 아이콘 선택에 따라 서브 기능 실행
    st.write('---------------------------------------')

    if on_icon_project_maps:
        bp_project_maps()
        
    if on_icon_mudmat_bearing:
        bp_mudmat_bearing()


# 비밀번호가 틀리면 안내 메시지 출력
else:
    st.write(':blue[Purpose]: To develop engineering tools for innovative work automation')
    st.write('Author: Jung.Sohn')
    st.subheader(':blue[Features]')
    st.write('    1. :green[Confidential]: Data is protected by password, and the password will be updated regularly.')
    st.write('    2. :green[Verified]: All developed engineering tools will be verified with case studies.')
    st.write('    3. :green[Digital Twins]: Previous analoge data will be converted into digital to prepare the Data Science era.')

    st.subheader(':blue[Contents]')
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        '''
        \n 1. Project
        \n 1.a Map
        \n 1.b SoilProfile
        \n 1.c LabTesting
        '''
    with col2:
        '''
        \n 2. Mudmat
        \n 2.a Bearing
        \n 2.b Settlement
        \n 2.c PLAXIS
        '''
    with col3:
        '''
        \n 3. Pile
        \n 3.a Bearing
        \n 3.b Settlement
        \n 3.c PLAXIS
        '''
    with col4:
        '''
        \n 4. Code
        \n 4.a RP2A
        \n 4.b RP2GEO
        \n 4.c ISO19901
        '''
    
