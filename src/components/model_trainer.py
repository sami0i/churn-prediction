import joblib
from xgboost import XGBClassifier
from src.utils.common import save_to_s3

class ModelTrainer:
    """
    Trains an XGBoost classification model and optionally uploads it to S3.
    """

    def __init__(self, config):
        """
        Initializes the model trainer with training parameters from config.

        Parameters:
        - config: Object containing `params`, `model_output_path`, and `save_to_s3_flag`
        """
        self.config = config
        self.model = XGBClassifier(**self.config.params)

    def train(self, X_train, y_train):
        """
        Trains the XGBoost model using the provided training features and labels.

        Parameters:
        - X_train: Training feature matrix
        - y_train: Training label vector
        """
        self.model.fit(X_train, y_train)

    def save_model(self):
        """
        Saves the trained model to a local path.
        If `save_to_s3_flag` is set, also uploads the model to S3.
        """
        self.config.model_output_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.config.model_output_path)

        print(f"✅ Model saved to {self.config.model_output_path}")

        if self.config.save_to_s3_flag:
            save_to_s3(self.model, self.config.model_output_path)
