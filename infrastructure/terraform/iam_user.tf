resource "aws_iam_user" "ml_engineer" {
  name = "ml-engineer"
  tags = {
    Project = "churn-prediction"
  }
}

resource "aws_iam_policy" "ml_engineer_policy" {
  name        = "ml-engineer-s3-policy"
  description = "IAM policy for ML engineer to access S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.model_bucket.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.model_bucket.bucket}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "ml_engineer_attach" {
  user       = aws_iam_user.ml_engineer.name
  policy_arn = aws_iam_policy.ml_engineer_policy.arn
}

resource "aws_iam_access_key" "ml_engineer_key" {
  user = aws_iam_user.ml_engineer.name
}
