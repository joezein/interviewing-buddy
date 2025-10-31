output "frontend_endpoint" {
  description = "Public URL for the frontend load balancer"
  value       = "http://${aws_lb.frontend.dns_name}"
}

output "backend_endpoint" {
  description = "Public URL for the backend load balancer"
  value       = "http://${aws_lb.backend.dns_name}"
}

output "database_endpoint" {
  description = "Postgres endpoint"
  value       = aws_db_instance.this.address
}
