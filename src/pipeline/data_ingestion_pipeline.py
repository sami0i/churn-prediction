from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion

def run_data_ingestion():
    """
    Executes the data ingestion pipeline:
    - Loads configuration
    - Instantiates ingestion component
    - Returns loaded dataset as DataFrame
    """
    config = ConfigurationManager().get_data_ingestion_config()
    ingestion = DataIngestion(config)
    df = ingestion.get_dataset()
    return df
