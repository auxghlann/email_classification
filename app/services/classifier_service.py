from collections import Counter
from pathlib import Path
import re
from typing import List, Optional
import joblib
import pandas as pd

from app.schemas.email_schema import EmailClassificationResponse


class ClassifierService:
    def __init__(self, model_path: Path, features_path: Path) -> None:
        self.model_path = model_path
        self.features_path = features_path
        self.model = None
        self.feature_names: List[str] = []
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        if not self.features_path.exists():
            raise FileNotFoundError(f"Feature names file not found at {self.features_path}")

        self.model = joblib.load(self.model_path)
        self.feature_names = joblib.load(self.features_path)

    def extract_features(self, text: str) -> pd.DataFrame:
        words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
        word_counts = Counter(words)

        features_dict = {word: [word_counts.get(word, 0)] for word in self.feature_names}
        return pd.DataFrame(features_dict)

    def classify(self, text: str) -> EmailClassificationResponse:
        features_df = self.extract_features(text)
        prediction_int = int(self.model.predict(features_df)[0])

        probabilities = self.model.predict_proba(features_df)[0]
        confidence = float(probabilities[prediction_int])

        is_spam = prediction_int == 1

        return EmailClassificationResponse(
            is_spam=is_spam,
            confidence=round(confidence, 4),
        )


# Global singleton instance
_classifier_service: Optional[ClassifierService] = None


def get_classifier_service() -> ClassifierService:
    global _classifier_service
    if _classifier_service is None:
        base_dir = Path(__file__).resolve().parent.parent.parent
        model_path = base_dir / "pkl_files" / "spam_model.pkl"
        features_path = base_dir / "pkl_files" / "feature_names.pkl"
        _classifier_service = ClassifierService(model_path, features_path)
    return _classifier_service
