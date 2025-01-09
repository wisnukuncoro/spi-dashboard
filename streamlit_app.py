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
    page_title="SPI Dashboard",
    page_icon="🏂",
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


#######################
# Load data
df_reshaped = pd.read_csv('data/us-population-2010-2019-reshaped.csv')


#######################
# Sidebar
# with st.sidebar:
#     st.title('SPI Dashboard')
    
#     year_list = list(df_reshaped.year.unique())[::-1]
    
#     selected_year = st.selectbox('Pilih Tahun', year_list)
#     df_selected_year = df_reshaped[df_reshaped.year == selected_year]
#     df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

#     color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
#     selected_color_theme = st.selectbox('Pilih Tema Warna', color_theme_list)


#######################
# Plots

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

# Choropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                              color_continuous_scale=input_color_theme,
                              range_color=(0, max(df_selected_year.population)),
                              scope="usa",
                              labels={'population':'Population'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)

def load_data(sheet, cols, rows, nrows):
        uploaded_file = st.file_uploader("Upload File Excel File", type="xlsx")
        if uploaded_file is not None:
            data = pd.read_excel(uploaded_file, sheet_name=sheet, usecols=cols, skiprows=rows, nrows=nrows)
            return data
        return None
      
branch_list = pd.read_csv('data/branch_list.csv', delimiter=';')
branch_region_1 = pd.read_csv('data/branch_region_1.csv', delimiter=';')
branch_region_2 = pd.read_csv('data/branch_region_2.csv', delimiter=';')
branch_region_3 = pd.read_csv('data/branch_region_3.csv', delimiter=';')
branch_region_4 = pd.read_csv('data/branch_region_4.csv', delimiter=';')
      
#######################
# Dashboard Main Panel

jumlah_siswa = load_data('Jumlah Siswa', 'C:CR', 3, 69)

