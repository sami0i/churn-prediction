# -------------------------
# ECS Cluster
# -------------------------
resource "aws_ecs_cluster" "ml_cluster" {
  name = "churn-prediction-cluster"
}

# -------------------------
# CloudWatch Log Group
# -------------------------
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/churn-prediction"
  retention_in_days = 7
}

# -------------------------
# ECS Task Definition
# -------------------------
resource "aws_ecs_task_definition" "ml_task" {
  family                   = "churn-prediction-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "ml-container",
      image     = "${aws_ecr_repository.ml_repo.repository_url}:latest",
      essential = true,
      environment = [
        { name = "BUCKET_NAME", value = var.bucket_name },
        { name = "UPLOAD_TO_S3", value = "true" },
        { name = "AWS_REGION", value = var.aws_region }
      ],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_logs.name,
          awslogs-region        = var.aws_region,
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}