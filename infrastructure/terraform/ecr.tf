resource "aws_ecr_repository" "ml_repo" {
  name                 = "churn-prediction-repo"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}
