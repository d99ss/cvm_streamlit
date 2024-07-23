import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import home
import info_cadastral
import info_diario
import about

# Load environment variables from .env file
load_dotenv()

# Set the page title and layout for the Streamlit app
st.set_page_config(page_title="Consulta CVM", layout="wide")

# Function to run the Streamlit app with multi-page navigation
class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Main menu navigation using option_menu with horizontal orientation
        app = option_menu(
            menu_title='',
            options=['Home', 'Cadastro de Fundos', 'Fundos: Informação diária', 'About'],
            icons=['house', 'person-circle', 'clipboard-pulse', 'info-circle'],
            menu_icon='cast',
            default_index=0,  # Default to 'Home' page
            orientation='horizontal',  # Set orientation to horizontal
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "green"},
            }
        )

        # Display selected app based on option_menu selection
        if app == "Home":
            home.app()
        elif app == "Fundos: Informação diária":
            info_diario.app()
        elif app == "Cadastro de Fundos":
            info_cadastral.app()
        elif app == 'About':
            about.app()

# Instantiate MultiApp and run the application
if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.run()
