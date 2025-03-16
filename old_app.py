import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

from dragon.ui.style.palette import NavVar
from dragon.ui.style.css_loader import local_css, remote_css
from dragon.ui.apps.robot import Robot
from dragon.ui.apps.about import About
from dragon.ui.apps.unknown import Unknown

if __name__ == '__main__':
    st.set_page_config(
        page_title="Dragon bot",
        page_icon="resources/robot.png",
        layout="wide",
        initial_sidebar_state="auto",
    )

    local_css("resources/style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    apps = {'Dragon': Robot,
            'About': About}
    with st.sidebar:
        choose = option_menu(
            "Dragon bot", ["Dragon", "About"],
            icons=['robot', 'info-square'],
            menu_icon="joystick", default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": NavVar.background},
                "icon": {"color": NavVar.icon, "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": NavVar.page_selected},
            }
        )

    apps.get(choose, Unknown)().run()

