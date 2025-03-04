import streamlit as st
from common import Page
from logic.analyzer import Analyzer

class AnalyticsPage(Page):
    url = "/analytics"
    title = "Аналитика"
    def render(self, *, analyzer: Analyzer, **_):
        st.markdown('# Аналитика')