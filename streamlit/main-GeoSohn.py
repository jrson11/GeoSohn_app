import streamlit as st

# ====================================================================
## 셋업

st.set_page_config(layout="wide") # 페이지 설정을 wide 모드로 설정
st.header('GeoSohn - Web App') # 타이틀
password = st.sidebar.text_input("Please enter the :red[PASSWORD]") # 비번 확인
st.sidebar.write("Enter 'guest' to take tour")

# ====================================================================
## 서브펑션
@st.cache_data()

def mudmat_bearing_clay(key):
    if key == 'guest':
        from mudmat_bearing_capacity import guest
        guest()
    elif key == 'member':
        from mudmat_bearing_capacity import main
        main()

## --------------------------------------------------------------------
def toggles(password):
    col1,col2,col3,col4 = st.columns(4)

    with col1:
        toggle_map = st.toggle(':world_map: Map')
        toggle_SI = st.toggle(':floppy_disk: In-situ CPT')

    with col2:
        toggle_shallow_bearing = st.toggle(':alembic: Mudmat Bearing Capacity')
        toggle_shallow_settlement = st.toggle('Mudmat Settlement')

    with col3:
        toggle_pile_bearing = st.toggle(':test_tube: Suction Pile Bearing Capacity')
        toggle_pile_settlement = st.toggle('Suction Pile Settlement')

    with col4:
        toggle_lab = st.toggle(':building_construction: Soil Lab Testings')
        toggle_FEM = st.toggle(':computer: Numerical Modeling')

    st.write('--------------------------------------------------------')
    
    # Toggle 에 따른 서브펑션 실행
    if password == st.secrets['DB_password']:
        st.subheader('welcome')

        if toggle_shallow_bearing:
            project = st.sidebar.selectbox('Select one',['Clay','Tortue','Raven','ASWX','NaKika'])
            if project == 'Clay':
                mudmat_bearing_clay('member')
            
    else:
        st.subheader('Only a few web-app is available for guests.')
        
        if toggle_shallow_bearing:
            project = st.sidebar.selectbox('Select one',['Clay'])
            if project == 'Clay':
                mudmat_bearing_clay('guest')
        
        

# ====================================================================
## 메인

# 비밀번호가 맞으면 실행
if password == 'guest':
    st.write("Welcome to :blue[GeoSohn] digital twins system. Guest can tour the table of contents.")
    toggles(password)

elif password == st.secrets['DB_password']:
    st.write("Thanks for joining :blue[GeoSohn] digital twins system. Please click one of icons below.")
    toggles(password)


# 비밀번호가 틀리면 안내 메시지 출력
else:
    st.write(':blue[Purpose]: To develop engineering tools for innovative work automation')
    st.write(':blue[Author]: :green[Jung.Sohn]')
    st.subheader(':blue[Features]')
    st.write('    1. :green[Confidential]: Apps are protected by password, and the password will be updated regularly.')
    st.write('    2. :green[Verified]: All apps will be verified with case studies.')
    st.write('    3. :green[Digital Twins]: Previous data will be converted into digital to prepare the Data Science era.')
    #
    st.image('https://geosohn.readthedocs.io/en/latest/_images/Canvas_of_Offshore_Geotech(Sep2023).png')
