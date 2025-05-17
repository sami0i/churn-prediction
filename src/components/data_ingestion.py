import pandas as pd

class DataIngestion:
    """
    Handles loading the dataset from either a local path or an S3 bucket.
    Falls back to S3 only if the local file does not exist.
    """

    def __init__(self, config):
        """
        Initializes the ingestion component with the provided configuration.

        Parameters:
        - config: An object containing `local_dir`, `filename`, and `bucket_name`.
        """
        self.config = config

    def get_dataset(self):
        """
        Loads the dataset as a pandas DataFrame.
        - Uses the local file if it exists.
        - Otherwise attempts to load from S3 using the bucket and filename.

        Returns:
        - pd.DataFrame: Loaded dataset

        Raises:
        - ValueError: If no local file is found and bucket is not configured
        """
        local_path = self.config.local_dir / self.config.filename

        # Check for local dataset first
        if local_path.exists():
            print(f"📁 Using local dataset: {local_path}")
            return pd.read_csv(local_path)

        # Fallback to S3 if local file is missing
        if not self.config.bucket_name:
            raise ValueError("❌ BUCKET_NAME not set in env and local file not found.")

        s3_path = f"s3://{self.config.bucket_name}/data/{self.config.filename}"
        print(f"📥 Using S3 dataset: {s3_path}")
        return pd.read_csv(s3_path)
