from typing import TypedDict, Optional
from typing_extensions import Unpack
import datetime
import pandas as pd
import numpy as np

from common import FilterParams
from .metrics import ValidatorSimple


vs = ValidatorSimple(neural = True)

class Analyzer:
    """Data processing class. Loads data and gives metrics"""
    data: list

    def preprocessing(self, data):
        data = data.rename(columns={'user_question': 'question'})
        data['ground_truth'] = np.where(data['winner'].str.upper() == 'GIGA', data['giga_answer'], data['saiga_answer'])
        data['answer'] = np.where(data['winner'].str.upper() == 'GIGA', data['saiga_answer'], data['giga_answer'])
        data['contexts'] = data['contexts'].apply(lambda x: x if len(x) > 0 else [""])
        data = data[['question', 'answer', 'ground_truth', 'contexts']]
        return data
    
    def load(self, data):
        data = pd.read_json(data)
        dataset = self.preprocessing(data)
        data = pd.concat([data, vs.validate_rag(dataset)], axis=1)
        self.data = data

    def _filter_data(self, **filters: Unpack[FilterParams]) -> list:
        region = filters.get('region')
        question_group = filters.get('question_group')
        # education = filters.get('education')
        period = filters.get('period')

        filt_data = self.data

        # if period is None, think it's the last 30 days!
        # if education is not None:
        #     data = self.data[self.data['education_level'] in education]
        if region is not None:
            filt_data = filt_data[filt_data['campus'] in region]
            
        
        if question_group is not None:
            filt_data = filt_data[filt_data['question_category'] in question_group]
        if period is not None:
            start_date, end_date = period
            filt_data = filt_data[
                (filt_data['datetime'] >= start_date) & 
                (filt_data['datetime'] <= end_date)]  
        
        return filt_data

    def context_recall(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return data['context_recall'].mean()  # Среднее значение по столбцу 'context_recall'

    def context_precision(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return data['context_precision'].mean()  # Среднее значение по столбцу 'context_precision'

    def answer_correctness_literal(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return data['answer_correctness_literal'].mean()  # Среднее значение по столбцу 'answer_correctness_literal'

    def answer_correctness_neural(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return data['answer_correctness_neural'].mean()  # Среднее значение по столбцу 'answer_correctness_neural'
    
    def regions_frequency(self, **filters: Unpack[FilterParams]):
        # Must be in decreasing-by-value order!
        data = self._filter_data(**filters)
        unique = pd.unique(data['campus'])
        return pd.Series([data[data['campus'] == i].count() for i in unique], index=unique)
    
    def question_groups_frequency(self, **filters: Unpack[FilterParams]):
        # Dict must be in decreasing-by-value order!
        data = self._filter_data(**filters)
        return data['question_category'].value_counts().to_dict()

    def most_frequent_questions(self, **filters: Unpack[FilterParams]) -> pd.DataFrame:
        # columns=['Вопрос', 'Количество схожих'] !
        data = self._filter_data(**filters)
        return data['question'].value_counts().to_dict()
    
    def most_frequent_docs(self, **filters: Unpack[FilterParams]) -> pd.DataFrame:
        # columns=['Документ', 'Ссылка', 'Количество ссылок'] !
        data = self._filter_data(**filters)
        return data['contexts'].value_counts().to_dict()
        
    def average_time_and_delta(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return 1.5, -0.1
    
    def like_fraction(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return 0.8
    
    def asked_second_time_fraction(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return 0.2