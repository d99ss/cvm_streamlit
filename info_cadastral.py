import streamlit as st
import pandas as pd
from difflib import get_close_matches
import io


def cadastral_page():
    st.header('Fundos de Investimento:')
    st.subheader('Informação Cadastral')
    st.write("Dados cadastrais de fundos de investimento estruturados e não estruturados (ICVM 555), tais como: CNPJ, data de registro e situação do fundo.")
    st.divider()

    @st.cache_data(ttl=3600)
    def load_data():
        url = 'https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv'

        # Specify only the columns you need
        usecols = [
            "TP_FUNDO",
            "CNPJ_FUNDO",
            "DENOM_SOCIAL",
            "DT_REG",
            "DT_CONST",
            "DT_CANCEL",
            "SIT",
            "DT_INI_SIT",
            "DT_INI_ATIV",
            "DT_FIM_EXERC",
            "CLASSE",
            "DT_INI_CLASSE",
            "VL_PATRIM_LIQ",
            "DT_PATRIM_LIQ",
            "ADMIN",
            "GESTOR",
            "CNPJ_AUDITOR",
            "AUDITOR",
            "CNPJ_CUSTODIANTE",
            "CUSTODIANTE",
            "CNPJ_CONTROLADOR",
            "CONTROLADOR",
            "CLASSE_ANBIMA"
        ]

        # Define dtypes for the columns
        dtypes = {
            "TP_FUNDO": "string",
            "CNPJ_FUNDO": "string",
            "DENOM_SOCIAL": "string",
            "DT_REG": "string",  # Dates will be converted later
            "DT_CONST": "string",
            "DT_CANCEL": "string",
            "SIT": "category",
            "DT_INI_SIT": "string",
            "DT_INI_ATIV": "string",
            "DT_FIM_EXERC": "string",
            "CLASSE": "category",
            "DT_INI_CLASSE": "string",
            "VL_PATRIM_LIQ": "float64",
            "DT_PATRIM_LIQ": "string",
            "ADMIN": "string",
            "GESTOR": "string",
            "CNPJ_AUDITOR": "string",
            "AUDITOR": "string",
            "CNPJ_CUSTODIANTE": "string",
            "CUSTODIANTE": "string",
            "CNPJ_CONTROLADOR": "string",
            "CONTROLADOR": "string",
            "CLASSE_ANBIMA": "category"
        }

        # Load the data with specified columns and dtypes
        data = pd.read_csv(url, sep=';', encoding='latin1',
                           usecols=usecols, dtype=dtypes)

        # Convert DT_REG to datetime for filtering and keep it as a datetime object
        date_columns = ["DT_REG", "DT_CONST", "DT_CANCEL", "DT_INI_SIT",
                        "DT_INI_ATIV", "DT_FIM_EXERC", "DT_INI_CLASSE", "DT_PATRIM_LIQ"]
        for col in date_columns:
            data[col] = pd.to_datetime(
                data[col], format='%Y-%m-%d', errors='coerce')

        return data

    def apply_filters(data):
        # Move filters to the sidebar
        with st.sidebar:
            # Filter by TP_FUNDO using a selectbox
            tp_fundo_options = data['TP_FUNDO'].unique().tolist()
            selected_tp_fundo = st.selectbox("Filtrar por Tipo", options=[
                                             "All"] + tp_fundo_options)

            # Filter by SIT using a selectbox
            sit_options = data['SIT'].unique().tolist()
            selected_sit = st.selectbox(
                "Selecione a situação", options=["All"] + sit_options)

            # Search by CNPJ_FUNDO
            cnpj_search = st.text_input("Pesquisar por CNPJ")

            # Search by DENOM_SOCIAL with approximate matching
            denom_social_search = st.text_input("Pesquisar por Nome do Fundo")

            # Date range filter in sidebar
            min_date = data['DT_REG'].min().date()  # Min date as date object
            max_date = data['DT_REG'].max().date()  # Max date as date object
            start_date, end_date = st.date_input(
                "Selecione o intervalo de datas",
                value=[min_date, max_date],  # Set default range
                min_value=min_date,  # Set minimum date
                max_value=max_date,  # Set maximum date,
                format="DD/MM/YYYY"  # Date format
            )

        # Apply the filter for TP_FUNDO
        if selected_tp_fundo != "All":
            data = data[data['TP_FUNDO'] == selected_tp_fundo]

        # Apply the filter for SIT
        if selected_sit != "All":
            data = data[data['SIT'] == selected_sit]

        # Apply the search for CNPJ_FUNDO
        if cnpj_search:
            data = data[data['CNPJ_FUNDO'].str.contains(cnpj_search)]

        # Apply the search for DENOM_SOCIAL with approximate matching
        if denom_social_search:
            # Get a list of close matches
            close_matches = get_close_matches(
                denom_social_search.upper(), data['DENOM_SOCIAL'], n=10, cutoff=0.3)
            if close_matches:
                data = data[data['DENOM_SOCIAL'].isin(close_matches)]

        # Apply the date range filter
        if start_date and end_date:
            data = data[(data['DT_REG'] >= pd.to_datetime(start_date)) & (
                data['DT_REG'] <= pd.to_datetime(end_date))]

        return data

    # Load data
    data = load_data()

    # Apply filters after data is loaded
    filtered_data = apply_filters(data)

    # Convert date columns back to string format for display purposes
    date_columns = ["DT_REG", "DT_CONST", "DT_CANCEL", "DT_INI_SIT",
                    "DT_INI_ATIV", "DT_FIM_EXERC", "DT_INI_CLASSE", "DT_PATRIM_LIQ"]
    for col in date_columns:
        filtered_data[col] = filtered_data[col].dt.strftime('%d-%m-%Y')

    # Display the data in a Streamlit dataframe
    st.dataframe(filtered_data, hide_index=True, height=1000, use_container_width=True)

    # Function to download the filtered data as an Excel file
    def download_excel(data):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Filtered Data')
        output.seek(0)
        return output

    # Display download button for filtered data
    st.download_button(
        label="📥 Download Excel",
        data=download_excel(filtered_data),
        file_name='filtered_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
