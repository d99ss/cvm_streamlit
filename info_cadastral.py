import streamlit as st
import pandas as pd
import time
import requests
from streamlit_option_menu import option_menu
import io

def app():
    st.header('Fundos de Investimento:')
    st.subheader('Informação Cadastral')
    st.write("Dados cadastrais de fundos de investimento estruturados e não estruturados (ICVM 555), tais como: CNPJ, data de registro e situação do fundo.")
    st.divider()

    # Get info cadastral
    @st.cache_data(ttl=60)  # Cache the data for 60 seconds
    def load_data():
        start_time = time.time()
        r = requests.get('https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv')
        lines = [i.decode('latin1').strip().split(';') for i in r.iter_lines()]
        data = pd.DataFrame(lines[1:], columns=lines[0])
        
        # Remove specified columns
        data = data.drop(columns=['DT_CONST', 'CD_CVM', 'DT_INI_EXERC', 'DIRETOR'])
        
        # Convert date columns to datetime format for sorting
        date_columns = ['DT_REG', 'DT_CANCEL', 'DT_INI_SIT', 'DT_INI_ATIV', 'DT_FIM_EXERC', 'DT_INI_CLASSE', 'DT_PATRIM_LIQ']
        for col in date_columns:
            data[col] = pd.to_datetime(data[col], format='%Y-%m-%d', errors='coerce')
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        return data

    data = load_data()

    # State management for filters
    if "start_date" not in st.session_state:
        st.session_state.start_date = data['DT_REG'].min()
    if "end_date" not in st.session_state:
        st.session_state.end_date = data['DT_REG'].max()
    if "selected_fund_type" not in st.session_state:
        st.session_state.selected_fund_type = "All"
    if "search_term" not in st.session_state:
        st.session_state.search_term = ""
    if "selected_sit" not in st.session_state:
        st.session_state.selected_sit = "All"
    

    # Date range filter in sidebar
    start_date, end_date = st.sidebar.date_input("Selecione o intervalo de datas", [st.session_state.start_date, st.session_state.end_date], min_value=data['DT_REG'].min(), max_value=data['DT_REG'].max())

    if start_date is not None and end_date is not None:
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        mask = (data['DT_REG'] >= pd.to_datetime(start_date)) & (data['DT_REG'] <= pd.to_datetime(end_date))
        filtered_data = data.loc[mask]
    else:
        filtered_data = data

    # Filter by TP_FUNDO in sidebar
    fund_types = filtered_data['TP_FUNDO'].unique().tolist()
    fund_types.insert(0, "All")  # Add 'All' option to the list
    selected_fund_type = st.sidebar.selectbox("Filtrar por Tipo", options=fund_types, index=fund_types.index(st.session_state.selected_fund_type))
    
    if selected_fund_type != "All":
        st.session_state.selected_fund_type = selected_fund_type
        filtered_data = filtered_data[filtered_data['TP_FUNDO'] == selected_fund_type]
    else:
        filtered_data = filtered_data[filtered_data['TP_FUNDO'].isin(fund_types)]

    # Filter by SIT in sidebar
    sit_options = filtered_data['SIT'].unique().tolist()
    sit_options.insert(0, "All")  # Add 'All' option to the list
    selected_sit = st.sidebar.selectbox("Selecione a situação", options=sit_options, index=sit_options.index(st.session_state.selected_sit))
    
    if selected_sit != "All":
        st.session_state.selected_sit = selected_sit
        filtered_data = filtered_data[filtered_data['SIT'] == selected_sit]
    else:
        filtered_data = filtered_data[filtered_data['SIT'].isin(sit_options)]

    # Search by CNPJ_FUNDO in sidebar
    st.sidebar.write("### Search by CNPJ")
    search_term = st.sidebar.text_input("Enter CNPJ", value=st.session_state.search_term)
    
    if search_term:
        st.session_state.search_term = search_term
        filtered_data = filtered_data[filtered_data['CNPJ_FUNDO'].str.contains(search_term, case=False, na=False)]

    # Create a copy of the filtered dataframe for display with formatted dates
    display_filtered_data = filtered_data.copy()
    for col in display_filtered_data.columns:
        if col.startswith('DT_'):
            display_filtered_data[col] = display_filtered_data[col].dt.strftime('%d-%m-%Y')

    # Display the most recent date in the DT_REG column
    most_recent_date = data['DT_REG'].max()
    st.write(f"The most recent date in the dataset is: {most_recent_date.strftime('%d-%m-%Y')}")

    # Display the filtered DataFrame using st.write
    st.write(display_filtered_data)
    
    # Clear all filters in sidebar
    if st.sidebar.button("Clear All"):
        st.session_state.start_date = data['DT_REG'].min()
        st.session_state.end_date = data['DT_REG'].max()
        st.session_state.selected_fund_type = "All"
        st.session_state.search_term = ""
        st.session_state.selected_sit = "All"
        st.experimental_rerun()

    # Download the filtered data as an Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        filtered_data.to_excel(writer, index=False, sheet_name='Filtered Data')
    output.seek(0)
    st.download_button(
        label='📥 Download Excel',
        data=output,
        file_name='filtered_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Call the app function to run the Streamlit app
if __name__ == "__main__":
    app()
