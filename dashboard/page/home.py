import streamlit as st
import altair as alt
import plotly.express as px
import widgets

from common import Page
from logic.analyzer import Analyzer

class HomePage(Page):
    url = "/"
    title = "Обзор"
    def render(self, *, analyzer: Analyzer, **_):
        st.markdown('# Обзор')

        cols = st.columns((1, 0.25, 1), gap='small')
        
        with cols[0]:
            metric_cols = st.columns((1, 1), gap='small')
            with metric_cols[0]:
                with st.container(border=2, height=300):
                    st.markdown('### Полнота контекста')
                    val = analyzer.context_recall()*100
                    st.altair_chart(widgets.make_donut(val, 'Полнота контекста', widgets.choose_color(30, 70, val)))
                with st.container(border=2, height=300):
                    st.markdown('### Корректность ответа (смысловая)')
                    val = analyzer.answer_correctness_neural()*100
                    st.altair_chart(widgets.make_donut(val, 'Смысловая корректность ответа', widgets.choose_color(25, 60, val)))

            with metric_cols[1]:
                with st.container(border=2, height=300):
                    st.markdown('### Точность контекста')
                    val = analyzer.context_precision()*100
                    st.altair_chart(widgets.make_donut(val, 'Точность контекста', widgets.choose_color(30, 70, val)))
                with st.container(border=2, height=300):
                    time, delta = analyzer.average_time_and_delta()
                    st.markdown('### Время ответа')
                    st.metric('Время ответа', f'{time} с', f'{delta} с', label_visibility='hidden')
            

        with cols[2]:
            st.markdown('## Запросы по регионам', unsafe_allow_html=True)
            freq_dict = analyzer.regions_frequency()
            st.plotly_chart(widgets.make_pie(list(freq_dict.keys()), list(freq_dict.values())))