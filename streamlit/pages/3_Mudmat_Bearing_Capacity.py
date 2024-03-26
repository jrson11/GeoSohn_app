import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## log
#    02/28/2024: 진진 박사님께서 본인의 엑셀 템플릿 공유
#    03/13/2024: 첫번째 버전 완성
#    03/14/2024: 진진 박사님께 처음으로 시연
#    03/14/2024: 클래스를 사용한 객체화 시도
#    03/15/2024: Private 레퍼지토리를 사용하면 아무도 공유못한다는 사실 확인 (좌절), 하지만 Public 은 보안문제로 안만들기로 결정
#    03/16/2024: pyplot 그림이 맘에 안들어서 plotly 추가
#    03/19/2024: 클래스 객체화를 통한 Tortue 구축
#    03/20/2024: 클래스 너무 더러워서 중간 포기. 전체 스트럭쳐 재구성 노가다. 첫번째 예제 파일은 클래스 없이 가기로 결정
#    03/22/2024: csv 파일에서 파라미터를 읽어서 그래프까진 그릴수 있는데, 저장이 안됨. overwrite_csv 펑션이 무용지물 상태
#    03/25/2024: guest 와 member 용을 따로 나눠서 새로 퍼블릭하게 생성


# ====================================================================
## 셋업
st.set_page_config(layout="wide") # 페이지 설정을 wide 모드로 설정
st.header('GeoSohn - Mudmat Bearing Capacity') # 타이틀
password = st.text_input("Please enter the :red[PASSWORD] to get full access.") # 비번 확인



# ====================================================================
## 서브펑션

def make_envelope_constant(X):
    """주어진 배열의 마지막 값과 같은 값을 가진 배열을 생성하여 연결"""
    last_value = X[-1]
    ns = len(X)
    dummy = np.linspace(last_value, last_value, ns)
    Y = np.concatenate((X, dummy), axis=0)
    return Y

def make_envelope_decrease(X):
    """주어진 배열의 마지막 값에서 시작하여 0까지 감소하는 값을 가진 배열을 생성하여 연결"""
    last_value = X[-1]
    ns = len(X)
    dummy = np.linspace(last_value, 0, ns)
    Y = np.concatenate((X, dummy), axis=0)
    return Y

def sidebar():
    """사이드바 설정"""
    st.sidebar.subheader('Special thanks to the my Advisor P.Jeanjean, Ph.D., P.E., F.ASCE')
    st.sidebar.write(':blue[Purpose]: To estimate Factor of Safety from offshore mudmat bearing capacity analysis with CLAY soils.')
    st.sidebar.write(':blue[How to use]: Left columns has three tabs. Please fill out input data to apply updates.')
    st.sidebar.write(':blue[Author]: J.Sohn, Ph.D., P.E.')
    st.sidebar.write(':blue[Last update]: 03/25/2024')

def comment(toggle,X):
    if toggle == True:
        st.write(X)
        
def value(toggle,X,Y,Z):
    if toggle == True:
        st.write(X+' = '+str(Y),': ',Z)

# ====================================================================
## 메인

## 사이다바를 통한 코드 내용 설명
sidebar()

## 비밀번호를 통해서 멤버쉽 확인
if password == st.secrets['DB_password']:
    flag_member = 1
else:
    flag_member = 0

## 두열로 나눠서 좌측에는 파라미터, 우측에는 플롯팅
col_A, col_B = st.columns([1,2])

