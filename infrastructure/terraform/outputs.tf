output "bucket_name" {
  value = aws_s3_bucket.model_bucket.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.model_bucket.arn
}

output "ml_engineer_access_key_id" {
  value       = aws_iam_access_key.ml_engineer_key.id
  sensitive   = true
}

output "ml_engineer_secret_access_key" {
  value       = aws_iam_access_key.ml_engineer_key.secret
  sensitive   = true
}
