import streamlit as st
import altair as alt
import plotly.express as px
import diagrams

from common import Page
from logic.analyzer import Analyzer

class HomePage(Page):
    url = "/"
    title = "Обзор"
    def render(self, *, analyzer: Analyzer, **_):
        st.markdown('# Обзор')
        st.metric(label='Context Recall', value=analyzer.context_recall(), )
        st.write
        st.altair_chart(diagrams.make_donut(analyzer.context_recall()*100, 'Recall', 'red'))