if jumlah_siswa is not None:
  
    jumlah_siswa = pd.concat([jumlah_siswa.iloc[:,0], jumlah_siswa.iloc[:,79:]], axis=1)
    jumlah_siswa.columns = ['kode_cabang', '1_smt_24', '2_smt_24', '3_smt_24', 'intensif', 'beasiswa', 'total_reg_24', 'private_24', 'kapasitas_24', 'percent_24', '1_smt_25', '2_smt_25', '3_smt_25', 'total_reg_25', 'kapasitas_25', 'percent_25']

    jumlah_siswa = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_list['kode_cabang'])]

    jumlah_siswa = pd.merge(jumlah_siswa, branch_list, on='kode_cabang')
    jumlah_siswa = jumlah_siswa.fillna(0)
    jumlah_siswa_wilayah_1 = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_region_1['kode_cabang'])]
    jumlah_siswa_wilayah_2 = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_region_2['kode_cabang'])]
    jumlah_siswa_wilayah_3 = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_region_3['kode_cabang'])]
    jumlah_siswa_wilayah_4 = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_region_4['kode_cabang'])]

    st.markdown("#### Tabel Jumlah Siswa")
    
    st.write(jumlah_siswa_wilayah_1)
    
    year_list = list(df_reshaped.year.unique())[::-1]
        
    selected_year = st.selectbox('Pilih Tahun Ajaran', year_list)
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Pilih Tema Warna', color_theme_list)
    
    st.markdown('#### Jumlah Siswa di Seluruh Cabang Edulab')
        
    col = st.columns(2, gap='medium')

    with col[0]:
                
        # total_ta_24 = int(jumlah_siswa['total_reg_24'].sum())
        # total_ta_25 = int(jumlah_siswa['total_reg_25'].sum())

        # st.metric(label='Total Siswa Tahun Ajaran 2024/2025', value=total_ta_24)

        # st.metric(label='Total Siswa Tahun Ajaran 2025/2026', value=total_ta_25)
        
        fig = px.bar(jumlah_siswa_wilayah_2, 
             y='nama_cabang', 
             x='total_reg_24', 
             title='Jumlah Siswa di Cabang Wilayah Jawa Barat',
             labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
             text='total_reg_24',)  # Menambahkan label pada setiap batang

        # Menampilkan grafik di Streamlit
        st.plotly_chart(fig)


    with col[1]:
               
        # choropleth = make_choropleth(df_selected_year, 'states_code', 'population', selected_color_theme)
        # st.plotly_chart(choropleth, use_container_width=True)
        
        fig = px.bar(jumlah_siswa_wilayah_1, 
             y='nama_cabang', 
             x='total_reg_24', 
             title='Jumlah Siswa di Cabang Wilayah Sumatera & Kalimantan',
             labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
             text='total_reg_24')  # Menambahkan label pada setiap batang

        # Menampilkan grafik di Streamlit
        st.plotly_chart(fig)
        
        # fig = px.bar(jumlah_siswa_wilayah_2, 
        #      y='nama_cabang', 
        #      x='total_reg_24', 
        #      title='Total Pendaftar per Cabang',
        #      labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
        #      text='total_reg_24',)  # Menambahkan label pada setiap batang

        # # Menampilkan grafik di Streamlit
        # st.plotly_chart(fig)
        
        # fig = px.bar(jumlah_siswa_wilayah_3, 
        #      y='nama_cabang', 
        #      x='total_reg_24', 
        #      title='Total Pendaftar per Cabang',
        #      labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
        #      text='total_reg_24',)  # Menambahkan label pada setiap batang

        # # Menampilkan grafik di Streamlit
        # st.plotly_chart(fig)
        
        # fig = px.bar(jumlah_siswa_wilayah_4, 
        #      y='nama_cabang', 
        #      x='total_reg_24', 
        #      title='Total Pendaftar per Cabang',
        #      labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
        #      text='total_reg_24',)  # Menambahkan label pada setiap batang

        # # Menampilkan grafik di Streamlit
        # st.plotly_chart(fig)
        
        # heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', selected_color_theme)
        # st.altair_chart(heatmap, use_container_width=True)
        
        
    col = st.columns(2, gap='medium')

    with col[0]:
                
        # total_ta_24 = int(jumlah_siswa['total_reg_24'].sum())
        # total_ta_25 = int(jumlah_siswa['total_reg_25'].sum())

        # st.metric(label='Total Siswa Tahun Ajaran 2024/2025', value=total_ta_24)

        # st.metric(label='Total Siswa Tahun Ajaran 2025/2026', value=total_ta_25)
        
        fig = px.bar(jumlah_siswa_wilayah_3, 
             y='nama_cabang', 
             x='total_reg_24', 
             title='Jumlah Siswa di Cabang Wilayah Indonesia Timur',
             labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
             text='total_reg_24',)  # Menambahkan label pada setiap batang

        # Menampilkan grafik di Streamlit
        st.plotly_chart(fig)


    with col[1]:
               
        # choropleth = make_choropleth(df_selected_year, 'states_code', 'population', selected_color_theme)
        # st.plotly_chart(choropleth, use_container_width=True)
        
        fig = px.bar(jumlah_siswa_wilayah_4, 
             y='nama_cabang', 
             x='total_reg_24', 
             title='Jumlah Siswa di Cabang Wilayah Jateng & Jatim',
             labels={'nama_cabang': 'Nama Cabang', 'total_reg_24': 'Total Pendaftar'},
             text='total_reg_24')  # Menambahkan label pada setiap batang

        # Menampilkan grafik di Streamlit
        st.plotly_chart(fig)    

    # with col3:
    #     st.markdown('#### Top Cabang')

    #     st.dataframe(df_selected_year_sorted,
    #                 column_order=("total_reg_, "population"),
    #                 hide_index=True,
    #                 width=None,
    #                 column_config={
    #                     "states": st.column_config.TextColumn(
    #                         "Cabang",
    #                     ),
    #                     "population": st.column_config.ProgressColumn(
    #                         "Jumlah Siswa",
    #                         format="%f",
    #                         min_value=0,
    #                         max_value=max(df_selected_year_sorted.population),
    #                     )}
    #                 )
        
    #     # with st.expander('About', expanded=True):
    #     #     st.write('''
    #     #         - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
    #     #         - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
    #     #         - :orange[**States Migration**]: percent_ge of states with annual inbound/ outbound migration > 50,000
    #     #         ''')