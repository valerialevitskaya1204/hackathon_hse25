from typing import TypedDict, Optional
from typing_extensions import Unpack
import datetime
import pandas as pd

from common import FilterParams
from .metrics import ValidatorSimple


vs = ValidatorSimple(neural = True)

class Analyzer:
    """Data processing class. Loads data and gives metrics"""
    data: list
    def load(self, data):
            self.data = data

    def _filter_data(self, **filters: Unpack[FilterParams]) -> list:
        region = filters.get('region')
        question_group = filters.get('question_group')
        period = filters.get('period')
        #education = filters.get('education')

        # if period is None, think it's the last 30 days!
        if region is not None:
            data = self.data[self.data['campus'] in region]
        # if education is not None:
        #     data = self.data[self.data['education_level'] in education]
        if question_group is not None:
            data = self.data[self.data['question_category'] in question_group]   
        return data

    def context_recall(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return vs.validate_rag(data, 'context_recall')
    
    def context_precision(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return vs.validate_rag(data, 'context_precision')
    
    def answer_correctness_literal(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
        return vs.validate_rag(data, 'answer_correctness_literal')
    
    def answer_correctness_neural(self, **filters: Unpack[FilterParams]):
        data = self._filter_data(**filters)
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