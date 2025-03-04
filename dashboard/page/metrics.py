import streamlit as st

from common import Page
from logic.analyzer import Analyzer
from metricdisplayer import MetricDisplayer


class MetricsPage(Page):
    url = '/metrics'
    title = 'Метрики'
    def render(self, *, analyzer: Analyzer, **_):
        metric_displayer = MetricDisplayer()
        with st.sidebar:
            st.markdown('### Фильтры')
            regions = ["Все"] + analyzer.available_regions()
            qgroups = ["Все"] + analyzer.available_question_groups()
            region = st.selectbox("Регион: ", regions)
            qgroup = st.selectbox("Группа вопросов: ", qgroups)
            
            if(region == "Все"):
                region = None

            if(qgroup == "Все"):
                qgroup = None

            st.markdown(f'{region} {qgroup}')

        params = {
            'region': region,
            'question_group': qgroup,
        }
        st.markdown('# Метрики')
        with st.expander('Ключевые', expanded=True):
            cols = st.columns((1, 1, 1, 1))
            with cols[0]:
                metric_displayer.answer_correctness_neural(analyzer.answer_correctness_neural(**params))
            with cols[1]:
                metric_displayer.answer_correctness_literal(analyzer.answer_correctness_literal(**params))
            with cols[2]:
                metric_displayer.context_precision(analyzer.context_precision(**params))
            with cols[3]:
                metric_displayer.context_recall(analyzer.context_recall(**params))
        
        with st.expander('Пользовательские'):
            cols = st.columns((1, 1, 1, 1))
            with cols[0]:
                metric_displayer.like_fraction(analyzer.like_fraction(**params))
            with cols[1]:
                metric_displayer.asked_second_time_fraction(analyzer.asked_second_time_fraction(**params))
            with cols[2]:
                metric_displayer.average_time_and_delta(analyzer.average_time_and_delta(**params))

        with st.expander('Статистика по региону/теме'):
            cols = st.columns((1, 1))
            with cols[0]:
                metric_displayer.regions_pie(analyzer.regions_frequency(**params))
            with cols[1]:
                metric_displayer.question_groups_pie(analyzer.question_groups_frequency(**params))