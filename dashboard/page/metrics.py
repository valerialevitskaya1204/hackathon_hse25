import streamlit as st
from common import Page
from logic.analyzer import Analyzer

class MetricsPage(Page):
    url = "/metrics"
    title = "Метрики"
    def render(self, *, analyzer: Analyzer, **_):
        st.markdown('# Метрики')