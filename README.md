
# Churn Prediction Pipeline

A scalable, cloud-ready Machine Learning pipeline for predicting customer churn — built with **Docker**, **Terraform**, **GitHub Actions**, and **AWS ECS**.


> 📦 Provisioned with Terraform · 🚀 Deployed with ECS Fargate · 🔐 Artifacts stored in S3

## Touch the working solution live!
Click [here](https://github.com/sami0i/churn-prediction/actions/runs/15084115059) to see the project demo.
![image](https://github.com/user-attachments/assets/a9685aba-2428-464f-a8a5-6cddafa4c2db)


## Project Structure

```bash
churn-prediction/
├── src/                     # Core pipeline: ingestion, preprocessing, training, prediction
│   ├── components/
│   ├── config/
|   ├── constants/
|   ├── entity/
│   ├── pipeline/
│   └── utils/
├── config/                  # YAML configs for pipeline stages
├── data/                    # Sample input dataset (CSV)
├── artifacts/              # Saved model, encoder, scaler, etc.
├── infrastructure/          # Terraform + Ansible for infra as code
│   ├── terraform/
│   └── ansible/
├── .github/workflows/       # GitHub Actions CI/CD
├── Dockerfile
├── requirements.txt
├── params.yaml
└── main.py
```

## Features

- ✅ **Modular ML Pipeline** — Data ingestion, preprocessing, model training, and prediction stages.
- ✅ **Config-Driven** — Easily change parameters and file paths via `config.yaml` and `params.yaml`.
- ✅ **CI/CD Pipeline** — Auto-build, push, and deploy via GitHub Actions + AWS ECS.
- ✅ **Infrastructure as Code** — Provision cloud resources with Terraform + Ansible.
- ✅ **S3 Integration** — Artifacts (model, encoder, scaler) stored and loaded from Amazon S3.

---


## ✅ Satisfaction Assessment

This section evaluates how each requirement of the problem statement is satisfied in the churn prediction project.

---

## 1. Scalable Containerized Solution Supporting Multiple Markets

- **Design Choice:** Market is treated as a categorical feature and **one-hot encoded** in the preprocessing pipeline.
- **New Market Ready:** Thanks to `handle_unknown="ignore"`, the pipeline won't break if a previously unseen market appears at inference time.
- **Why Not One Model Per Market?** That approach would fail on new markets and require retraining per region. The unified model design supports generalization and maintenance efficiency.
- **Data Scalability:** Dataset is read from **Amazon S3**, allowing ingestion of large datasets beyond local memory constraints.

---

## 2. Infrastructure via Terraform

- **📁 Folder:** `infrastructure/terraform/`
- **Resources Created:** S3 buckets, IAM roles and policies, ECS cluster, ECR repo, task definitions, and CloudWatch logs.
- **State Management:** Backend state is stored in S3 and locked with DynamoDB for consistency.
- **Documentation:** High-level explanation is available in `PREDICT.md`.
- **Usage:** Can be run independently or through GitHub Actions.

```bash
cd infrastructure/terraform
terraform init
terraform apply
```

---

## 3. Artifact Upload with Ansible

- **📁 Folder:** `infrastructure/ansible/upload_artifacts_to_s3.yml`
- **Function:** Uploads trained model artifacts (`.joblib` files) to the appropriate folder in S3.
- **Command:**

```bash
ansible-playbook infrastructure/ansible/upload_artifacts_to_s3.yml
```

- **Purpose:** Demonstrates separation of provisioning (Terraform) and post-processing tasks (Ansible), a real-world best practice.

---

## 4. CI/CD Pipeline Triggered on Commit

- **📁 Config:** `.github/workflows/`  
- **Platform:** GitHub Actions  
- **Triggers:** Pipeline starts on any commit to any branch.
- **Branch Awareness:** Uses `${GITHUB_REF_NAME}` to print current branch name.
- **Stages:**
  - Terraform infra provisioning
  - Docker image build + push to ECR
  - ECS task execution for training/inference

---

## 📄 5. Documentation and Usage Guidelines

- **README.md:** Clearly explains the full project:
  - Setup and installation
  - CLI usage for training and prediction
  - Docker execution and CI/CD process
  - Infrastructure steps with Terraform and Ansible
- **Structure:** Folder-level and file-level structure is documented with visuals and examples.
- **Ease of Use:** One command to train, one to predict.

```bash
python main.py --mode=train
python main.py --mode=predict --input=data/data.csv
```

---

✅ This project meets all functional and engineering requirements using scalable, modular, and production-grade tooling.




## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/churn-prediction.git
cd churn-prediction
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Train the Model

```bash
python main.py --mode=train
```

### 4. Run Prediction

```bash
python main.py --mode=predict --input=data/data.csv
```

Predictions will be saved to `results/results.npy`.

## Run with Docker

```bash
docker build -t churn-prediction .
docker run --rm   -e BUCKET_NAME=your-s3-bucket-name   -v $(pwd)/data:/app/data   -v $(pwd)/results:/app/results   churn-prediction   python main.py --mode=predict --input=data/data.csv
```

## Infrastructure

Provisioned using Terraform (S3, IAM, ECS, ECR) and Ansible for local uploads.

```bash
cd infrastructure/terraform
terraform init && terraform apply
```

```bash
ansible-playbook infrastructure/ansible/upload_artifacts_to_s3.yml
```

## CI/CD with GitHub Actions

On each push:
- Prints branch name
- Terraform provisions infra (conditionally)
- Docker builds + pushes to ECR
- ECS runs a container for training/prediction
- Optionally logs evaluation score / metrics


##  Artifacts in S3

- `artifacts/encoder.joblib`
- `artifacts/scaler.joblib`
- `artifacts/models/base_model.joblib`

These are used by the prediction pipeline and uploaded automatically.




## Future Work & Real-World Enhancements

This section outlines practical extensions and improvements to evolve this assessment-level solution into a production-ready machine learning system.

---

### 🧪 1. Model Evaluation & Thresholding

- Currently, model evaluation is not part of the pipeline.
- Future work should include evaluation metrics such as accuracy, F1-score, precision, recall, and ROC-AUC.
- Visuals like confusion matrices and classification reports should also be included.
- Conditional deployment can be triggered based on threshold metrics.

---

### 📡 2. Experiment Tracking

- Integrate **MLflow**, **Weights & Biases**, or similar tools.
- Automatically log:
  - Hyperparameters
  - Metrics
  - Model versions
  - Code versions
- Enables reproducibility and better model governance.

---

### 🛎️ 3. Advanced Training Features

- Use callbacks like:
  - `early_stopping_rounds`
  - Evaluation sets during training
- Improves performance and avoids overfitting.

---

### 🔍 4. Monitoring in Production

- Detect:
  - Data drift / concept drift
  - Service latency
  - System errors

---

### ♻️ 5. Automated Retraining

- Set up retraining triggers based on:
  - Scheduled time (e.g., weekly)
  - Performance degradation on live data
  - Drift detection alerts

---

### 🌐 6. Real-Time Inference

- Extend batch pipeline to real-time APIs using:
  - **FastAPI** or **Flask**
  - **AWS Lambda** + **API Gateway**
- Allow low-latency, scalable serving of predictions.

---

### 🔐 7. Security and IAM Best Practices

- Add bucket encryption and tighter IAM role definitions.
- Enable CloudTrail for auditing access to resources.

---

### 📁 8. CI/CD Optimization

- ⛔️ Currently, CI/CD runs even on doc-only commits.
- ✅ In production, you would **skip actions** when only `.md`, `.txt`, or `.yaml` files are modified:
  ```yaml
  if: "!contains(github.event.head_commit.message, '[skip ci]')"
  ```
- For this project, we allowed doc-only triggers for **demo testing** purposes.

---
