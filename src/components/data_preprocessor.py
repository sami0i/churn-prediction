import joblib
import pandas as pd
import os
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, LabelEncoder
from src.utils.common import save_to_s3, load_from_s3

class DataPreprocessor:
    """
    Handles preprocessing of tabular data, including:
    - Dropping non-predictive columns (e.g., cust_id)
    - Encoding categorical variables using OneHotEncoder
    - Scaling numerical variables using MinMaxScaler
    - Saving and loading preprocessing artifacts locally or from S3
    """

    def __init__(self, config):
        """
        Initialize DataPreprocessor with configuration paths and flags.

        Parameters:
        - config: Config object with encoder_path, scaler_path, bucket_name, etc.
        """
        self.encoder_path = config.encoder_path
        self.scaler_path = config.scaler_path
        self.save_to_s3_flag = config.save_to_s3_flag
        self.bucket = config.bucket_name

        self.encoder = None
        self.scaler = None
        self.X = None
        self.y = None

    def fit(self, df: pd.DataFrame):
        """
        Fits the encoder and scaler to the training data.

        - Drops 'cust_id' and encodes 'churn' labels (if present).
        - Identifies categorical and numerical columns.
        - Stores the transformed features in self.X and labels in self.y.
        """
        df = df.copy()

        # Drop identifier column
        if "cust_id" in df.columns:
            df.drop(columns=["cust_id"], inplace=True)

        # Label-encode churn column if present
        if "churn" in df.columns:
            label_encoder = LabelEncoder()
            self.y = label_encoder.fit_transform(df.pop("churn"))
        else:
            self.y = None

        # Split into categorical and numerical features
        cat_cols = df.select_dtypes(include="object").columns.tolist()
        num_cols = df.select_dtypes(exclude="object").columns.tolist()

        # Initialize transformers
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        self.scaler = MinMaxScaler()

        # Fit and transform features
        X_cat = self.encoder.fit_transform(df[cat_cols]) if cat_cols else []
        X_num = self.scaler.fit_transform(df[num_cols]) if num_cols else []

        from numpy import hstack
        self.X = hstack([X_num, X_cat]) if cat_cols else X_num

    def transform(self, df: pd.DataFrame):
        """
        Transforms new data using the previously fitted encoder and scaler.

        Parameters:
        - df: Input DataFrame

        Returns:
        - Transformed NumPy array ready for model inference
        """
        df = df.copy()

        if "cust_id" in df.columns:
            df.drop(columns=["cust_id"], inplace=True)

        if "churn" in df.columns:
            df.drop(columns=["churn"], inplace=True)

        cat_cols = df.select_dtypes(include="object").columns.tolist()
        num_cols = df.select_dtypes(exclude="object").columns.tolist()

        X_cat = self.encoder.transform(df[cat_cols]) if cat_cols else []
        X_num = self.scaler.transform(df[num_cols]) if num_cols else []

        from numpy import hstack
        return hstack([X_num, X_cat]) if cat_cols else X_num

    def save(self):
        """
        Saves the fitted encoder and scaler to disk.
        Also uploads to S3 if `save_to_s3_flag` is enabled.
        """
        self.encoder_path.parent.mkdir(parents=True, exist_ok=True)
        self.scaler_path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.encoder, self.encoder_path)
        joblib.dump(self.scaler, self.scaler_path)

        print(f"✅ Saved encoder to {self.encoder_path}")
        print(f"✅ Saved scaler to {self.scaler_path}")

        if self.save_to_s3_flag:
            save_to_s3(self.encoder, self.encoder_path)
            save_to_s3(self.scaler, self.scaler_path)

    def load(self):
        """
        Loads the encoder and scaler from local paths or S3 if not found locally.
        """
        if self.encoder_path.exists():
            self.encoder = joblib.load(self.encoder_path)
            print(f"✅ Loaded encoder from local: {self.encoder_path}")
        elif self.save_to_s3_flag:
            self.encoder = load_from_s3(self.encoder_path)
            print(f"☁️  Loaded encoder from S3")

        if self.scaler_path.exists():
            self.scaler = joblib.load(self.scaler_path)
            print(f"✅ Loaded scaler from local: {self.scaler_path}")
        elif self.save_to_s3_flag:
            self.scaler = load_from_s3(self.scaler_path)
            print(f"☁️  Loaded scaler from S3")
