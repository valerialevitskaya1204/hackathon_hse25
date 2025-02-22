from typing import List, Dict
import evaluate
import numpy as np
import pandas as pd
from tqdm import tqdm
from ragas import evaluate as ragas_evaluate
from ragas.metrics import answer_correctness, answer_relevancy, context_precision as ragas_context_precision, context_recall as ragas_context_recall

class Validator:
    """
    A class for evaluating quality metrics for datasets, including context recall,
    context precision, and answer correctness using both literal and neural approaches.
    Supports Ragas-based evaluation as well.
    """

    def __init__(self, neural: bool = False):
        """
        Initialize the Validator class.

        :param neural: Whether to use neural-based evaluation (BERTScore). Default is False.
        """
        self.neural = neural
        self.rouge = evaluate.load("rouge")
        self.bleu = evaluate.load("bleu")
        self.chrf = evaluate.load("chrf")
        self.bertscore = evaluate.load("bertscore") if neural else None

    def context_recall(self, ground_truth: str, contexts: List[str]) -> float:
        """Calculate ROUGE-2 recall between contexts and ground truth."""
        try:
            scores = [
                self.rouge.compute(predictions=[str(c)], references=[ground_truth])["rouge2"]
                for c in contexts
            ]
            return np.mean(scores) if scores else 0.0
        except Exception as e:
            print(f"Ошибка в подсчете context_recall: {e}")
            return 0.0

    def context_precision(self, ground_truth: str, contexts: List[str]) -> float:
        """Calculate BLEU precision between contexts and ground truth."""
        scores = []
        for c in contexts:
            try:
                result = self.bleu.compute(
                    predictions=[str(c)], references=[ground_truth], max_order=2
                )
                scores.append(result["precisions"][1])
            except (ZeroDivisionError, IndexError):
                scores.append(0.0)
            except Exception as e:
                print(f"Ошибка в подсчете context_precision: {e}")
        return np.mean(scores) if scores else 0.0

    def answer_correctness_literal(self, ground_truth: str, answer: str, char_order: int = 6, word_order: int = 2, beta: float = 1) -> float:
        """Calculate chrF score between answer and ground truth."""
        try:
            score = self.chrf.compute(
                predictions=[answer],
                references=[ground_truth],
                char_order=char_order,
                word_order=word_order,
                beta=beta,
            )["score"]
            return score
        except Exception as e:
            print(f"Ошибка в подсчете answer_correctness_literal: {e}")
            return 0.0

    def answer_correctness_neural(self, ground_truth: str, answer: str, model_type: str = "cointegrated/rut5-base") -> float:
        """Calculate BERTScore F1 between answer and ground truth."""
        if not self.neural or not self.bertscore:
            return 0.0

        try:
            score = self.bertscore.compute(
                predictions=[answer],
                references=[ground_truth],
                model_type=model_type,
                batch_size=1,
                num_layers=11,
            )["f1"][0]
            return score
        except Exception as e:
            print(f"Ошибка в подсчете answer_correctness_neural: {e}")
            return 0.0

    def score_sample(self, answer: str, ground_truth: str, context: List[str]) -> Dict[str, float]:
        """Calculate all metrics for a given sample."""
        return {
            "context_recall": self.context_recall(ground_truth, context),
            "context_precision": self.context_precision(ground_truth, context),
            "answer_correctness_literal": self.answer_correctness_literal(ground_truth, answer),
            "answer_correctness_neural": self.answer_correctness_neural(ground_truth, answer) if self.neural else 0.0,
        }

    def validate_dataset(self, dataset: pd.DataFrame, use_ragas: bool = False) -> Dict[str, float]:
        """
        Validate the dataset and return average scores for all metrics.

        :param dataset: DataFrame with columns: 'answer', 'ground_truth', 'contexts'
        :param use_ragas: Whether to use Ragas metrics for evaluation.
        :return: Dictionary of average metric scores.
        """
        if use_ragas:
            try:
                score = ragas_evaluate(
                    dataset,
                    metrics=[
                        answer_correctness,
                        answer_relevancy,
                        ragas_context_recall,
                        ragas_context_precision,
                    ]
                )
                return score
            except Exception as e:
                print(f"Ошибка в подсчете оценок с помощью Ragas: {e}")
                return {}

        results = {"context_recall": [], "context_precision": [], "answer_correctness_literal": [], "answer_correctness_neural": []}

        for _, row in tqdm(dataset.iterrows(), total=len(dataset), desc="Evaluating"):
            try:
                scores = self.score_sample(row["answer"], row["ground_truth"], row["contexts"])
                for key, value in scores.items():
                    results[key].append(value)
            except KeyError as e:
                print(f"В тестовом датасете нет нужной строки: {e}")
            except Exception as e:
                print(f"В тестовом датасете нет что-то со строкой: {e}")

        return {key: np.mean(values) if values else 0.0 for key, values in results.items()}