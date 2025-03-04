import streamlit as st
from page.home import HomePage
from page.analytics import AnalyticsPage


PAGES_INCLUDED = [HomePage, AnalyticsPage]


# Sidebar navigation
st.sidebar.title("Навигация")


page = st.navigation([page().page() for page in PAGES_INCLUDED])
page.run()