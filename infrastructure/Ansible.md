# 📦 Ansible Playbooks for Churn Prediction

This folder contains Ansible playbooks used to interact with AWS S3 for uploading datasets and model artifacts.

---

## 🗂️ Playbooks Overview

### 1. `upload_dataset_to_s3.yml`
Uploads the training dataset (`data/data.csv`) to the specified S3 bucket under the `data/` prefix.

- **Source**: `../../data/data.csv`
- **Destination**: `s3://<BUCKET_NAME>/data/data.csv`
- **How to run**:

```bash
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_REGION=your-region
export BUCKET_NAME=your-bucket-name

ansible-playbook -i localhost, -c local upload_dataset_to_s3.yml
```

---

### 2. `upload_artifacts_to_s3.yml`
Uploads all files from the `artifacts/` folder to S3 under a separate prefix `artifacts-ansible/`. Useful to separate manually-uploaded artifacts from pipeline-generated ones.

- **Source**: `../../artifacts/`
- **Destination**: `s3://<BUCKET_NAME>/artifacts-ansible/`
- **How to run**:

```bash
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_REGION=your-region
export BUCKET_NAME=your-bucket-name

ansible-playbook -i localhost, -c local upload_artifacts_to_s3.yml
```

---

## 📌 Notes

- These playbooks require the [`amazon.aws` collection](https://galaxy.ansible.com/amazon/aws). Install with:

```bash
ansible-galaxy collection install amazon.aws
```

- Make sure your AWS credentials are set in your shell environment before running the playbooks.
- These scripts are typically used for manual artifact uploads (to fulfill assessment requirements).

---

✅ These playbooks help automate uploading files to S3 without using SDKs or the AWS CLI directly.