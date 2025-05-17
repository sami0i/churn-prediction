terraform {
  backend "s3" {
    bucket         = "churn-prediction-terraform-state"
    key            = "state.tfstate"
    region         = "eu-north-1"
    use_lockfile   = true  # New preferred way
  }
}
