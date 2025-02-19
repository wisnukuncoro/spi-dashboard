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

def load_data(all_sheets, sheet_name, rows, cols):
        data = all_sheets[sheet_name].iloc[rows,cols]
        return data
    
def filter_active_branch(data):
    data = data[data['kode_cabang'].isin(branch_list['kode_cabang'])]   
    return data

if excel is not None:
    
    all_sheets = pd.read_excel(excel, sheet_name=None)

    long_date = load_data(all_sheets, 'Jumlah Siswa', slice(0,1), slice(3,4)).iloc[0,0]
    year = long_date[-4:]
    
    if long_date[1] == ' ':
        date = long_date[0]
        month = long_date[2:-4]
    else:
        date = long_date[0:2]
        month = long_date[3:-4]
    
    if long_date[-4:] != '2025':
        st.markdown("""
        **Error!**
        Web ini hanya dapat memproses jika data yang diinput merupakan data tahun 2025.           
        """)
    else:
        st.markdown("""
        **Upload file sukses!**                
        Silakan pilih menu di samping untuk melihat visualisasi data.
        """)
            
        ### Page 1 Data Preparation
        
        num_of_students = load_data(all_sheets, 'Jumlah Siswa', slice(3, None), slice(2, 96))
        num_of_students = pd.concat([num_of_students.iloc[:,0], num_of_students.iloc[:,79:]], axis=1)
        num_of_students.columns = ['kode_cabang', '1_smt_24', '2_smt_24', '3_smt_24', 'intensif', 'beasiswa', 'total_reg_24', 'private_24', 'kapasitas_24', 'percent_24', '1_smt_25', '2_smt_25', '3_smt_25', 'total_reg_25', 'kapasitas_25', 'percent_25']
        num_of_students = num_of_students[num_of_students['kode_cabang'].isin(branch_list['kode_cabang'])]   
        
        num_of_students = pd.merge(num_of_students, branch_list, on='kode_cabang')
        num_of_students = num_of_students.fillna(0)
        
        
        ### Page 2 Data Preparation
        
        growth_siswa = load_data(all_sheets, 'Growth Siswa', slice(2, None), slice(3, 29))
        growth_siswa.drop(growth_siswa.columns[1], axis=1, inplace=True)
        growth_siswa.columns = ['kode_cabang', 'ta_17_18_2018', 'ta_18_19_2018', 'bulanan_2018', 'ta_18_19_2019', 'ta_19_20_2019', 'bulanan_2019', 'ta_19_20_2020', 'ta_20_21_2020', 'bulanan_2020', 'ta_21_22_2021', 'ta_22_23_2021', 'bulanan_2021', 'ta_21_22_2022', 'ta_22_23_2022', 'bulanan_2022', 'ta_22_23_2023', 'ta_23_24_2023', 'bulanan_2023', 'ta_23_24_2024', 'ta_24_25_2024', 'bulanan_2024', 'ta_24_25_2025', 'ta_25_26_2025', 'bulanan']
        
        growth_siswa = filter_active_branch(growth_siswa)
        growth_siswa = pd.merge(growth_siswa, branch_list, on='kode_cabang')
        
        
        ### Page 3 Data Preparation
        if month == 'Januari' or month == 'Maret' or month == 'Mei' or month == 'Juli' or month == 'Agustus' or month == 'Oktober' or month == 'Desember':
            list_date = [str(i) for i in range(1, 32)]
        elif month == 'April' or month == 'Juni' or month == 'September' or month == 'November':
            list_date = [str(i) for i in range(1, 31)]
        else:
            list_date = [str(i) for i in range(1, 29)]
               
        siswa = load_data(all_sheets, 'Siswa ', slice(2, None), slice(1, len(list_date)+8))
        siswa.drop(siswa.columns[[1,2,6]], axis=1, inplace=True)
                    
        columns_siswa = ['kode_cabang', 'hasil', 'target', 'percentage']
        
        siswa.columns = columns_siswa + list_date
        siswa = filter_active_branch(siswa)
        siswa = pd.merge(siswa, branch_list, on='kode_cabang')
        
        
        ### Page 4 Data Preparation
        revenue = load_data(all_sheets, 'Revenue', slice(64, 67), slice(4, 6))
        
        st.session_state['date'] = date
        st.session_state['month'] = month 
        st.session_state['year'] = year     
        st.session_state['long_date'] = long_date
        st.session_state['num_of_students'] = num_of_students
        st.session_state['growth_siswa'] = growth_siswa
        st.session_state['siswa'] = siswa
        st.session_state['num_of_dates'] = len(list_date)
        st.session_state['revenue'] = revenue