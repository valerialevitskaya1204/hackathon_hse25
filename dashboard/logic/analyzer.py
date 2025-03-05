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
    def load(self, data):
        self.data = pd.read_json(data)

    def _filter_data(self, **filters: Unpack[FilterParams]) -> pd.DataFrame:
        region = filters.get('region')
        question_group = filters.get('question_group')
        period = filters.get('period')

        data = self.data.copy()

        if region is not None:
            data = data[data['campus'].isin(region)]  # Используем isin()
        
        if question_group is not None:
            data = data[data['question_category'].isin(question_group)]  # Тоже заменяем на isin()

        return data
    
    def preprocessing(self, data):
        data = data.rename(columns={'user_question': 'question'})
        data['ground_truth'] = np.where(data['winner'].str.upper() == 'GIGA', data['giga_answer'], data['saiga_answer'])
        data['answer'] = np.where(data['winner'].str.upper() == 'GIGA', data['saiga_answer'], data['giga_answer'])
        data['contexts'] = data['contexts'].apply(lambda x: x if len(x) > 0 else [""])
        data = data[['question', 'answer', 'ground_truth', 'contexts']]
        return data

    def context_recall(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        data = self.preprocessing(data)
        return vs.validate_rag(data, 'context_recall')
    
    def context_precision(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        data = self.preprocessing(data)
        return vs.validate_rag(data, 'context_precision')
    
    def answer_correctness_literal(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        data = self.preprocessing(data)
        return vs.validate_rag(data, 'answer_correctness_literal')
    
    def answer_correctness_neural(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        data = self.preprocessing(data)
        return vs.validate_rag(data, 'answer_correctness_neural')
    
    def regions_frequency(self, **filters: Unpack[FilterParams]):
        # Must be in decreasing-by-value order!
        data = self._filter_data(**filters)
        return data['campus'].value_counts().to_dict()
    
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