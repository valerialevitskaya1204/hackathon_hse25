import streamlit as st

from common import Page
from metricdisplayer import MetricDisplayer
from logic.analyzer import Analyzer

class HomePage(Page):
    url = '/'
    title = 'Обзор'
    def render(self, *, analyzer: Analyzer, **_):
        metric_displayer = MetricDisplayer()
        st.markdown('# Обзор за последние 30 дней')

        cols = st.columns((1, 0.25, 1), gap='small')
        
        with cols[0]:
            metric_cols = st.columns((1, 1), gap='small')
            with metric_cols[0]:
                metric_displayer.context_recall(analyzer.context_recall())
                metric_displayer.answer_correctness_neural(analyzer.answer_correctness_neural())

            with metric_cols[1]:
                metric_displayer.like_fraction(analyzer.like_fraction())
                metric_displayer.average_time_and_delta(analyzer.average_time_and_delta())
            

        with cols[2]:
            st.markdown('## Запросы по регионам', unsafe_allow_html=True)
            metric_displayer.regions_pie(analyzer.regions_frequency())