
# home.py
import streamlit as st
from streamlit_option_menu import option_menu

def app():
    st.title("Home Page")
    st.write("A consulta aos Fundos de Investimento registrados na CVM pode ser feita por CNPJ ou por parte do nome do fundo.")
    st.write("Podem ser obtidas todas as informações públicas dos fundos, tais como o valor diário da cota e do patrimônio líquido, o número de cotistas, valores captados e resgatados. Ainda é possível consultar o Regulamento, o Prospecto, a Lâmina de Informações essenciais, a Composição da carteira, os Fatos Relevantes e os Balancetes de cada Fundo.")
    st.write("Consulte, através dos ícones abaixo, os Fundos de Investimento registrados na CVM e os cancelados (disponíveis na Central de Sistemas.")
    # Add more Streamlit components as needed
