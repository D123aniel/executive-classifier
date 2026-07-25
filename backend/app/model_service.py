from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Lock

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


LABELS = ("Direct", "Partially Evasive", "Fully Evasive")
MAX_TOKENS = 512


@dataclass(frozen=True)
class Prediction:
    label: str
    scores: dict[str, float]
    margin: float
    review_recommended: bool
    truncated: bool
    token_count: int


class ModelService:
    def __init__(
        self,
        model_path: Path,
        top_score_review_threshold: float,
        margin_review_threshold: float,
    ) -> None:
        self.model_path = model_path
        self.top_score_review_threshold = top_score_review_threshold
        self.margin_review_threshold = margin_review_threshold
        self._tokenizer = None
        self._model = None
        self._device = torch.device("cpu")
        self._load_lock = Lock()

    @property
    def is_loaded(self) -> bool:
        return self._model is not None and self._tokenizer is not None

    def load(self) -> None:
        if self.is_loaded:
            return

        with self._load_lock:
            if self.is_loaded:
                return

            if not self.model_path.is_dir():
                raise FileNotFoundError(
                    f"Model directory does not exist: {self.model_path}"
                )

            self._device = self._select_device()
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                local_files_only=True,
            )
            self._model = AutoModelForSequenceClassification.from_pretrained(
                self.model_path,
                local_files_only=True,
            )
            self._model.to(self._device)
            self._model.eval()

    def predict(self, question: str, response: str) -> Prediction:
        self.load()
        assert self._tokenizer is not None
        assert self._model is not None

        full_encoding = self._tokenizer(
            question.strip(),
            response.strip(),
            add_special_tokens=True,
            truncation=False,
            verbose=False,
        )
        token_count = len(full_encoding["input_ids"])

        model_inputs = self._tokenizer(
            question.strip(),
            response.strip(),
            max_length=MAX_TOKENS,
            truncation=True,
            return_tensors="pt",
        ).to(self._device)

        with torch.inference_mode():
            logits = self._model(**model_inputs).logits[0]
            probabilities = torch.softmax(logits, dim=-1).detach().cpu().tolist()

        scores = {
            label: round(float(probability), 6)
            for label, probability in zip(LABELS, probabilities, strict=True)
        }
        ranked_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        label, top_score = ranked_scores[0]
        margin = round(top_score - ranked_scores[1][1], 6)

        return Prediction(
            label=label,
            scores=scores,
            margin=margin,
            review_recommended=(
                top_score < self.top_score_review_threshold
                or margin < self.margin_review_threshold
            ),
            truncated=token_count > MAX_TOKENS,
            token_count=token_count,
        )

    @staticmethod
    def _select_device() -> torch.device:
        if torch.cuda.is_available():
            return torch.device("cuda")
        if torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")
