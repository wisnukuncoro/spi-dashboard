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
    page_title="Jumlah Siswa",
    page_icon="🧑‍💻",
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
      
      
#######################
# Dashboard Main Panel

if st.session_state['file_uploaded'] is not False:
    jumlah_siswa = st.session_state['jumlah_siswa']

    jumlah_siswa_wilayah_1 = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_region_1['kode_cabang'])]
    jumlah_siswa_wilayah_2 = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_region_2['kode_cabang'])]
    jumlah_siswa_wilayah_3 = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_region_3['kode_cabang'])]
    jumlah_siswa_wilayah_4 = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_region_4['kode_cabang'])]

    st.metric(label='Total Siswa Tahun Ajaran 2024/2025', value=int(jumlah_siswa['total_reg_24'].sum()))
    st.metric(label='Total Siswa Tahun Ajaran 2025/2026', value=int(jumlah_siswa['total_reg_25'].sum()))
        
    col = st.columns(2, gap='medium')

    with col[0]:
        
        fig = px.bar(jumlah_siswa_wilayah_1, 
            y='nama_cabang', 
            x='total_reg_24', 
            title='Wilayah Jawa Barat TA 24/25',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
            text='total_reg_24',)

        st.plotly_chart(fig)


    with col[1]:
                     
        fig = px.bar(jumlah_siswa_wilayah_1, 
            y='nama_cabang', 
            x='total_reg_25', 
            title='Wilayah Jawa Barat TA 25/26',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_25': 'Total Pendaftar'},
            text='total_reg_25')

        st.plotly_chart(fig)
        
    
    col = st.columns(2, gap='medium')

    with col[0]:
        
        fig = px.bar(jumlah_siswa_wilayah_2, 
            y='nama_cabang', 
            x='total_reg_24', 
            title='Wilayah Sumatera & Kalimantan TA 24/25',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
            text='total_reg_24',)

        st.plotly_chart(fig)

    with col[1]:
        
        fig = px.bar(jumlah_siswa_wilayah_2, 
            y='nama_cabang', 
            x='total_reg_25', 
            title='Wilayah Sumatera & Kalimantan TA 25/26',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_25': 'Total Pendaftar'},
            text='total_reg_25') 

        st.plotly_chart(fig)    
        
        
    col = st.columns(2, gap='medium')

    with col[0]:
        
        fig = px.bar(jumlah_siswa_wilayah_3, 
            y='nama_cabang', 
            x='total_reg_24', 
            title='Wilayah Indonesia Timur TA 24/25',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
            text='total_reg_24',)

        st.plotly_chart(fig)


    with col[1]:
                     
        fig = px.bar(jumlah_siswa_wilayah_3, 
            y='nama_cabang', 
            x='total_reg_25', 
            title='Wilayah Indonesia Timur TA 25/26',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_25': 'Total Pendaftar'},
            text='total_reg_25')

        st.plotly_chart(fig)
        
        
    col = st.columns(2, gap='medium')

    with col[0]:
        
        fig = px.bar(jumlah_siswa_wilayah_4, 
            y='nama_cabang', 
            x='total_reg_24', 
            title='Wilayah Jateng & Jatim TA 24/25',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
            text='total_reg_24',)

        st.plotly_chart(fig)

    with col[1]:
        
        fig = px.bar(jumlah_siswa_wilayah_4, 
            y='nama_cabang', 
            x='total_reg_25', 
            title='Wilayah Jateng & Jatim TA 25/26',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_25': 'Total Pendaftar'},
            text='total_reg_25') 

        st.plotly_chart(fig) 
        
else:
    st.markdown('Silakan upload file pada menu **Welcome** terlebih dahulu.')