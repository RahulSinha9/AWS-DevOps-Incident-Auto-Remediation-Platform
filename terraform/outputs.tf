output "vpc_id" {
  description = "Platform VPC ID."
  value       = aws_vpc.main.id
}

output "ecr_repository_url" {
  description = "Push the platform Docker image to this ECR repository."
  value       = aws_ecr_repository.platform.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name."
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECS service name."
  value       = aws_ecs_service.platform.name
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name."
  value       = aws_lb.platform.dns_name
}

output "incident_queue_url" {
  description = "SQS queue receiving CloudWatch alarm incidents."
  value       = aws_sqs_queue.incidents.url
}

output "incident_dlq_url" {
  description = "SQS dead-letter queue."
  value       = aws_sqs_queue.incident_dlq.url
}

output "incident_table_name" {
  description = "DynamoDB incident/audit table."
  value       = aws_dynamodb_table.incidents.name
}

output "notification_topic_arn" {
  description = "SNS incident notification topic."
  value       = aws_sns_topic.incidents.arn
}

output "llm_secret_arn" {
  description = "Secrets Manager secret for optional LLM credentials."
  value       = aws_secretsmanager_secret.llm.arn
}

output "ecs_task_role_arn" {
  description = "IAM task role used by the incident platform."
  value       = aws_iam_role.platform_task.arn
}

output "rds_endpoint" {
  description = "Optional PostgreSQL endpoint."
  value       = try(aws_db_instance.postgres[0].address, null)
}
