import streamlit as st
import home
import info_cadastral
import info_diario

# Set the page title and layout for the Streamlit app
st.set_page_config(page_title="Consulta CVM", layout="wide", initial_sidebar_state="auto")

# Define the Streamlit app pages using st.Page
home_page = st.Page(home.app, title="Home", icon="🏚️")
cadastral_page = st.Page(info_cadastral.cadastral_page, title="Cadastro de Fundos", icon="📋")
diario_page = st.Page(info_diario.diario_page, title="Fundos: Informação diária", icon="📉")

# Use st.navigation for the navigation menu
pg = st.navigation([home_page, cadastral_page, diario_page])

# Run the selected page
pg.run()
