class Analyzer:
    def load(self, f: str):
        self.data = [0, 1, 2, 3, 4, 5]
    
    def context_recall(self):
        return 0.57
    
    def context_precision(self):
        return 0.43
    
    def answer_correctness_literal(self):
        return 0.23
    
    def answer_correctness_neural(self):
        return 0.1