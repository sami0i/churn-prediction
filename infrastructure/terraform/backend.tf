terraform {
  backend "s3" {
    bucket         = "churn-prediction-terraform-state"
    key            = "churn-prediction-assessment/terraform.tfstate"
    region         = "eu-north-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

