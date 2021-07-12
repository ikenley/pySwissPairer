variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}

variable "name" {
  description = "Project name to use as a base for most resources"
}

variable "env" {
  description = "Environment used for tagging images etc."
}

variable "node_env" {
  description = "Node.js Environment"
}

variable "is_prod" {
  description = ""
  type        = bool
}

variable "vpc_id" {
  description = "VPC to deploy resources into"
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC. Default value is a valid CIDR, but not acceptable by AWS and should be overridden"
  type        = string
}

variable "azs" {
  description = "A list of availability zones names or ids in the region"
  type        = list(string)
}

variable "public_subnets" {
  description = "A list of public subnets inside the VPC"
  type        = list(string)
  default     = []
}

variable "private_subnets" {
  description = "A list of private subnets inside the VPC"
  type        = list(string)
  default     = []
}

variable "database_subnets" {
  description = "A list of database subnets"
  type        = list(string)
  default     = []
}

# DNS

variable "domain_name" {
  description = "Base domain name e.g. example.com"
}

variable "dns_subdomain" {
  description = "Subdomain for creating a record e.g. my-subdomain"
}

variable "is_dns_private_zone" {
  description = "Whether DNS is in private zone"
  default     = false
}

# ALB

variable "alb_arn" {}
variable "alb_sg_id" {
  description = "ALB security group id"
}

variable "alb_listener_rule_host" {
  description = "Host for ALB listener rule. Defaults to var.dns_subdomain"
  default     = ""
}

variable "alb_listener_rule_path_pattern" {
  description = "Path pattern for ALB listener rule e.g. /my-app"
  default     = "/"
}

variable "health_check_path" {
  description = "Path for target group health check"
  default     = "/"
}

# # AWS ECS Fargate cluster
# variable "ecs_cluster_arn" {
#   description = "ARN of ECS Fargate cluster. Defaults to new cluster"
#   default     = ""
# }

# variable "ecs_cluster_name" {
#   description = "Name of ECS Fargate cluster. Defaults to new cluster"
#   default     = ""
# }

# ECS Task Definition

# variable "container_names" {
#   type        = list(string)
#   description = "Names of each container. Additional resources are created for each container (e.g. ECR repos)"
#   default     = ["main"]
# }

# variable "container_ports" {
#   type        = list(number)
#   description = "Port number to expose for each container"
#   default     = [80]
# }

# variable "container_memory" {
#   type        = number
#   description = "The amount of memory (in MiB) to allow the container to use. This is a hard limit, if the container attempts to exceed the container_memory, the container is killed."
#   default     = null
# }

# variable "container_cpu" {
#   type        = number
#   description = "The number of cpu units to reserve for the container."
#   default     = 0
# }

# ECS Service

# variable "desired_count" {
#   description = "(Optional) The number of instances of the task definition to place and keep running. Defaults to 0."
#   type        = number
#   default     = 1
# }

# variable "security_groups" {
#   description = "(Optional) The security groups associated with the task or service. If you do not specify a security group, the default security group for the VPC is used."
#   type        = list(any)
#   default     = []
# }

# variable "host_in_public_subnets" {
#   description = "Whether to host Service in public subnet. Default is private. Only use to save $"
#   type        = bool
#   default     = false
# }

# CodePipeline

variable "code_pipeline_s3_bucket_name" {}
variable "source_full_repository_id" {}
variable "source_branch_name" {}
variable "codestar_connection_arn" {}
variable "s3_artifacts_name" {}

# Configuration parameters

# variable "auth_jwt_authority" {
#   description = "JWT Authority endpoint for user authentication"
#   sensitive   = true
# }
# variable "auth_cognito_users_pool_id" {
#   description = "External users Cognito UserPool id"
#   sensitive   = true
# }
# variable "auth_client_id" {
#   description = "External users Cognito client id"
#   sensitive   = true
# }
# variable "auth_aud" {
#   description = "Auth aud"
#   sensitive   = true
# }

# Lambda function

variable "lambda_api_function_arn" {
  description = "Function ARN of API lambda function"
}