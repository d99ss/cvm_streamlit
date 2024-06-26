import streamlit as st
import pandas as pd
import requests
import zipfile
import io
from difflib import get_close_matches
from st_aggrid import AgGrid, GridOptionsBuilder
from agstyler import PINLEFT, PRECISION_TWO, draw_grid
from streamlit_option_menu import option_menu

def app():
    st.title('Fundos de Investimento: Informe Diário')
    st.write('O INFORME DIÁRIO é um demonstrativo que contém as seguintes informações do fundo, relativas à data de competência:')
    st.write("Valor total da carteira do fundo, Patrimônio líquido, Valor da cota, Captações realizadas no dia, Resgates pagos no dia, Número de cotistas")
    st.divider()

    @st.cache_data(persist=True)
    def load_data():
        # Get info diario
        arquivo = 'inf_diario_fi_202307.csv'
        link = 'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_202307.zip'
        r_info_diario = requests.get(link)
        zf = zipfile.ZipFile(io.BytesIO(r_info_diario.content))
        zf = zf.open(arquivo)
        lines = zf.readlines()
        lines = [i.strip().decode('ISO-8859-1') for i in lines]
        lines = [i.split(';') for i in lines]
        df_info_diario = pd.DataFrame(lines[1:], columns=lines[0])

        # Convert date column to datetime
        df_info_diario['DT_COMPTC'] = pd.to_datetime(df_info_diario['DT_COMPTC'], format='%Y-%m-%d')
        
        return df_info_diario

    df_info_diario = load_data()
    
    # Format the DT_COMPTC column to day-month-year for display
    df_info_diario['DT_COMPTC'] = df_info_diario['DT_COMPTC'].dt.strftime('%d-%m-%Y')
    
    # Initialize session state for filters
    if 'search_term' not in st.session_state:
        st.session_state['search_term'] = ''
    if 'selected_types' not in st.session_state:
        st.session_state['selected_types'] = []
    if 'date_range' not in st.session_state:
        min_date = pd.to_datetime(df_info_diario['DT_COMPTC'], format='%d-%m-%Y').min().date()
        max_date = pd.to_datetime(df_info_diario['DT_COMPTC'], format='%d-%m-%Y').max().date()
        st.session_state['date_range'] = (min_date, max_date)
    
    # Search box for CNPJ
    search_term = st.text_input("Search for CNPJ", st.session_state['search_term'])
    st.session_state['search_term'] = search_term
    
    if search_term:
        search_term = search_term.replace(".", "").replace("/", "").replace("-", "")
        cnpjs = df_info_diario['CNPJ_FUNDO'].str.replace(".", "").str.replace("/", "").str.replace("-", "")
        matches = get_close_matches(search_term, cnpjs, n=10, cutoff=0.1)
        df_info_diario = df_info_diario[df_info_diario['CNPJ_FUNDO'].str.replace(".", "").str.replace("/", "").str.replace("-", "").isin(matches)]
    
    # Slicer for TP_FUNDO
    selected_types = st.multiselect("Filter by TP_FUNDO", options=df_info_diario['TP_FUNDO'].unique(), default=st.session_state['selected_types'])
    st.session_state['selected_types'] = selected_types
    
    if selected_types:
        df_info_diario = df_info_diario[df_info_diario['TP_FUNDO'].isin(selected_types)]
    
    # Date slider for DT_COMPTC
    min_date = pd.to_datetime(df_info_diario['DT_COMPTC'], format='%d-%m-%Y').min().date()
    max_date = pd.to_datetime(df_info_diario['DT_COMPTC'], format='%d-%m-%Y').max().date()
    start_date, end_date = st.date_input("Select date range", st.session_state['date_range'], min_value=min_date, max_value=max_date)
    st.session_state['date_range'] = (start_date, end_date)
    
    # Convert selected dates to datetime for filtering
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
    
    # Ensure DT_COMPTC is converted back to datetime before filtering
    df_info_diario['DT_COMPTC'] = pd.to_datetime(df_info_diario['DT_COMPTC'], format='%d-%m-%Y')
    
    df_info_diario = df_info_diario[(df_info_diario['DT_COMPTC'] >= start_date) & 
                                    (df_info_diario['DT_COMPTC'] <= end_date)]
    
    # Format the DT_COMPTC column back to day-month-year for display
    df_info_diario['DT_COMPTC'] = df_info_diario['DT_COMPTC'].dt.strftime('%d-%m-%Y')
    
    st.write(df_info_diario)
    
    # Clear all button
    if st.button('Clear all'):
        st.session_state['search_term'] = ''
        st.session_state['selected_types'] = []
        st.session_state['date_range'] = (min_date, max_date)
        st.experimental_rerun()
    
    # Download filtered data as Excel
    @st.cache_data
    def to_excel(df):
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
        processed_data = output.getvalue()
        return processed_data

    df_xlsx = to_excel(df_info_diario)

    st.download_button(label='📥 Download Current Data as Excel',
                       data=df_xlsx,
                       file_name='filtered_data.xlsx')

if __name__ == "__main__":
    app()
