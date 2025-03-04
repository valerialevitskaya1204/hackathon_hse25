from functools import wraps
from typing import Callable, Optional


class Analyzer:
    """Data processing class. Loads data and gives metrics"""

    data: list

    def _filter_data(self, *, region=None, question_group=None) -> list:
        if region is not None and question_group is not None:
            return [1, 4, 8, 8]
        if region is not None:
            return [8, 800, 555, 35, 35]
        if question_group is not None:
            return [42, 42, 42]
        return self.data
    

    def load(self, f: str):
        self.data = [0, 1, 2, 3, 4, 5]

    def context_recall(self, *, region=None, question_group=None):
        data = self._filter_data(region=region, question_group=question_group)

        return 0.3 + len(data) * 0.1
    
    def context_precision(self, *, region=None, question_group=None):
        data = self._filter_data(region=region, question_group=question_group)

        return 0.43 - len(data) * 0.02
    
    def answer_correctness_literal(self, *, region=None, question_group=None):
        data = self._filter_data(region=region, question_group=question_group)

        return 0.23 + 0.01 * data[0]
    
    def answer_correctness_neural(self, *, region=None, question_group=None):
        data = self._filter_data(region=region, question_group=question_group)

        return 0.1 + data[1]%2 * 0.1
    
    def regions_frequency(self, *, region=None, question_group=None):
        data = self._filter_data(region=region, question_group=question_group)

        return {
            'Нижний Новгород': 1070 + len(data) * 2,
                     'Москва': 6025 - len(data * 2),  
        }
    
    def question_groups_frequency(self, *, region=None, question_group=None):
        data = self._filter_data(region=region, question_group=question_group)
        
        return {
            'Закон': 2027,
            'Внеучебная жизнь': 1800,
        }

    def average_time_and_delta(self, *, region=None, question_group=None):
        data = self._filter_data(region=region, question_group=question_group)

        return 1.5, -0.1
    
    def like_fraction(self, *, region=None, question_group=None):
        data = self._filter_data(region=region, question_group=question_group)

        return 0.8
    
    def asked_second_time_fraction(self, *, region=None, question_group=None):
        data = self._filter_data(region=region, question_group=question_group)

        return 0.2

    
    def available_regions(self):
        return ["Москва", "Нижний Новгород"]
    
    def available_question_groups(self):
        return ["Закон", "Внеучебная жизнь"]
    