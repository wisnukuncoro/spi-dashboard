##################
# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import plotly.express as px
  
####################
# Page configuration
st.set_page_config(
    page_title="Revenue",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#############
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


branch_list = pd.read_csv('data/branch_list.csv', delimiter=';')
branch_region_1 = pd.read_csv('data/branch_region_1.csv', delimiter=';')
branch_region_2 = pd.read_csv('data/branch_region_2.csv', delimiter=';')
branch_region_3 = pd.read_csv('data/branch_region_3.csv', delimiter=';')
branch_region_4 = pd.read_csv('data/branch_region_4.csv', delimiter=';')


try:
    revenue = st.session_state['revenue']
    revenue.columns = ['label', 'value']
    
    st.markdown('***Data dibawah ini merupakan data per ' + st.session_state['long_date'] + '**')
    st.text("")
        
    col = st.columns(2, gap='medium')

    with col[0]:
        angka = revenue.iloc[0,1]
        st.metric(label='Revenue Versi Cabang', value="Rp {:,.0f}".format(angka).replace(",", "."), border=True)
    with col[1]:
        angka = revenue.iloc[1,1] / revenue.iloc[2,1] * 100
        st.metric(label='Persentase Ketercapaian', value=f"{angka:.2f} %", border=True)
    
    col = st.columns(2, gap='medium')
    
    with col[0]:
        angka = revenue.iloc[1,1]
        st.metric(label='Revenue Versi Finance', value="Rp {:,.0f}".format(angka).replace(",", "."), border=True)
    with col[1]:
        angka = revenue.iloc[2,1]
        st.metric(label='Target', value="Rp {:,.0f}".format(angka).replace(",", "."), border=True)
        
except:           
    st.markdown('Silakan upload file pada menu **Welcome** terlebih dahulu.')