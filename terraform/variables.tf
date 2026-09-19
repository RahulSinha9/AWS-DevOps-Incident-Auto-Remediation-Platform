variable "aws_region" {
  description = "AWS region for the platform."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Short project name used in resource names."
  type        = string
  default     = "aws-devops-incident-platform"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR for the platform VPC."
  type        = string
  default     = "10.50.0.0/16"
}

variable "availability_zones" {
  description = "Two availability zones used by the lab infrastructure."
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]
}

variable "container_image" {
  description = "Container image for the incident platform. Use the ECR image after the first CI build."
  type        = string
  default     = "public.ecr.aws/docker/library/nginx:alpine"
}

variable "container_cpu" {
  description = "Fargate CPU units."
  type        = number
  default     = 512
}

variable "container_memory" {
  description = "Fargate memory in MiB."
  type        = number
  default     = 1024
}

variable "desired_count" {
  description = "Initial ECS task count."
  type        = number
  default     = 1
}

variable "max_task_count" {
  description = "Maximum ECS task count for autoscaling."
  type        = number
  default     = 4
}

variable "alarm_cpu_threshold" {
  description = "ECS CPU percentage that triggers the incident pipeline."
  type        = number
  default     = 80
}

variable "alarm_5xx_threshold" {
  description = "ALB HTTP 5xx count threshold."
  type        = number
  default     = 5
}

variable "enable_rds" {
  description = "Create a small PostgreSQL RDS instance for the database incident scenario. It incurs AWS charges."
  type        = bool
  default     = false
}

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "incidentdemo"
}

variable "db_username" {
  description = "PostgreSQL master username."
  type        = string
  default     = "incidentadmin"
}

variable "db_password" {
  description = "PostgreSQL master password. Supply via tfvars or environment; never commit it."
  type        = string
  sensitive   = true
  default     = null
}
