# 🛠️ Terraform Infrastructure Overview

This file documents the AWS resources provisioned using Terraform to support the **Churn Prediction Pipeline**, including model training, artifact storage, container orchestration, and deployment via GitHub Actions.

---

## 📦 S3 & IAM for Storage and Access

| Resource | Purpose | Required |
|---------|---------|----------|
| `aws_s3_bucket.model_bucket` | Stores data, trained models, scalers, and outputs | ✅ Yes |
| `aws_s3_bucket_versioning.versioning` | Enables version tracking for models and data | 🔸 Optional but recommended |
| `aws_iam_user.ml_engineer` | Dedicated IAM user for CI/CD access from GitHub | ✅ Yes |
| `aws_iam_access_key.ml_engineer_key` | Generates access key + secret for GitHub secrets | ✅ Yes |
| `aws_iam_policy.ml_engineer_policy` | Grants ML engineer access to read/write in S3 | ✅ Yes |
| `aws_iam_user_policy_attachment.ml_engineer_attach` | Binds S3 policy to the user | ✅ Yes |

---

## 🐳 ECR & ECS for Containerized Model Execution

| Resource | Purpose | Required |
|----------|---------|----------|
| `aws_ecr_repository.ml_repo` | Stores Docker image built by GitHub Actions | ✅ Yes |
| `aws_ecs_cluster.ml_cluster` | Runs ML containers via ECS Fargate | ✅ Yes |
| `aws_ecs_task_definition.ml_task` | Defines container, command, IAM role, logging, etc. | ✅ Yes |
| `aws_cloudwatch_log_group.ecs_logs` | Stores container logs (stdout/stderr) | 🔸 Optional but helpful |

---

## 🔐 IAM Roles and Permissions for ECS

| Resource | Purpose | Required |
|----------|---------|----------|
| `aws_iam_role.ecs_task_execution_role` | ECS Fargate runtime role for image pull, log write | ✅ Yes |
| `aws_iam_role_policy_attachment.ecs_execution_role_policy` | Grants standard ECS task permissions | ✅ Yes |
| `aws_iam_policy.ecs_s3_access` | Grants ECS tasks access to read/write S3 | ✅ Yes |
| `aws_iam_role_policy_attachment.ecs_s3_access_attach` | Binds S3 access policy to ECS role | ✅ Yes |

---

## 🔐 Additional IAM Policies for GitHub Actions

| Resource | Purpose | Required |
|----------|---------|----------|
| `aws_iam_policy.ml_engineer_ecs_policy` | Allows `ml-engineer` to run ECS tasks | ✅ Yes |
| `aws_iam_user_policy_attachment.ml_engineer_attach_ecs` | Attaches ECS access to user | ✅ Yes |
| `aws_iam_policy.ml_engineer_ecr_policy` | Allows `ml-engineer` to push Docker image to ECR | ✅ Yes |
| `aws_iam_user_policy_attachment.ml_engineer_attach_ecr` | Attaches ECR access to user | ✅ Yes |

---

## 📤 Terraform Outputs

These outputs are generated when you run `terraform apply`:

| Output | Description |
|--------|-------------|
| `bucket_name` | Name of the S3 bucket for model and data |
| `bucket_arn` | ARN of the S3 bucket |
| `ml_engineer_access_key_id` | AWS access key ID for the IAM user (sensitive) |
| `ml_engineer_secret_access_key` | AWS secret access key (sensitive) |

---

## 📎 Notes

- All resources are created in the AWS region defined via `terraform.tfvars`.
- The Terraform setup supports multiple environments by varying bucket names, resource names, and cluster names.
- `ml-engineer` user credentials should be securely stored in GitHub repository secrets for CI/CD workflows.
