from typing import Callable
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

import widgets
from common import FilterParams

class Displayer:
    """Displays things"""
    def context_recall(self, val):
        with st.container(border=2, height=300):
            val *= 100
            st.markdown('### Полнота контекста')
            st.altair_chart(widgets.make_donut(val, 'Полнота контекста', widgets.choose_color(30, 70, val)))

    def context_precision(self, val):
        with st.container(border=2, height=300):
            val *= 100
            st.markdown('### Точность контекста')
            st.altair_chart(widgets.make_donut(val, 'Точность контекста', widgets.choose_color(30, 70, val)))
    
    def answer_correctness_neural(self, val):
        with st.container(border=2, height=300):
            val *= 100
            st.markdown('### Корректность ответа (смысловая)')
            st.altair_chart(widgets.make_donut(val, 'Смысловая корректность ответа', widgets.choose_color(25, 60, val)))

    def answer_correctness_literal(self, val):
        with st.container(border=2, height=300):
            val *= 100
            st.markdown('### Корректность ответа (лексическая)')
            st.altair_chart(widgets.make_donut(val, 'Лексическая корректность ответа', widgets.choose_color(25, 60, val)))

    def like_fraction(self, val):
        with st.container(border=2, height=300):
            st.markdown('### Удовлетворенность')
            val *= 100
            st.altair_chart(widgets.make_donut(val, 'Удовлетворенность', widgets.choose_color(30, 70, val)))

    def asked_second_time_fraction(self, val):
        with st.container(border=2, height=300):
            st.markdown('### Переспрашивают')
            val *= 100
            st.altair_chart(widgets.make_donut(val, 'Переспрашивают', widgets.choose_color(30, 70, val, reverse=True)))

    def average_time_and_delta(self, val):
        with st.container(border=2, height=300):
            time, delta = val
            st.markdown('### Время ответа')
            st.metric('Время ответа', f'{time} с', f'{delta} с', label_visibility='hidden')

    def regions_pie(self, val):
        freq_dict = val
        st.plotly_chart(widgets.make_pie(list(freq_dict.keys()), list(freq_dict.values())))

    def question_groups_hist(self, val):
        freq_dict = val
        st.plotly_chart(widgets.make_pie(list(freq_dict.keys()), list(freq_dict.values()), alternative_color_scheme=True))

    def frequent_questions(self, val: pd.DataFrame):
        st.plotly_chart(widgets.make_dataframe(val))

    def frequent_docs(self, val):
        val['Ссылка'] = '<a href="' + val['Ссылка'] + '">' + val['Ссылка'] + '</a>'
        st.plotly_chart(widgets.make_dataframe(val))

    def filters(self, available_regions, available_question_groups) -> FilterParams:
        regions = ['Все'] + available_regions
        qgroups = ['Все'] + available_question_groups
        predefined_dates = ['Последняя неделя', 'Последние 30 дней', 'Последние 3 месяца', 'Последний год', 'Произвольный период']
        region = st.selectbox('Регион: ', regions)
        qgroup = st.selectbox('Группа вопросов: ', qgroups)
        pdate = st.selectbox('Период: ', predefined_dates, index=1)
        
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

        return {
            'region': region,
            'question_group': qgroup,
            'period': (period_start, period_end),
        }
    
    def dynamic(f: Callable, filter: FilterParams = None):
        if filter == None:
            filter = FilterParams(period=(datetime.today() - timedelta(days=30), datetime.today()))
        
        df = pd.DataFrame()
        time_start = filter['period'][0]
        time_end = filter['period'][0] + timedelta(days=1)
        while time_end <= filter['period'][1]:
            

            time_start += timedelta(days=1)
            time_end += timedelta(days=1)