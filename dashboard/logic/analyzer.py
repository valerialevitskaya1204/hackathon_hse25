class Analyzer:
    def load(self, f: str):
        self.data = [0, 1, 2, 3, 4, 5]
    
    def context_recall(self):
        return 0.7
    
    def context_precision(self):
        return 0.43
    
    def answer_correctness_literal(self):
        return 0.23
    
    def answer_correctness_neural(self):
        return 0.1
    
    def regions_frequency(self):
        return {'Нижний Новгород': 1070,
                         'Москва': 6025,  
        }

    def average_time_and_delta(self):
        return 1.5, -0.1
    