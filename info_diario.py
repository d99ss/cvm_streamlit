# info_diario.py
import streamlit as st
import pandas as pd
import requests
import zipfile
import io
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


        return df_info_diario

    df_info_diario = load_data()
    
    st.write(df_info_diario)