with col_A:
    tab1, tab2, tab3 = st.tabs(['Input', 'Deduced', 'Output'])
    with tab1:
        st.header(':blue[Input Properties]')
        if flag_member == 1:
            toggle_comment = st.toggle('Need Parameter Descriptions?')
            
        ## Foundation Geometry
        st.subheader('Foundation Geometry')
        col1, col2, col3 = st.columns(3)
        with col1:
            B = st.number_input('B (m)', value=10)    # Witdh (m)
            comment(toggle_comment,'Witdh')
        with col2:
            L = st.number_input('L (m)', value=10)    # Length (m)
            comment(toggle_comment,'Length')
        with col3:
            D = st.number_input('D (m)', value=0)     # Embedment (m)
            comment(toggle_comment,'Embedment')

        ## Loads
        st.subheader('Loads')
        col1, col2, col3 = st.columns(3)
        with col1:
            SW = st.number_input('SW (kN)', value=0)         # Self_weight (kN)
            comment(toggle_comment,'Self_weight')
            Vext = st.number_input('Vext (kN)', value=2000)  # External_Vertical_load (kN)
            comment(toggle_comment,'External_Vertical_load')
        with col2:
            Hext = st.number_input('Hext (kN)', value=500)   # External_Horizontal_load (kN)
            comment(toggle_comment,'External_Horizontal_load')
            θ = st.number_input('θ (deg)', value=0)           # angle_between_Hext_and_long_axis (deg)
            comment(toggle_comment,'angle_between_Hext_and_long_axis')
        with col3:
            Mext_B = st.number_input('Mext_B (kNm)', value=0) # Moment in B direction (kNm)
            comment(toggle_comment,'Moment in B direction')
            Mext_L = st.number_input('Mext_L (kNm)', value=0) # Moment in L direction (kNm)
            comment(toggle_comment,'Moment in L direction')

        ## Soil
        st.subheader('Soil')
        col1, col2, col3 = st.columns(3)
        with col1:
            Su0 = st.number_input('Su0 (kPa)', value=10)        # Shear strength at mudline (kPa)
            k = st.number_input('k (kPa/m)', value=0)           # rate of increasment with depth (kPa/m)
        with col2:
            SUW = st.number_input('SUW (kN/m3)', value=4)         # Average submerged unit weight (kN/m3)
            UWw = st.number_input('UWw (kN/m3)', value=10)        # Water unit weight (kN/m3)
            phi = st.number_input('phi (deg)', value=0)         # Triaxial drained friction angle (deg)
            flagGap = st.number_input('Gap in soil?', value=0)     
            comment(toggle_comment,'1 = yes, 0 = no')
        with col3:
            α1 = st.number_input('α1 (-)', value=0.1)        # Horizontal friction factor along skirt (-)
            Kru = st.number_input('Kru (-)', value=1)         # Earth pressure coefficient (no gap) (-)
            Kru_gap = st.number_input('Kru_gap (-)', value=2)     # Earth pressure coefficient (with gap) (-)
            flagRough = st.number_input('Rough surface?', value=1)   # Is footing rough? 1 for yes, 0 for no
            comment(toggle_comment,'1 = yes, 0 = no')


        ## Factors
        st.subheader('Factors')
        col1, col2, col3 = st.columns(3)
        with col1:
            FSbear_API = st.number_input('FSbear_API', value=2)
            FSslid_API = st.number_input('FSslid_API', value=1.5)
        with col2:
            γ_load_LRFD = st.number_input('γ_load_LRFD', value=1.35)
            γ_bear_LRFD = st.number_input('γ_bear_LRFD', value=0.67)
            γ_slid_LRFD = st.number_input('γ_slid_LRFD', value=0.8)
        with col3:
            γ_loadV1_ISO = st.number_input('γ_loadV1_ISO', value=1.35)
            γ_loadV2_ISO = st.number_input('γ_loadV2_ISO', value=1.225)
            γ_loadH_ISO = st.number_input('γ_loadH_ISO', value=1.35)
            γ_mat_ISO = st.number_input('γ_mat_ISO', value=1.25)

    with tab2:
        st.header(':green[Deduced Values]')
        # 여기에 계산 결과 표시 코드 추가
        if flag_member == 1:
            toggle_value = True
        else:
            toggle_value = False
            st.write('Please enter the :red[PASSWORD] to get full access.')

        ## Effective area
        eB = Mext_B/(Vext+SW)   # Eccentricity in B (m)
        eL = Mext_L/(Vext+SW)   # Eccentricity in L (m)
        Beff = B-2*eB           # Effective width (m)
        Leff = L-2*eL           # Effective length (m)
        Aeff = Beff*Leff        # Effective area (m2)
        if eB < 0 or eL < 0:
            print('ERROR in effective area ------------------------------------------')
        #
        value(toggle_value,'eB',eB,'Eccentricity in B (m)')
        value(toggle_value,'eL',eL,'Eccentricity in L (m)')
        value(toggle_value,'Beff',Beff,'Effective width (m)')
        value(toggle_value,'Leff',Leff,'Effective length (m)')
        value(toggle_value,'Aeff',Aeff,'Effective area (m2)')
        
        ## Vertical load transfer
        Wplug = SUW*D*Aeff                  # Weight of soil plug (kN)
        Vext_base = round(SW+Vext+Wplug)    # Vertical load at base (kN)
        #
        value(toggle_value,'Wplug',Wplug,'Weight of soil plug (kN)')
        value(toggle_value,'Vext_base',Vext_base,'Vertical load at base (kN)')
        
        ## Horizontal load transfer
        Hext_B = Hext*np.sin(θ*np.pi/180)
        Hext_L = Hext*np.cos(θ*np.pi/180)
        Su1 = Su0+(k*D)/2       # average Su over skirt (kPa)
        Hf = α1*Su1*2*L*D       # soil friction on skirt (kN)
        Hep = Kru*Su1*B*D       # Act and Pass earth pressure (kN)
        if flagGap == 1:
            Wwedge = SUW*L*D**2/(2*np.tan((np.pi/180)*(45-phi/2)))  # Weight of passive wedge (kN)
            Hep_c = min(Kru_gap*Su1*L*D + Wwedge,Hep)
            Hep_tot = Hep_c
        else:
            Hep_tot = Hep
        H_B_base = max(round(Hext_L-(Hf+Hep_tot)/FSslid_API),0.00001)

        ## Soil
        Cu0 = Su0 + k*D             # Su at base
        Su_bear = Su0+k*(D+B/4)     # Su at failure depth
        
        ## Setup for Envelope
        ns = 201 # Number of samples to descretize H
        resultant_QhQv = round(np.sqrt(H_B_base**2 + Vext_base**2))

        # ----------------------------------------------------------------------------
        ## API 2A 21st
        Nc = 5.14
        Nq = 1
        Sc = 1+(Beff/Leff)*(Nq/Nc)  # Note: p243 (C6.13.1-7)
        mL = (2+Leff/Beff)/(1+Leff/Beff)
        mB = (2+Beff/Leff)/(1+Beff/Leff)
        m = mL*(np.cos(θ*np.pi/180))**2 + mB*(np.sin(θ*np.pi/180))**2 

        ## Ultimate
        Qv_APIult = Aeff*(Su_bear*Nc*Sc+(SUW+UWw)*D)
        Qh_APIult = Cu0*Aeff

        
        ## Envelope
        api_H = np.linspace(0,Qh_APIult,ns)
        api_ic = 1-m*api_H/(Beff*Leff*Su_bear*Nc)   # Note: p243, (C6.13.1-6)
        api_Kc = api_ic*Sc                          # Note: p243 (C6.13.1-3)
        api_Qv = Aeff*(Su_bear*Nc*api_Kc+(SUW+UWw)*D)
        #
        API_Hult = make_envelope_constant(api_H)
        API_Vult = make_envelope_decrease(api_Qv)


        ## API_WSD          <------------------------  Resistance / FS
        WSD_Hall = API_Hult.copy()
        ii = WSD_Hall > Qh_APIult/FSslid_API
        WSD_Hall[ii] = Qh_APIult/FSslid_API
        WSD_Vall = API_Vult/FSbear_API


        ## API_LRFD         <------------------------  Resistance * γR / γL
        LRFD_Hall = API_Hult.copy()
        ii = WSD_Hall > Qh_APIult*γ_slid_LRFD/γ_load_LRFD
        LRFD_Hall[ii] = Qh_APIult*γ_slid_LRFD/γ_load_LRFD
        LRFD_Vall = API_Vult * γ_bear_LRFD/γ_load_LRFD


        # ----------------------------------------------------------------------------
        ## API 2GEO

        ## new parameters: F & Scv
        f = lambda a,b,c,d,x: a + b*x - ((c + b*x)**2 + d**2)**0.5 # Note: (A.17)
        #
        if flagRough == 1:
            a = 2.56; b = 0.457; c = 0.713; d = 1.38
        else:
            a = 1.372; b = 0.07; c = -0.128; d = 0.342
        #
        x = k*Beff/Su0
        F = f(a,b,c,d,x)
        #
        list_kBeff_over_Su0 = [0,2,4,6,8,10]
        list_Scv =[0.18, 0.00, -0.05, -0.07, -0.09, -0.10]
        Scv = np.interp(x,list_kBeff_over_Su0,list_Scv)    # Note: p78, Table A.2

        ## Correction factors
        # Ic_geo = 0.5 - 0.5[1 - H′/(Α′suo)]0.5         (A.21)
        # Sc_geo = Scv*Beff/L scv (1−2ic) (Β′/L′)       (A.18)
        # Dc_geo = 0.3 (su ave / su2) arctan(D/B′)      (A.20)
        # su2 = F(Nc suo+ κΒ′/4) / Nc.
        # Kc_iso = 1 + sc + dc − ic− bc− gc             (A.16)
        Su2 = F*(Nc*Cu0 + k*Beff/4)/Nc

        ## Ultimate H
        Qh_GEOult = Cu0*Aeff

        ## Ultimate V
        geo_H = np.linspace(0,Qh_GEOult,ns)
        geo_ic = 0.5 - 0.5*(1 - geo_H/(Aeff*Su0))**0.5  # Note: 2GEO uses unfactored H
        geo_sc = Scv*(1-2*geo_ic)*(Beff/Leff)           # Note: 2GEO uses Leff
        geo_dc = 0.3*(Su1/Su2)*np.arctan(D/Beff)        # Note: 2GEO uses Su1/Su2
        geo_Kc = 1 + geo_sc + geo_dc - geo_ic
        geo_Qv = Aeff*(SUW*D + F*(Nc*Cu0 + k*Beff/4)*geo_Kc)
        #
        GEO_Hult = make_envelope_constant(geo_H)
        GEO_Vult = make_envelope_decrease(geo_Qv)
        #
        geo_Hall = geo_H/FSslid_API     #<--------------  Resistance / FS
        geo_Vall = geo_Qv/FSbear_API
        #
        GEO_Hall = make_envelope_constant(geo_Hall)
        GEO_Vall = make_envelope_decrease(geo_Vall)

    
        # ----------------------------------------------------------------------------
        ## ISO 19901-4

        ## new parameters: F & Scv
        f = lambda a,b,c,d,x: a + b*x - ((c + b*x)**2 + d**2)**0.5 # Note: (A.17)
        #
        if flagRough == 1:
            a = 2.56; b = 0.457; c = 0.713; d = 1.38
        else:
            a = 1.372; b = 0.07; c = -0.128; d = 0.342
        #
        x = k*Beff/Su0
        F = f(a,b,c,d,x)

        ## Correction factors
        # Ic_iso = 0,5 − 0,5 1−[Hb /(Α′cu /γ m)]        (A.17) 
        # Sc_iso = 0,2(1− 2ic )(Β′ / L)                 (A.15)
        # Dc_iso = 0,3 arctan(Db / Β′)                  (A.16)
        # Kc = 1 + sc + dc − ic                         (A.14)

        ## Ultimate H
        Qh_ISOult = Cu0*Aeff

        ## Ultimate V
        iso_H = np.linspace(0,Qh_ISOult,ns)
        iso_ic = 0.5 - 0.5*(1 - iso_H/(Aeff*Su0))**0.5 
        iso_sc = 0.2*(1-2*iso_ic)*(Beff/L)              # Note: ISO uses L
        iso_dc = 0.3*np.arctan(D/Beff)
        iso_Kc = 1 + iso_sc + iso_dc - iso_ic
        iso_Qv = Aeff*(SUW*D + F*(Nc*Cu0 + k*Beff/4)*iso_Kc)
        #
        ISO_Qh = make_envelope_constant(iso_H)
        ISO_Qv = make_envelope_decrease(iso_Qv)

        ## Allowable
        iso_H_a = np.linspace(0,Qh_ISOult,ns)
        ii = iso_H_a > Qh_ISOult/(γ_loadH_ISO*γ_mat_ISO)
        iso_H_a[ii] = Qh_ISOult/(γ_loadH_ISO*γ_mat_ISO)  # <------  Resistance / γL / γm

        iso_ic_a = 0.5 - 0.5*(1 - iso_H_a*γ_loadH_ISO/(Aeff*Su0/γ_mat_ISO))**0.5 
        iso_sc_a = 0.2*(1-2*iso_ic_a)*(Beff/L)              # Note: ISO uses L
        iso_dc_a = 0.3*np.arctan(D/Beff)
        iso_Kc_a = 1 + iso_sc_a + iso_dc_a - iso_ic_a
        iso_Qv_a = (1/γ_loadV1_ISO)*Aeff*(SUW*D + F*(Nc*Cu0 + k*Beff/4)*iso_Kc_a/γ_mat_ISO)
        #
        ISO_Hall = make_envelope_constant(iso_H_a)
        ISO_Vall = make_envelope_decrease(iso_Qv_a)

    with tab3:
        st.header(':red[Resulting Outputs]')
        # 여기에 계산 결과 표시 코드 추가

        ## API
        df_API = pd.DataFrame()
        df_API['API_Hult'] = API_Hult
        df_API['API_Vult'] = API_Vult
        df_API['WSD_Hall'] = WSD_Hall
        df_API['WSD_Vall'] = WSD_Vall
        df_API['LRFD_Hall'] = LRFD_Hall
        df_API['LRFD_Vall'] = LRFD_Vall

        ## GEO
        df_GEO = pd.DataFrame()
        df_GEO['GEO_Hult'] = GEO_Hult
        df_GEO['GEO_Vult'] = GEO_Vult
        df_GEO['GEO_Vult'].fillna(-1, inplace=True)
        df_GEO['GEO_Hall'] = GEO_Hall
        df_GEO['GEO_Vall'] = GEO_Vall
        df_GEO['GEO_Vall'].fillna(-1, inplace=True)
        df_GEO['GEO_Hult*slope'] = GEO_Hult*Vext_base/H_B_base
        df_GEO['GEO_Hult*slope-GEO_Vult'] = df_GEO['GEO_Hult*slope'] - df_GEO['GEO_Vult']


        ## ISO
        df_ISO = pd.DataFrame()
        df_ISO['ISO_Hult'] = ISO_Qh
        df_ISO['ISO_Vult'] = ISO_Qv
        df_ISO['ISO_Vult'].fillna(-1, inplace=True)
        df_ISO['ISO_Hall'] = ISO_Hall
        df_ISO['ISO_Vall'] = ISO_Vall
        df_ISO['ISO_Vall'].fillna(-1, inplace=True)
        #
        interp_H = np.interp(iso_H,geo_Hall,geo_Vall)
        INTERP_H = make_envelope_constant(interp_H)
        df_ISO['GEO_Vall'] = INTERP_H
        df_ISO['min_Vall'] = df_ISO[['GEO_Vall','ISO_Vall']].min(axis=1)


        ## FS: API 2A
        max_Vult_api = round(np.interp(H_B_base,api_H,api_Qv))
        max_Hult_api = round(np.interp(Vext_base,API_Vult,API_Hult))
        #max_Qd_api = round(max_Hult_api*Vext_base/H_B_base)
        FS_bear_2A_ult = round(max_Vult_api/Vext_base,2)
        

        ## FS: API 2GEO
        idx_min_geo_ult_direction = df_GEO['GEO_Hult*slope-GEO_Vult'].abs().idxmin(0)
        hor_Qd_geo_ult = round(df_GEO.loc[idx_min_geo_ult_direction,'GEO_Hult'])
        ver_Qd_geo_ult = round(df_GEO.loc[idx_min_geo_ult_direction,'GEO_Hult*slope'])
        max_Qd_geo_ult = round(np.sqrt(hor_Qd_geo_ult**2 + ver_Qd_geo_ult**2))
        #
        max_Vult_geo = round(np.interp(H_B_base,geo_H,geo_Qv))
        FS_bear_2GEO_ult = round(max_Vult_geo/Vext_base,2)
        FS_slid_2GEO_ult = round(max_Hult_api/H_B_base,2)
        FS_geo_ult = round(max_Qd_geo_ult/resultant_QhQv,2)


