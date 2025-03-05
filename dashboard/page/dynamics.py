import streamlit as st
from datetime import datetime, timedelta

from common import Page
from logic.analyzer import Analyzer
from displayer import Displayer


class DynamicsPage(Page):
    url = '/dynamics'
    title = 'Динамика'
    def render(self, *, analyzer: Analyzer, **_):
        displayer = Displayer()
        with st.sidebar:
            st.markdown('### Фильтры')
            params = displayer.filters(available_regions=analyzer.available_regions(), available_question_groups=analyzer.available_question_groups())

        st.markdown(f"# {params['period'][0].strftime('%d.%m.%Y')} — {params['period'][1].strftime('%d.%m.%Y')}")
        with st.expander('Ключевые', expanded=True):
            ...
        
        with st.expander('Пользовательские'):
            cols = st.columns((1, 1, 1, 1))
            with cols[0]:
                displayer.like_fraction(analyzer.like_fraction(**params))
            with cols[1]:
                displayer.asked_second_time_fraction(analyzer.asked_second_time_fraction(**params))
            with cols[2]:
                displayer.average_time_and_delta(analyzer.average_time_and_delta(**params))

        with st.expander('Статистика по региону'):
            displayer.regions_pie(analyzer.regions_frequency(**params))

        with st.expander('Статистика по теме вопроса'):
            displayer.question_groups_hist(analyzer.question_groups_frequency(**params))
