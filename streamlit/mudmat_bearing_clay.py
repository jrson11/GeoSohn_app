import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ====================================================================
## 서브펑션
# Note: 너무 간단한 def 들은 굳이 다른데서 안불러오고 각 프로젝트 파일에서 선언 후 사용

def make_envelope_conatant(X):
    last_value = X[-1]
    ns = len(X)
    dummy = np.linspace(last_value,last_value,ns)
    Y = np.concatenate((X,dummy), axis=0)
    return Y

def make_envelope_decrease(X):
    last_value = X[-1]
    ns = len(X)
    dummy = np.linspace(last_value,0,ns)
    Y = np.concatenate((X,dummy), axis=0)
    return Y

def sidebar():
    st.sidebar.subheader('Special thanks to the my Advisor Philippe Jeanjean, Ph.D., P.E., F.ASCE')
    st.sidebar.write(':blue[Purpose]: To estimate Factor of Safety from offshore mudmat bearing capacity analysis with CLAY soils.')
    st.sidebar.write(':blue[How to use]: Left columns has three tabs. Please fill out input data to apply updates.')
    st.sidebar.write(':blue[Last update]: 03/20/2024')

# ====================================================================
## 메인

def main():
  sidebar()
  st.sidebar.write('Main')

def guest():
  sidebar()
  st.sidebar.write('Guest')
