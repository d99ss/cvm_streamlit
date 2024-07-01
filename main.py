import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import home
import info_cadastral
import info_diario
import about
import streamlit.components.v1 as components

# Load environment variables from .env file
load_dotenv()

# Set the page title for the Streamlit app
st.set_page_config(page_title="Consulta CVM")

# Your custom HTML with the script tag for monetization
custom_html = """
<!DOCTYPE html>
<html>
<head>
    <!-- Add any additional head content here -->
<meta name="monetag" content="ee258e12eb3275245f01eba2200ba907">
</head>
<body>
<script type="text/javascript">
	atOptions = {
		'key' : '6c5b1b04f6f5f0dff5ab162665d63c36',
		'format' : 'iframe',
		'height' : 600,
		'width' : 160,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//intellectualtimetableindependence.com/6c5b1b04f6f5f0dff5ab162665d63c36/invoke.js"></script>
</body>
</html>
"""

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
        # Sidebar navigation using option_menu
        with st.sidebar:
            components.html(custom_html, height=100)  # Embed the custom HTML in the sidebar
            app = option_menu(
                menu_title='Main Menu',
                options=['Home', 'Cadastro de Fundos', 'Fundos: Informação diária', 'About'],
                icons=['house', 'person-circle', 'clipboard-pulse', 'info-circle'],
                menu_icon='cast',
                default_index=0,  # Default to 'Home' page
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

        # Embed the custom HTML at the bottom of the page
        components.html(custom_html, height=100)

# Embed the custom HTML at the top of the page
components.html(custom_html, height=100)

# Instantiate MultiApp and run the application
if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.run()
