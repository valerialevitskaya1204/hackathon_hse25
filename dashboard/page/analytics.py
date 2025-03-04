import streamlit as st
from common import Page

class AnalyticsPage(Page):
    url = "/analytics"
    title = "Аналитика"
    def render(self):
        st.markdown('# Hello')