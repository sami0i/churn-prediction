import pandas as pd
import numpy as np
import pytest
from src.components.data_preprocessor import DataPreprocessor
from src.entity.config_entity import DataPreprocessConfig
from pathlib import Path

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "cust_id": [1, 2],
        "count_total": [10, 20],
        "country": ["A", "B"],
        "churn": ["Yes", "No"]
    })

@pytest.fixture
def preprocessor_config(tmp_path: Path):
    return DataPreprocessConfig(
        encoder_path=tmp_path / "encoder.joblib",
        scaler_path=tmp_path / "scaler.joblib",
        save_to_s3_flag=False,
        bucket_name=""
    )

def test_fit_and_transform(sample_dataframe: pd.DataFrame, preprocessor_config: DataPreprocessConfig):
    dp = DataPreprocessor(preprocessor_config)
    
    dp.fit(sample_dataframe)
    
    # Check shapes
    assert dp.X.shape[0] == 2  # 2 samples
    assert dp.y.tolist() == [1, 0]  # Label-encoded churn
    
    # Check transform shape matches fit shape
    transformed = dp.transform(sample_dataframe)
    assert transformed.shape == dp.X.shape

def test_save_and_load_artifacts(sample_dataframe: pd.DataFrame, preprocessor_config: DataPreprocessConfig):
    dp = DataPreprocessor(preprocessor_config)
    dp.fit(sample_dataframe)
    dp.save()

    assert preprocessor_config.encoder_path.exists()
    assert preprocessor_config.scaler_path.exists()

    dp2 = DataPreprocessor(preprocessor_config)
    dp2.load()

    transformed = dp2.transform(sample_dataframe)
    assert transformed.shape == dp.X.shape
