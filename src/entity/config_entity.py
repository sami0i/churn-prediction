from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration for data ingestion step.
    """
    filename: str
    local_dir: Path
    bucket_name: str


@dataclass(frozen=True)
class DataPreprocessConfig:
    """
    Configuration for data preprocessing step.
    Includes encoder/scaler paths and S3 saving options.
    """
    encoder_path: Path
    scaler_path: Path
    save_to_s3_flag: bool
    bucket_name: str


@dataclass(frozen=True)
class TrainingConfig:
    """
    Configuration for model training step.
    Contains model output path, training hyperparameters, and storage flags.
    """
    model_output_path: Path
    params: dict
    save_to_s3_flag: bool
    bucket_name: str
    test_size: float
    random_state: int
