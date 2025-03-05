import streamlit as st
import altair as alt

import styles

from page.home import HomePage
from page.metrics import MetricsPage
from logic.analyzer import Analyzer
from page.dynamics import DynamicsPage


PAGES_INCLUDED = [HomePage, MetricsPage, DynamicsPage]

analyzer = Analyzer()
analyzer.load('parsed_dash.json')

st.set_page_config(page_icon='🚀', layout='wide', initial_sidebar_state='expanded')
alt.theme.enable('dark')
styles.init_styles()
with st.sidebar:
    st.title('Дашборд бота ВШЭ')
page = st.navigation([page().page(analyzer=analyzer) for page in PAGES_INCLUDED], expanded=True)
page.run()