import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import home
import info_cadastral
import info_diario
import about
import streamlit.components.v1 as components


# Load environment variables from .env filemyenv\Scripts\activate

load_dotenv()

# Set the page title for the Streamlit app
st.set_page_config(page_title="Consulta CVM")



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
            app = option_menu(
                menu_title='Main Menu',
                options=['Home', 'Cadastro de Fundos',
                         'Fundos: Informação diária', 'About'],
                icons=['house', 'person-circle',
                       'clipboard-pulse', 'info-circle'],
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
            

# Your custom HTML with the script tag for monetization
custom_html = """
<!DOCTYPE html>
<html>
<head>
    <!-- Add any additional head content here -->
</head>
<body>
    <script type="text/javascript">
	atOptions = {
		'key' : '6061c3328cd4a2114ac481b4cbae2cde',
		'format' : 'iframe',
		'height' : 60,
		'width' : 468,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//www.topcreativeformat.com/6061c3328cd4a2114ac481b4cbae2cde/invoke.js"></script>
</body>
</html>
"""

# Embed the custom HTML in your Streamlit app
components.html(custom_html, height=500)        


# Instantiate MultiApp and run the application
if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.run()
