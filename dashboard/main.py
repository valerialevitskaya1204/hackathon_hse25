import streamlit as st
import altair as alt

from page.home import HomePage
from page.analytics import AnalyticsPage
from logic.analyzer import Analyzer

PAGES_INCLUDED = [HomePage, AnalyticsPage]

analyzer = Analyzer()
analyzer.load('path.json')


page = st.navigation([page().page(analyzer=analyzer) for page in PAGES_INCLUDED], expanded=True)
page.run()