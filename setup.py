from setuptools import setup, find_packages

setup(
    name="churn_prediction",
    version="0.1.0",
    description="Scalable machine learning pipeline for customer churn prediction",
    author="Samane Ahangar",
    author_email="me@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas==1.5.3",
        "numpy==1.24.4",
        "scikit-learn==1.2.2",
        "xgboost==1.7.6",
        "joblib==1.2.0",
        "boto3==1.28.0",
        "s3fs>=2023.6.0",
        "python-dotenv==1.0.0",
        "pyyaml", 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.10",
)
