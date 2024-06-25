import streamlit as st
import pandas as pd
import time
import requests
import zipfile
import io
from st_aggrid import AgGrid
from st_aggrid import AgGrid, GridOptionsBuilder
from agstyler import PINLEFT, PRECISION_TWO, draw_grid
from streamlit_option_menu import option_menu


def app():
    st.title('Fundos de Investimento: Informação Cadastral')
    st.write("Dados cadastrais de fundos de investimento estruturados e não estruturados (ICVM 555), tais como: CNPJ, data de registro e situação do fundo.")
    st.divider()


    # Get info cadastral

    @st.cache_data(persist=True)
    def load_data():
        start_time = time.time()
        r = requests.get('https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv')
        lines = [i.strip().split(';') for i in r.text.split('\n')]
        data = pd.DataFrame(lines[1:], columns=lines[0])
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        print(f"Elapsed time: {elapsed_time/60:.2f} minutes")


        """data = pd.read_excel(
            "C:/Users/david/OneDrive/Desktop/Miza/streamlit/cad_fi.xlsx", parse_dates=['DT_REG'])"""
        return data

    data = load_data()

    gb = GridOptionsBuilder()

    # makes columns resizable, sortable and filterable by default
    gb.configure_default_column(
        resizable=True,
        filterable=True,
        sortable=True,
        editable=False,
    )

    AgGrid(data, height=400)
