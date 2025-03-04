import streamlit as st
import widgets

class MetricDisplayer:
    """Displays metrics according to the data"""
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

    def question_groups_pie(self, val):
        freq_dict = val
        st.plotly_chart(widgets.make_pie(list(freq_dict.keys()), list(freq_dict.values()), alternativeColorScheme=True))