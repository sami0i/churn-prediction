from src.config.configuration import ConfigurationManager
from src.components.data_preprocessor import DataPreprocessor

def run_data_preprocessing_pipeline(df):
    """
    Executes the data preprocessing pipeline:
    - Loads preprocessing configuration
    - Fits encoder and scaler to the provided DataFrame
    - Saves preprocessing artifacts locally and optionally to S3
    - Returns the transformed features and labels

    Parameters:
    - df: Raw input DataFrame to preprocess

    Returns:
    - X: Feature matrix (NumPy array)
    - y: Target labels (NumPy array or None)
    """
    config = ConfigurationManager().get_data_preprocess_config()
    preprocessor = DataPreprocessor(config)
    preprocessor.fit(df)
    preprocessor.save()

    return preprocessor.X, preprocessor.y
