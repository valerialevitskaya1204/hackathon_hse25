import streamlit as st
from datetime import datetime, timedelta

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
            predefined_dates = ['Последняя неделя', 'Последние 30 дней', 'Последние 3 месяца', 'Последний год', 'Произвольный период']
            region = st.selectbox("Регион: ", regions)
            qgroup = st.selectbox("Группа вопросов: ", qgroups)
            pdate = st.selectbox("Период: ", predefined_dates, index=1)
            
            if region == 'Все':
                region = None

            if qgroup == 'Все':
                qgroup = None
            
            period_end = datetime.today()
            if pdate == 'Последняя неделя':
                period_start = period_end - timedelta(days=7)
            elif pdate == 'Последние 30 дней':
                period_start = period_end - timedelta(days=30)
            elif pdate == 'Последние 3 месяца':
                period_start = period_end - timedelta(days=92)
            elif pdate == 'Последний год':
                period_start = period_end - timedelta(days=365)
            elif pdate == 'Произвольный период':
                period_start = st.date_input('Начало: ', format='DD.MM.YYYY')
                period_end = st.date_input('Конец', min_value=period_start, format='DD.MM.YYYY')

            st.markdown(f'{region} {qgroup}')

        params = {
            'region': region,
            'question_group': qgroup,
            'period': (period_start, period_end),
            '1': 'zhopa'
        }
        st.markdown(f'# Метрики с {period_start.strftime('%d.%m.%Y')} по {period_end.strftime('%d.%m.%Y')}')
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

        with st.expander('Статистика по региону'):
            metric_displayer.regions_pie(analyzer.regions_frequency(**params))

        with st.expander('Статистика по теме вопроса'):
            metric_displayer.question_groups_hist(analyzer.question_groups_frequency(**params))

        with st.expander('Типы наиболее частых вопросов'):
            metric_displayer.frequent_questions(analyzer.most_frequent_questions(**params))