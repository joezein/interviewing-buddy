variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
}

variable "project_name" {
  description = "Friendly project name used for tagging"
  type        = string
  default     = "interview-buddy"
}

variable "environment" {
  description = "Environment name (e.g. dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_id" {
  description = "Existing VPC ID to deploy resources into"
  type        = string
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs for load balancers"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for ECS tasks and database"
  type        = list(string)
}

variable "backend_image" {
  description = "ECR image URI (with tag) for the FastAPI service"
  type        = string
}

variable "frontend_image" {
  description = "ECR image URI (with tag) for the Next.js service"
  type        = string
}

variable "backend_desired_count" {
  description = "Number of backend ECS tasks to run"
  type        = number
  default     = 2
}

variable "frontend_desired_count" {
  description = "Number of frontend ECS tasks to run"
  type        = number
  default     = 2
}

variable "db_username" {
  description = "Master username for the Postgres database"
  type        = string
  default     = "interview_admin"
}

variable "db_password" {
  description = "Master password for the Postgres database"
  type        = string
  sensitive   = true
}

variable "db_allocated_storage" {
  description = "Allocated storage in GB for the Postgres instance"
  type        = number
  default     = 20
}

variable "db_instance_class" {
  description = "Instance class for the Postgres instance"
  type        = string
  default     = "db.t4g.micro"
}

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}
