import streamlit as st
import pandas as pd
import requests
import zipfile
import io
from difflib import get_close_matches
from streamlit_option_menu import option_menu

def app():
    st.header('Fundos de Investimento:')
    st.subheader('Informe Diário')
    st.write('O INFORME DIÁRIO é um demonstrativo que contém as seguintes informações do fundo:')
    st.write("Valor total da carteira do fundo, Patrimônio líquido, Valor da cota, Captações realizadas no dia, Resgates pagos no dia, Número de cotistas.")
    st.divider()

    @st.cache_data(ttl=3600)  # Cache the data for 1 hour (3600 seconds)
    def load_data(month):
        # Get info diario
        arquivo = f'inf_diario_fi_{month}.csv'
        link = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{month}.zip'
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

    # Month selection in sidebar
    months = {
        "Janeiro 2021": "202101",
        "Fevereiro 2021": "202102",
        "Março 2021": "202103",
        "Abril 2021": "202104",
        "Maio 2021": "202105",
        "Junho 2021": "202106",
        "Julho 2021": "202107",
        "Agosto 2021": "202108",
        "Setembro 2021": "202109",
        "Outubro 2021": "202110",
        "Novembro 2021": "202111",
        "Dezembro 2021": "202112",
        "Janeiro 2022": "202201",
        "Fevereiro 2022": "202202",
        "Março 2022": "202203",
        "Abril 2022": "202204",
        "Maio 2022": "202205",
        "Junho 2022": "202206",
        "Julho 2022": "202207",
        "Agosto 2022": "202208",
        "Setembro 2022": "202209",
        "Outubro 2022": "202210",
        "Novembro 2022": "202211",
        "Dezembro 2022": "202212",
        "Janeiro 2023": "202301",
        "Fevereiro 2023": "202302",
        "Março 2023": "202303",
        "Abril 2023": "202304",
        "Maio 2023": "202305",
        "Junho 2023": "202306",
        "Julho 2023": "202307",
        "Agosto 2023": "202308",
        "Setembro 2023": "202309",
        "Outubro 2023": "202310",
        "Novembro 2023": "202311",
        "Dezembro 2023": "202312",
        "Janeiro 2024": "202401",
        "Fevereiro 2024": "202402",
        "Março 2024": "202403",
        "Abril 2024": "202404",
        "Maio 2024": "202405",
        "Junho 2024": "202406",
        "Julho 2024": "202407"
    }
    
    selected_month = st.sidebar.selectbox("Selecione o mês", options=list(months.keys()))
    month_code = months[selected_month]

    if f'data_{month_code}' not in st.session_state:
        st.session_state[f'data_{month_code}'] = load_data(month_code)

    df_info_diario = st.session_state[f'data_{month_code}']
    
    # Format the DT_COMPTC column to day-month-year for display
    df_info_diario['DT_COMPTC'] = df_info_diario['DT_COMPTC'].dt.strftime('%d-%m-%Y')
    
    # Initialize session state for filters
    min_date = pd.to_datetime(df_info_diario['DT_COMPTC'], format='%d-%m-%Y').min().date()
    max_date = pd.to_datetime(df_info_diario['DT_COMPTC'], format='%d-%m-%Y').max().date()
    
    if 'search_term' not in st.session_state:
        st.session_state['search_term'] = ''
    if 'selected_types' not in st.session_state:
        st.session_state['selected_types'] = []
    if 'date_range' not in st.session_state:
        st.session_state['date_range'] = (min_date, max_date)
    else:
        # Ensure the date range is within the current month's range
        if st.session_state['date_range'][0] < min_date or st.session_state['date_range'][1] > max_date:
            st.session_state['date_range'] = (min_date, max_date)
    
    # Search box for CNPJ in sidebar
    search_term = st.sidebar.text_input("Pesquisar por CNPJ", st.session_state['search_term'])
    st.session_state['search_term'] = search_term
    
    if search_term:
        search_term = search_term.replace(".", "").replace("/", "").replace("-", "")
        cnpjs = df_info_diario['CNPJ_FUNDO'].str.replace(".", "").str.replace("/", "").str.replace("-", "")
        matches = get_close_matches(search_term, cnpjs, n=10, cutoff=0.1)
        df_info_diario = df_info_diario[df_info_diario['CNPJ_FUNDO'].str.replace(".", "").str.replace("/", "").str.replace("-", "").isin(matches)]
    
    # Slicer for TP_FUNDO in sidebar
    selected_types = st.sidebar.multiselect("Filtrar por Tipo", options=df_info_diario['TP_FUNDO'].unique(), default=st.session_state['selected_types'])
    st.session_state['selected_types'] = selected_types
    
    if selected_types:
        df_info_diario = df_info_diario[df_info_diario['TP_FUNDO'].isin(selected_types)]
    
    # Date slider for DT_COMPTC in sidebar
    start_date, end_date = st.sidebar.date_input("Selecione o intervalo de datas", st.session_state['date_range'], min_value=min_date, max_value=max_date)
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
    
    # Clear all button in sidebar
    if st.sidebar.button('Clear All'):
        st.session_state['search_term'] = ''
        st.session_state['selected_types'] = []
        st.session_state['date_range'] = (min_date, max_date)
        st.experimental_rerun()
    
    # Download filtered data as Excel
    @st.cache_data
    def to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        processed_data = output.getvalue()
        return processed_data

    df_xlsx = to_excel(df_info_diario)

    st.download_button(label='📥 Download Excel',
                       data=df_xlsx,
                       file_name='filtered_data.xlsx',
                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    app()
