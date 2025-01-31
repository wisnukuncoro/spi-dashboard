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

try:
    num_of_students = st.session_state['num_of_students']

    num_of_students_region_1 = num_of_students[num_of_students['kode_cabang'].isin(branch_region_1['kode_cabang'])]
    num_of_students_region_2 = num_of_students[num_of_students['kode_cabang'].isin(branch_region_2['kode_cabang'])]
    num_of_students_region_3 = num_of_students[num_of_students['kode_cabang'].isin(branch_region_3['kode_cabang'])]
    num_of_students_region_4 = num_of_students[num_of_students['kode_cabang'].isin(branch_region_4['kode_cabang'])]
    
    st.markdown('***Data dibawah ini merupakan data per ' + st.session_state['date'] + '**')
    st.text("")
     
    col = st.columns(2, gap='medium')
    
    with col[0]:
        st.metric(label='Total Siswa TA 24/25 (TA Berjalan)', value=int(num_of_students['total_reg_24'].sum()), border=True)
        st.metric(label='Total Siswa Private TA 24/25 (TA Berjalan)', value=int(num_of_students['private_24'].sum()), border=True)
        
    with col[1]:
        st.metric(label='Total Siswa TA 25/26', value=int(num_of_students['total_reg_25'].sum()), border=True)
        st.metric(label='Total Siswa Private TA 25/26', value=0, border=True)
        
    col = st.columns(2, gap='medium')

    with col[0]:
        
        fig = px.bar(num_of_students_region_1, 
            y='nama_cabang', 
            x='total_reg_24', 
            title='Wilayah Jawa Barat TA 24/25',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Siswa'},
            text='total_reg_24',)

        st.plotly_chart(fig)

    with col[1]:
                     
        fig = px.bar(num_of_students_region_1, 
            y='nama_cabang', 
            x='total_reg_25', 
            title='Wilayah Jawa Barat TA 25/26',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_25': 'Total Siswa'},
            text='total_reg_25')

        st.plotly_chart(fig)
        
    
    col = st.columns(2, gap='medium')

    with col[0]:
        
        fig = px.bar(num_of_students_region_2, 
            y='nama_cabang', 
            x='total_reg_24', 
            title='Wilayah Sumatera & Kalimantan TA 24/25',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Siswa'},
            text='total_reg_24',)

        st.plotly_chart(fig)

    with col[1]:
        
        fig = px.bar(num_of_students_region_2, 
            y='nama_cabang', 
            x='total_reg_25', 
            title='Wilayah Sumatera & Kalimantan TA 25/26',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_25': 'Total Siswa'},
            text='total_reg_25') 

        st.plotly_chart(fig)    
        
        
    col = st.columns(2, gap='medium')

    with col[0]:
        
        fig = px.bar(num_of_students_region_3, 
            y='nama_cabang', 
            x='total_reg_24', 
            title='Wilayah Indonesia Timur TA 24/25',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Siswa'},
            text='total_reg_24',)

        st.plotly_chart(fig)


    with col[1]:
                     
        fig = px.bar(num_of_students_region_3, 
            y='nama_cabang', 
            x='total_reg_25', 
            title='Wilayah Indonesia Timur TA 25/26',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_25': 'Total Siswa'},
            text='total_reg_25')

        st.plotly_chart(fig)
        
        
    col = st.columns(2, gap='medium')

    with col[0]:
        
        fig = px.bar(num_of_students_region_4, 
            y='nama_cabang', 
            x='total_reg_24', 
            title='Wilayah Jateng & Jatim TA 24/25',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Siswa'},
            text='total_reg_24',)

        st.plotly_chart(fig)

    with col[1]:
        
        fig = px.bar(num_of_students_region_4, 
            y='nama_cabang', 
            x='total_reg_25', 
            title='Wilayah Jateng & Jatim TA 25/26',
            labels={'nama_cabang': 'Nama Cabang', 'total_reg_25': 'Total Siswa'},
            text='total_reg_25') 

        st.plotly_chart(fig) 
        
except:
    st.markdown('Silakan upload file pada menu **Welcome** terlebih dahulu.')