
import streamlit as st
import abc

class App(abc.ABC):

    def run(self):
        st.text('unknown page')