with col_B:
    tab1, tab2, tab3 = st.tabs(['All', 'Each', 'Diagram'])

    with tab1:
        
        fig,ax = plt.subplots(2,1, figsize=(6,7), dpi=200, height_ratios=[3,1])
        #
        ax[0].plot(H_B_base,Vext_base, 'ro', label='Load at the base')
        ax[0].text(H_B_base*0.7,Vext_base*0.9, '('+str(H_B_base)+','+str(Vext_base)+')')
        if D == 0:
            pass
        else:
            ax[0].plot(Hext,Vext+SW, 'bx', label='Load at the mudline')
        ax[0].text(Hext*0.7,(Vext+SW)*0.9, '('+str(Hext)+','+str(Vext)+')',color='b')
        #
        ax[0].plot(df_API['API_Hult'],df_API['API_Vult'],'-',c='C0', label='API 2A ultimate')
        ax[0].plot(df_API['WSD_Hall'],df_API['WSD_Vall'],'--',c='C1', label='API WSD allowable')
        ax[0].plot(df_API['LRFD_Hall'],df_API['LRFD_Vall'],'-.',c='purple', label='API LRFD allowable')
        #
        ax[0].plot(df_GEO['GEO_Hult'],df_GEO['GEO_Vult'],'g-', label='API 2GEO ultimate')
        ax[0].plot(df_GEO['GEO_Hall'],df_GEO['GEO_Vall'],'g--', label='API 2GEO allowable')
        ax[0].plot(df_ISO['ISO_Hult'],df_ISO['ISO_Vult'],'k-', label='ISO 19901-4 ultimate')
        ax[0].plot(df_ISO['ISO_Hall'],df_ISO['ISO_Vall'],'k--', label='ISO 19901-4 allowable')
        #
        ax[0].fill_between(df_ISO['ISO_Hall'],df_ISO['min_Vall'],y2=0, color='C0', alpha=0.3)
        ax[0].plot([H_B_base,H_B_base],[Vext_base,max_Vult_api],'k--',linewidth=0.5)
        ax[0].text(H_B_base,max_Vult_api*0.9, 'Bearing \n(2A: FS='+str(FS_bear_2A_ult)+')\n(2GEO: FS='+str(FS_bear_2GEO_ult)+')')
        ax[0].plot([H_B_base,max_Hult_api],[Vext_base,Vext_base],'k--',linewidth=0.5)
        ax[0].text(max_Hult_api*0.85,Vext_base*1.0, 'Sliding \n(FS='+str(FS_slid_2GEO_ult)+')')
        ax[0].plot([0,hor_Qd_geo_ult],[0,ver_Qd_geo_ult],'r--',linewidth=0.5)
        ax[0].text(hor_Qd_geo_ult*0.85,ver_Qd_geo_ult*0.9,'(FS='+str(FS_geo_ult)+')', color='r',bbox=dict(edgecolor='None',facecolor='yellow', alpha=0.5))
        #
        ax[1].plot(0,0,'ro', label='Load at the base')
        ax[1].plot(0,0,'-',c='C0', label='API 2A ultimate')
        ax[1].plot(0,0,'--',c='C1', label='API WSD allowable')
        ax[1].plot(0,0,'-.',c='purple', label='API LRFD allowable')
        if D == 0:
            pass
        else:
            ax[1].plot(0,0,'bx', label='Load at the seafloor + self weight')
        ax[1].plot(0,0,'g-', label='API 2GEO ultimate')
        ax[1].plot(0,0,'g--', label='API 2GEO allowable')
        ax[1].plot(0,0,'k-', label='ISO 19901-4 ultimate')
        ax[1    ].plot(0,0,'k--', label='ISO 19901-4 allowable')
        ax[1].axis('off')
        #
        ax[0].set_xlabel('Unfactored H (kN)')
        ax[0].set_ylabel('Unfactored V (kN)')
        ax[0].set_xlim([0,Qh_APIult*1.1])
        ax[0].set_ylim([0,Qv_APIult*1.1])
        ax[0].grid(linestyle='dotted')
        ax[0].minorticks_on()
        ax[1].legend(loc='upper center', fancybox=True, shadow=True, fontsize=10, ncol=2)
        ax[0].set_title('$B$='+str(B)+'(m), $L$='+str(L)+'(m), $D$='+str(D)+'(m), $s_u$='+str(Su0)+'(kPa), κ='+str(k)+'(kPa/m)', fontsize=10)
        #ax.axis('equal')
        fig.suptitle('Undrained Load Interaction Envelopes', y=0.95)
    
        st.pyplot(fig)

    with tab2:

        if flag_member == 1:
            col1,col2,col3 = st.columns(3)
        
            with col1:
                toggle_ULT = st.toggle('Ultimate Capacity')
            with col2:
                toggle_WSD = st.toggle('Allowable Loads')
            with col3:
                toggle_LRFD = st.toggle('LRFD')
        else:
            toggle_ULT = False
            toggle_WSD = False
            toggle_LRFD = False
            st.write('Please enter the :red[PASSWORD] to get full access.')


        fig,ax = plt.subplots(2,1, figsize=(6,7), dpi=200, height_ratios=[3,1])
        #
        ax[0].plot(H_B_base,Vext_base, 'ro', label='Load at the base')
        ax[0].text(H_B_base*0.7,Vext_base*0.9, '('+str(H_B_base)+','+str(Vext_base)+')')
        if D == 0:
            pass
        else:
            ax[0].plot(Hext,Vext+SW, 'bx', label='Load at the mudline')
        ax[0].text(Hext*0.7,(Vext+SW)*0.9, '('+str(Hext)+','+str(Vext)+')',color='b')
        ax[1].plot(0,0,'ro', label='Load at the base')

        if toggle_ULT:
            ax[0].plot(df_API['API_Hult'],df_API['API_Vult'],'-',c='C0', label='API 2A ultimate')
            ax[0].plot(df_GEO['GEO_Hult'],df_GEO['GEO_Vult'],'g-', label='API 2GEO ultimate')
            ax[0].plot(df_ISO['ISO_Hult'],df_ISO['ISO_Vult'],'k-', label='ISO 19901-4 ultimate')
            #
            ax[1].plot(0,0,'-',c='C0', label='API 2A ultimate')
            ax[1].plot(0,0,'g-', label='API 2GEO ultimate')
            ax[1].plot(0,0,'k-', label='ISO 19901-4 ultimate')

        if toggle_WSD:
            ax[0].plot(df_API['WSD_Hall'],df_API['WSD_Vall'],'--',c='C1', label='API WSD allowable')
            ax[0].plot(df_GEO['GEO_Hall'],df_GEO['GEO_Vall'],'g--', label='API 2GEO allowable')
            ax[0].plot(df_ISO['ISO_Hall'],df_ISO['ISO_Vall'],'k--', label='ISO 19901-4 allowable')
            #
            ax[0].fill_between(df_ISO['ISO_Hall'],df_ISO['min_Vall'],y2=0, color='C0', alpha=0.3)
            ax[1].plot(0,0,'--',c='C1', label='API WSD allowable')
            ax[1].plot(0,0,'g--', label='API 2GEO allowable')
            ax[1].plot(0,0,'k--', label='ISO 19901-4 allowable')
        if toggle_LRFD:
            ax[0].plot(df_API['LRFD_Hall'],df_API['LRFD_Vall'],'-.',c='purple', label='API LRFD allowable')
            ax[1].plot(0,0,'-.',c='purple', label='API LRFD allowable')

        #
        #ax[0].plot([H_B_base,H_B_base],[Vext_base,max_Vult_api],'k--',linewidth=0.5)
        #ax[0].text(H_B_base,max_Vult_api*0.9, 'Bearing \n(2A: FS='+str(FS_bear_2A_ult)+')\n(2GEO: FS='+str(FS_bear_2GEO_ult)+')')
        #ax[0].plot([H_B_base,max_Hult_api],[Vext_base,Vext_base],'k--',linewidth=0.5)
        #ax[0].text(max_Hult_api*0.85,Vext_base*1.0, 'Sliding \n(FS='+str(FS_slid_2GEO_ult)+')')
        #ax[0].plot([0,hor_Qd_geo_ult],[0,ver_Qd_geo_ult],'r--',linewidth=0.5)
        #ax[0].text(hor_Qd_geo_ult*0.85,ver_Qd_geo_ult*0.9,'(FS='+str(FS_geo_ult)+')', color='r',bbox=dict(edgecolor='None',facecolor='yellow', alpha=0.5))
        #
        if D == 0:
            pass
        else:
            ax[1].plot(0,0,'bx', label='Load at the seafloor + self weight')
        ax[1].axis('off')
        #
        ax[0].set_xlabel('Unfactored H (kN)')
        ax[0].set_ylabel('Unfactored V (kN)')
        ax[0].set_xlim([0,Qh_APIult*1.1])
        ax[0].set_ylim([0,Qv_APIult*1.1])
        ax[0].grid(linestyle='dotted')
        ax[0].minorticks_on()
        ax[1].legend(loc='upper center', fancybox=True, shadow=True, fontsize=10, ncol=2)
        ax[0].set_title('$B$='+str(B)+'(m), $L$='+str(L)+'(m), $D$='+str(D)+'(m), $s_u$='+str(Su0)+'(kPa), κ='+str(k)+'(kPa/m)', fontsize=10)
        #ax.axis('equal')
        fig.suptitle('Undrained Load Interaction Envelopes', y=0.95)
    
        st.pyplot(fig)


    with tab3:
        if flag_member == 1:
            st.image('https://raw.githubusercontent.com/jrson11/GeoSohn_app/main/streamlit/images/Mudmat_bearing_capacity-Diagram.jpg')
        else:
            st.write('Please enter the :red[PASSWORD] to get full access.')
