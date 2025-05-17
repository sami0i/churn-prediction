import sys
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
import xgboost as xgb

from src.config.configuration import ConfigurationManager
from src.components.data_preprocessor import DataPreprocessor
from src.utils.common import load_from_s3


def load_model_from_s3(path: Path):
    """
    Loads a trained model from S3 using a shared utility.

    Parameters:
    - path: Path object representing the model location in S3

    Returns:
    - Loaded model object
    """
    return load_from_s3(path)


def run_prediction(input_csv_path: str):
    """
    Runs the full prediction pipeline:
    - Loads raw input CSV
    - Loads preprocessing artifacts
    - Transforms input features
    - Loads the trained model
    - Generates predictions
    - Saves predictions to a .npy file

    Parameters:
    - input_csv_path: Path to input CSV file
    """
    # Step 1: Load new input data
    df = pd.read_csv(input_csv_path)

    # Step 2: Load and initialize preprocessor
    config = ConfigurationManager().get_data_preprocess_config()
    preprocessor = DataPreprocessor(config)
    preprocessor.load()

    # Step 3: Transform input data (features only)
    X = preprocessor.transform(df)

    # Step 4: Load trained model (prefer local, fallback to S3)
    model_path = ConfigurationManager().get_training_config().model_output_path
    if model_path.exists():
        model = joblib.load(model_path)
        print(f"✅ Loaded model from local: {model_path}")
    else:
        model_config = ConfigurationManager().get_training_config()
        model = load_model_from_s3(model_config.model_output_path)
        print(f"☁️  Loaded model from S3")

    # Step 5: Ensure model is a valid XGBClassifier instance
    if not isinstance(model, xgb.XGBClassifier):
        model = joblib.load(model)  # Fallback in case raw bytes are returned

    # Step 6: Predict probabilities
    predictions = model.predict_proba(X, iteration_range=(0, 10))

    # Step 7: Save predictions
    output_dir = Path("results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "results.npy"

    with open(output_path, "wb") as f:
        np.save(f, predictions)

    print(f"✅ Predictions saved to: {output_path.resolve()}")


if __name__ == "__main__":
    # Entry point for CLI execution
    if len(sys.argv) != 2:
        print("Usage: python -m src.pipeline.predict <input_csv_path>")
    else:
        run_prediction(sys.argv[1])
