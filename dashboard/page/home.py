import streamlit as st
from common import Page

class HomePage(Page):
    url = "/"
    title = "Главная"
    def render(self):
        st.markdown('# World')