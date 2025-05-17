from sklearn.model_selection import train_test_split

from src.config.configuration import ConfigurationManager
from src.components.model_trainer import ModelTrainer

def run_training_pipeline(X, y):
    """
    Runs the model training pipeline:
    - Loads training configuration
    - Splits data into training and test sets
    - Trains the model
    - Saves the trained model locally (and optionally to S3)

    Parameters:
    - X: Feature matrix (NumPy array)
    - y: Labels (NumPy array)
    """
    config_mgr = ConfigurationManager()
    train_cfg = config_mgr.get_training_config()

    # Step 1: Split data for training (80%) and validation (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=train_cfg.test_size, random_state=train_cfg.random_state
    )

    # Step 2: Initialize and train model
    trainer = ModelTrainer(train_cfg)
    trainer.train(X_train, y_train)

    # Step 3: Save trained model
    trainer.save_model()
