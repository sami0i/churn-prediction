terraform {
  backend "s3" {
    bucket         = "your-terraform-bucket-name"
    key            = "churn-prediction-assessment/terraform.tfstate"
    region         = "eu-north-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
