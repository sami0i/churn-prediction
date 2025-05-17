import argparse
from pathlib import Path

from src.pipeline.data_ingestion_pipeline import run_data_ingestion
from src.pipeline.data_preprocess_pipeline import run_data_preprocessing_pipeline
from src.pipeline.train_pipeline import run_training_pipeline
from src.pipeline.predict import run_prediction


def run_training_workflow():
    """
    Executes the full training pipeline:
    1. Ingests dataset
    2. Preprocesses data
    3. Trains and saves model
    """
    print("\n🚀 Starting ML Workflow Pipeline...\n")

    print("📥 Step 1: Running Data Ingestion...")
    df = run_data_ingestion()

    print("\n🧹 Step 2: Running Data Preprocessing...")
    X, y = run_data_preprocessing_pipeline(df)

    print("\n🧠 Step 3: Running Model Training...")
    run_training_pipeline(X, y)

    print("\n✅ Training completed.\n")


def main():
    """
    Entry point for running either the training or prediction pipeline.
    Uses CLI arguments to determine mode and input path.
    """
    parser = argparse.ArgumentParser(description="Churn Prediction ML Pipeline")
    parser.add_argument(
        "--mode",
        choices=["train", "predict"],
        required=True,
        help="Pipeline mode to run: 'train' or 'predict'"
    )
    parser.add_argument(
        "--input",
        type=str,
        help="Path to input CSV file (required for --mode=predict)"
    )

    args = parser.parse_args()

    if args.mode == "train":
        run_training_workflow()

    elif args.mode == "predict":
        if not args.input:
            raise ValueError("❌ You must provide --input when using --mode=predict")
        run_prediction(Path(args.input).resolve())


if __name__ == "__main__":
    main()
