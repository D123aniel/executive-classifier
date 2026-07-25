import argparse
import csv
from pathlib import Path

from app.model_service import ModelService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare local model predictions with saved holdout outputs."
    )
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--score-tolerance", type=float, default=1e-4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    service = ModelService(
        model_path=args.model_path,
        top_score_review_threshold=0.60,
        margin_review_threshold=0.15,
    )

    with args.predictions.open(newline="", encoding="utf-8") as predictions_file:
        rows = list(csv.DictReader(predictions_file))[: args.samples]

    if not rows:
        raise ValueError("The saved predictions file contains no rows.")

    for index, row in enumerate(rows, start=1):
        prediction = service.predict(row["question"], row["answer"])
        expected_label = row["Predicted_Class"]
        if prediction.label != expected_label:
            raise AssertionError(
                f"Sample {index}: expected {expected_label}, got {prediction.label}"
            )

        expected_scores = {
            "Direct": float(row["Direct_prob"]),
            "Partially Evasive": float(row["Partially Evasive_prob"]),
            "Fully Evasive": float(row["Fully Evasive_prob"]),
        }
        for label, expected_score in expected_scores.items():
            actual_score = prediction.scores[label]
            if abs(actual_score - expected_score) > args.score_tolerance:
                raise AssertionError(
                    f"Sample {index}, {label}: expected {expected_score:.6f}, "
                    f"got {actual_score:.6f}"
                )

        print(f"Sample {index}: {prediction.label} verified")

    print(f"Verified {len(rows)} saved predictions.")


if __name__ == "__main__":
    main()
