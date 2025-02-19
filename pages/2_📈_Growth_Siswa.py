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
    page_title="Growth Siswa",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
selected_color_theme = 'blues'

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                            legend=None,
                            scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap


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

def separate_by_year(data, columns, column_name):
  data = pd.concat([data.iloc[:,0], data.iloc[:,25], data.iloc[:, columns]], axis=1)
  data.columns = column_name
  return data

branch_list = {
    'branch_list_all': pd.read_csv('data/branch_list.csv', delimiter=';'),
    'region_1': pd.read_csv('data/branch_region_1.csv', delimiter=';'),
    'region_2': pd.read_csv('data/branch_region_2.csv', delimiter=';'),
    'region_3': pd.read_csv('data/branch_region_3.csv', delimiter=';'),
    'region_4': pd.read_csv('data/branch_region_4.csv', delimiter=';')
}

try:
    growth_siswa = st.session_state['growth_siswa']
    
    st.markdown('***Data dibawah ini merupakan data per ' + st.session_state['long_date'] + '**')
    st.text("")
       
    year_list = list([2019, 2020, 2021, 2022, 2023, 2024, 2025])[::-1]
    selected_year = st.selectbox('Pilih Tahun', year_list)
    del year_list[:year_list.index(selected_year)+1]
    year_list.append(2018)
    compared_year = st.selectbox('Pilih Tahun Perbandingan', year_list, index=year_list.index(selected_year-1))
    
    data = {
      2018: separate_by_year(growth_siswa, slice(1,4), ['Kode Cabang', 'Nama Cabang', 'TA 17/18', 'TA 18/20', 'Bulanan']),
      2019: separate_by_year(growth_siswa, slice(4,7), ['Kode Cabang', 'Nama Cabang', 'TA 18/19', 'TA 19/20', 'Bulanan']),
      2020: separate_by_year(growth_siswa, slice(7,10), ['Kode Cabang', 'Nama Cabang', 'TA 19/20', 'TA 20/21', 'Bulanan']),
      2021: separate_by_year(growth_siswa, slice(10,13), ['Kode Cabang', 'Nama Cabang', 'TA 21/22', 'TA 22/23', 'Bulanan']),
      2022: separate_by_year(growth_siswa, slice(13,16), ['Kode Cabang', 'Nama Cabang', 'TA 21/22', 'TA 22/23', 'Bulanan']),
      2023: separate_by_year(growth_siswa, slice(16,19), ['Kode Cabang', 'Nama Cabang', 'TA 22/23', 'TA 23/24', 'Bulanan']),
      2024: separate_by_year(growth_siswa, slice(19,22), ['Kode Cabang', 'Nama Cabang', 'TA 23/24', 'TA 24/25', 'Bulanan']),
      2025: separate_by_year(growth_siswa, slice(22,25), ['Kode Cabang', 'Nama Cabang', 'TA 24/25', 'TA 25/26', 'Bulanan']),
    }
    
    
    
    merged_data = pd.merge(data[selected_year], data[compared_year], on='Kode Cabang', suffixes=('_1', '_2'))
    
    growth_branches = merged_data[merged_data['Bulanan_1'] > merged_data['Bulanan_2']]
     
    st.text("")
    
    def explanation_by_region(data, no_region, region_name):
        
        try:
            data = data[data['Kode Cabang'].isin(branch_list[f"region_{no_region}"]['kode_cabang'])] 
            data = data['Nama Cabang_1'].tolist()
            if len(data) > 1:
                list_growth_branches = ', '.join(data[:-1]) + ', dan ' + data[-1] + "."
            else:
                list_growth_branches = f"{data[0]}."
            
            st.markdown(f"""
            Untuk Wilayah {region_name}, terdapat **{len(data)} cabang** yang memiliki perolehan bulanan lebih besar dari tahun {compared_year}, yaitu {list_growth_branches}
            """)
        except:
            st.markdown(f"""
            Untuk Wilayah {region_name}, tidak terdapat cabang yang memiliki perolehan bulanan lebih besar dari tahun {compared_year}.
            """)
        
    st.markdown(f"""
    Per tanggal {st.session_state['long_date'][:-4]} {selected_year}, total cabang yang memiliki perolehan bulanan lebih besar dari tahun {compared_year} adalah **{len(growth_branches)} cabang**.
    """)
    explanation_by_region(growth_branches, 1, 'Jawa Barat')
    explanation_by_region(growth_branches, 2, 'Sumatera & Kalimantan')
    explanation_by_region(growth_branches, 3, 'Indonesia Timur')
    explanation_by_region(growth_branches, 4, 'Jateng & Jatim')
    st.text("")
    
    
    # df_heatmap = growth_siswa
    # df_heatmap = growth_siswa
    
    # heatmap = make_heatmap(df_heatmap, 'tahun', 'nama_cabang', 'bulanan', selected_color_theme)
    
    # st.table(pd.concat([data[selected_year], data[compared_year]], axis=1))
    
    # st.bar_chart(pd.concat([data[selected_year], data[compared_year]]),
    #              x='Nama Cabang',
    #              y='Bulanan',
    #              horizontal=True)
        
    col = st.columns(2, gap='medium')

    with col[0]:
        data[compared_year].index = data[compared_year].index + 1
        st.markdown(f'#### {compared_year}')
        st.table(data[compared_year].iloc[:, 1:])

    with col[1]:
        data[selected_year].index = data[selected_year].index + 1
        st.markdown(f'#### {selected_year}')  
        st.table(data[selected_year].iloc[:, 1:])
    
        
except:
    st.markdown('Silakan upload file pada menu **Welcome** terlebih dahulu.')