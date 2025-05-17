import os
import yaml
from pathlib import Path
from src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from src.entity.config_entity import DataIngestionConfig, DataPreprocessConfig, TrainingConfig

class ConfigurationManager:
    """
    Loads and provides structured access to configuration settings for:
    - Data ingestion
    - Data preprocessing
    - Model training

    Reads from YAML config files and injects environment-based runtime values.
    """

    def __init__(self, config_path=CONFIG_FILE_PATH, params_path=PARAMS_FILE_PATH):
        """
        Initializes the configuration manager by loading config and param files.

        Parameters:
        - config_path: Path to the main config YAML
        - params_path: Path to the model parameters YAML
        """
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        with open(params_path, "r") as f:
            self.param = yaml.safe_load(f)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Creates a configuration object for the data ingestion pipeline.

        Returns:
        - DataIngestionConfig with filename, local directory, and bucket name
        """
        data_cfg = self.config["data_ingestion"]
        return DataIngestionConfig(
            filename=data_cfg["filename"],
            local_dir=Path(data_cfg["local_dir"]),
            bucket_name=os.getenv("BUCKET_NAME", "")  # Allows env override
        )

    def get_data_preprocess_config(self) -> DataPreprocessConfig:
        """
        Creates a configuration object for the data preprocessing pipeline.

        Returns:
        - DataPreprocessConfig with encoder/scaler paths and S3 options
        """
        preprocess_cfg = self.config["data_preprocessing"]
        return DataPreprocessConfig(
            encoder_path=Path(preprocess_cfg["encoder_path"]),
            scaler_path=Path(preprocess_cfg["scaler_path"]),
            save_to_s3_flag=preprocess_cfg.get("save_to_s3", True),
            bucket_name=os.getenv("BUCKET_NAME", "")
        )

    def get_training_config(self) -> TrainingConfig:
        """
        Creates a configuration object for model training.

        Returns:
        - TrainingConfig with model path, parameters, and S3 save flag
        """
        params = self.param["model"]
        model_path = self.config["model"]["model_path"]

        split_cfg = self.param.get("split", {})
        test_size = split_cfg.get("test_size", 0.2)
        random_state = split_cfg.get("random_state", 42)

        return TrainingConfig(
            model_output_path=Path(model_path),
            params={k: v for k, v in params.items() if k != "model_path"},
            save_to_s3_flag=True,
            bucket_name=os.getenv("BUCKET_NAME", ""),
            test_size=test_size,
            random_state=random_state
        )
