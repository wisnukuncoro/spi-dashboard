import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Hello!",
    page_icon="👋",
)

st.write("# SPI Edulab Indonesia 📊")

excel = st.file_uploader("Masukkan file excel")

branch_list = pd.read_csv('data/branch_list.csv', delimiter=';')
branch_region_1 = pd.read_csv('data/branch_region_1.csv', delimiter=';')
branch_region_2 = pd.read_csv('data/branch_region_2.csv', delimiter=';')
branch_region_3 = pd.read_csv('data/branch_region_3.csv', delimiter=';')
branch_region_4 = pd.read_csv('data/branch_region_4.csv', delimiter=';')    

if excel is not None:
    
    st.markdown("""
    **Upload file sukses!**                
    Silakan pilih menu di samping untuk melihat visualisasi data.
    """)
    
    all_sheets = pd.read_excel(excel, sheet_name=None)
    
    def load_data(sheet_name, rows, cols):
        data = all_sheets[sheet_name].iloc[rows,cols]
        return data
    
    def filter_active_branch(data):
        data = data[data['kode_cabang'].isin(branch_list['kode_cabang'])]   
        return data
    
    ### Page 1 Data Preparation
    
    jumlah_siswa = load_data('Jumlah Siswa', slice(3, None), slice(2, 96))
    jumlah_siswa = pd.concat([jumlah_siswa.iloc[:,0], jumlah_siswa.iloc[:,79:]], axis=1)
    jumlah_siswa.columns = ['kode_cabang', '1_smt_24', '2_smt_24', '3_smt_24', 'intensif', 'beasiswa', 'total_reg_24', 'private_24', 'kapasitas_24', 'percent_24', '1_smt_25', '2_smt_25', '3_smt_25', 'total_reg_25', 'kapasitas_25', 'percent_25']
    jumlah_siswa = jumlah_siswa[jumlah_siswa['kode_cabang'].isin(branch_list['kode_cabang'])]   
    
    jumlah_siswa = pd.merge(jumlah_siswa, branch_list, on='kode_cabang')
    jumlah_siswa = jumlah_siswa.fillna(0)
    
    
    ### Page 2 Data Preparation
    
    growth_siswa = load_data('Growth Siswa', slice(2, None), slice(3, 31))
    growth_siswa.drop(growth_siswa.columns[[1]], axis=1, inplace=True)
    growth_siswa.columns = ['kode_cabang', 'ta_17_18_2018', 'ta_18_19_2018', 'bulanan_2018', 'ta_18_19_2019', 'ta_19_20_2019', 'bulanan_2019', 'ta_19_20_2020', 'ta_20_21_2020', 'bulanan_2020', 'ta_21_22_2021', 'ta_22_23_2021', 'bulanan_2021', 'ta_21_22_2022', 'ta_22_23_2022', 'bulanan_2022', 'ta_22_23_2023', 'ta_23_24_2023', 'ta_24_25_2023', 'bulanan_2023', 'ta_23_24_2024', 'ta_24_25_2024', 'ta_25_26_2024', 'bulanan_2024', 'ta_24_25_2025', 'ta_25_26_2025', 'bulanan']
    
    growth_siswa = filter_active_branch(growth_siswa)
    growth_siswa = pd.merge(growth_siswa, branch_list, on='kode_cabang')
              
    st.session_state['jumlah_siswa'] = jumlah_siswa
    st.session_state['growth_siswa'] = growth_siswa
    st.session_state['file_uploaded'] = True
    
else:
    st.session_state['file_uploaded'] = False
    

    

    

    

    


    
    

      
  