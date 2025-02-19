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
    page_title="Siswa",
    page_icon="🏆",
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
    siswa = st.session_state['siswa']
    siswa.fillna(0, inplace=True)

    siswa_wilayah_1 = siswa[siswa['kode_cabang'].isin(branch_region_1['kode_cabang'])]
    siswa_wilayah_2 = siswa[siswa['kode_cabang'].isin(branch_region_2['kode_cabang'])]
    siswa_wilayah_3 = siswa[siswa['kode_cabang'].isin(branch_region_3['kode_cabang'])]
    siswa_wilayah_4 = siswa[siswa['kode_cabang'].isin(branch_region_4['kode_cabang'])]

    st.markdown('***Data dibawah ini merupakan data per ' + st.session_state['long_date'] + '**')
    st.text("")
        
    col = st.columns(3, gap='medium')

    with col[0]:
        st.metric(label='Perolehan Siswa Bulan Ini', value=int(siswa['hasil'].sum()), border=True)
    with col[1]:
        st.metric(label='Target Perolehan Siswa', value=int(siswa['target'].sum()), border=True)
    with col[2]:
        x = int(siswa['hasil'].sum()) / int(siswa['target'].sum()) * 100
        st.metric(label='Persentase', value=f"{x:.2f} %", border=True)
        
    # col = st.columns(2, gap='medium')

    # with col[0]:
    #     value = f"{max(siswa['percentage']*100):.2f}"
    #     cabang = siswa[siswa['percentage'] == max(siswa['percentage'])]
    #     st.metric(label='Cabang dengan persentase perolehan tertinggi terhadap target', value=f"{cabang['nama_cabang'].iloc[0]}: {value} %", border=True)
    # with col[1]:
    #     value = max(siswa['hasil'])
    #     cabang = siswa[siswa['hasil'] == max(siswa['hasil'])]
    #     st.metric(label='Cabang dengan perolehan pertinggi', value=f"{cabang['nama_cabang'].iloc[0]}: {value} siswa", border=True)

    daily_students_gain = []

    num_of_dates = [i for i in range(1, st.session_state['num_of_dates']+1)]

    for i in range(len(num_of_dates)):
        daily_students_gain.append(siswa.iloc[:,i+4].sum())  

    daily_students_gain = pd.DataFrame({'tanggal': num_of_dates,
                                        'hasil': daily_students_gain
    })

    date = int(st.session_state['date'])
    month = st.session_state['month']
    year = st.session_state['year']

    col = st.columns(2)

    with col[0]:
        st.text("")
        st.markdown(f'**Perolehan siswa Edulab pada tanggal {date-1} {month} {year}**')

        list_students_gain = pd.concat([siswa.iloc[:, date+2], siswa.iloc[:, -1]], axis=1)
        list_students_gain = list_students_gain[list_students_gain.iloc[:,0] != 0]

        explanation = []
        for i in range(len(list_students_gain)):
            explanation.append(f'{int(list_students_gain.iloc[i, 0])} siswa di cabang {list_students_gain.iloc[i, 1]}')
            
        for i in explanation:
            st.markdown(f"{i}")
            
    with col[1]:
        st.text("")
        st.markdown('**Perolehan siswa Edulab pada tanggal ' + st.session_state['long_date'] + '**')

        list_students_gain = pd.concat([siswa.iloc[:, date+3], siswa.iloc[:, -1]], axis=1)
        list_students_gain = list_students_gain[list_students_gain.iloc[:,0] != 0]

        explanation = []
        for i in range(len(list_students_gain)):
            explanation.append(f'{int(list_students_gain.iloc[i, 0])} siswa di cabang {list_students_gain.iloc[i, 1]}')
            
        for i in explanation:
            st.markdown(f"{i}")     

    # # Membagi daftar ke dalam 3 bagian
    # kolom1, kolom2 = st.columns(2)

    # # Looping untuk mengisi setiap kolom secara bergantian
    # for i, nama in enumerate(explanation):
    #     if i % 2 == 0:
    #         kolom1.markdown(f"- {nama}")
    #     elif i % 2 == 1:
    #         kolom2.markdown(f"- {nama}")




        
    fig = px.bar(daily_students_gain, 
            y='hasil', 
            x='tanggal', 
            title=f"Perolehan Siswa Harian Edulab pada Bulan {st.session_state['month']}{st.session_state['year']}",
            labels={'hasil': 'Perolehan Siswa', 'tanggal': 'Tanggal'},
            text='hasil')

    st.plotly_chart(fig)
    
except:           
    st.markdown('Silakan upload file pada menu **Welcome** terlebih dahulu.')
        
