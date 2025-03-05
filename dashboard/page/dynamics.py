import streamlit as st

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

        st.markdown(f'# {params['period'][0].strftime('%d.%m.%Y')} — {params['period'][1].strftime('%d.%m.%Y')}')
        with st.expander('Ключевые', expanded=True):
            cols = st.columns((1, 0.3, 1))
            with cols[0]:
                displayer.dynamic(analyzer.answer_correctness_literal, params, metric_name='Корректность ответа (лексическая)')
                displayer.dynamic(analyzer.answer_correctness_neural, params, metric_name='Корректность ответа (смысловая)')

            with cols[2]:
                displayer.dynamic(analyzer.context_recall, params, metric_name='Полнота контекста')
                displayer.dynamic(analyzer.context_precision, params, metric_name='Точность контекста')
        
        with st.expander('Пользовательские'):
            cols = st.columns((1, 0.3, 1))
            with cols[0]:
                displayer.dynamic(analyzer.like_fraction, params, metric_name='Удовлетворенность')
                displayer.dynamic(analyzer.asked_second_time_fraction, params, metric_name='Переспросили')
            with cols[2]:
                displayer.dynamic(analyzer.average_time, params, metric_name='Среднее время ответа')

        with st.expander('Статистика по регионам'):
            displayer.dynamic(analyzer.regions_frequency, params, metric_name='Количество запросов в регионе')

        with st.expander('Статистика по темам вопросов'):
            displayer.dynamic(analyzer.question_groups_frequency, params, metric_name='Количество запросов по теме вопроса')
