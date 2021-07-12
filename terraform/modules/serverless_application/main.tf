#------------------------------------------------------------------------------
# Application
# Creates a **FULL** stack application-
# AWS Fargate service with 2 containers:
#   - "client": NGINX SPA create-react-app with a reverse proxy
#   - An API backend (in this case a .NET Core API)
#
# Resources created:
#   - DNS record + SSL cert
#   - Application Load Balancer
#   - ECR repositories
#   - ECS Task Definition
#   - ECS Fargate Cluster + Service
#   - CodePipeline/CodeBuild CI/CD pipeline
#   - IAM roles/policies for all the above
# Future iterations may require that these parts be abstracted (e.g. ALB)
#------------------------------------------------------------------------------

data "aws_caller_identity" "current" {}

locals {
  tags = merge(var.tags, {
    Terraform = true
  })
  account_id = data.aws_caller_identity.current.account_id

  # Need to create this locally to avoid circular dep
  codebuild_project_name = var.name
}

#------------------------------------------------------------------------------
# DNS
#------------------------------------------------------------------------------

data "aws_route53_zone" "this" {
  name         = "${var.domain_name}."
  private_zone = var.is_dns_private_zone
}

data "aws_lb" "this" {
  arn = var.alb_arn
}

resource "aws_route53_record" "app" {
  zone_id = data.aws_route53_zone.this.zone_id
  name    = "${var.dns_subdomain}.${var.domain_name}"
  type    = "A"

  alias {
    name                   = data.aws_lb.this.dns_name
    zone_id                = data.aws_lb.this.zone_id
    evaluate_target_health = true
  }
}

resource "aws_acm_certificate" "this" {
  count = var.is_dns_private_zone ? 0 : 1

  domain_name       = "${var.dns_subdomain}.${var.domain_name}"
  validation_method = "DNS"

  tags = local.tags

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "ssl_validation" {
  for_each = var.is_dns_private_zone ? {} : {
    for dvo in aws_acm_certificate.this[0].domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.this.zone_id
}

# ECS Fargate
# https://github.com/cn-terraform/terraform-aws-ecs-fargate

#------------------------------------------------------------------------------
# Task Definition
# https://github.com/cn-terraform/terraform-aws-ecs-fargate-task-definition
#------------------------------------------------------------------------------

# resource "aws_ecr_repository" "this" {
#   count = length(var.container_names)

#   name                 = "${var.name}-${var.container_names[count.index]}"
#   image_tag_mutability = "IMMUTABLE"

#   image_scanning_configuration {
#     scan_on_push = true
#   }
# }

# resource "aws_iam_role" "ecs_task_execution_role" {
#   name = "${var.name}-ecs-task-execution-role"
#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = "sts:AssumeRole"
#         Effect = "Allow"
#         Principal = {
#           Service = "ecs-tasks.amazonaws.com"
#         }
#       }
#     ]
#   })

#   tags = local.tags
# }

# resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy_attach" {
#   role       = aws_iam_role.ecs_task_execution_role.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
# }

# resource "aws_iam_role" "ecs_task_role" {
#   name = "${var.name}-ecs-task-role"
#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = "sts:AssumeRole"
#         Effect = "Allow"
#         Principal = {
#           Service = "ecs-tasks.amazonaws.com"
#         }
#       }
#     ]
#   })

#   tags = local.tags
# }

# resource "aws_iam_role_policy_attachment" "ecs_task_role_policy_attach" {
#   role       = aws_iam_role.ecs_task_role.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
# }

# resource "aws_iam_policy" "ecs_task_role_app_policy" {
#   name        = "${var.name}-ecs-task-policy"
#   description = "Additional permissions for ECS task application"

#   policy = templatefile("${path.module}/ecs_task_role_policy.tpl", {
#     name = var.name
#   })
# }

# resource "aws_iam_role_policy_attachment" "ecs_task_role_app_policy_attach" {
#   role       = aws_iam_role.ecs_task_role.name
#   policy_arn = aws_iam_policy.ecs_task_role_app_policy.arn
# }

# # https://github.com/cloudposse/terraform-aws-ecs-container-definition

# module "ecs_container_definition" {
#   count = length(var.container_names)

#   source  = "cloudposse/ecs-container-definition/aws"
#   version = "0.56.0"

#   container_name   = aws_ecr_repository.this[count.index].name
#   container_image  = "${aws_ecr_repository.this[count.index].repository_url}:latest"
#   container_memory = var.container_memory / length(var.container_names)
#   port_mappings = [
#     {
#       containerPort = var.container_ports[count.index]
#       hostPort      = var.container_ports[count.index]
#       protocol      = "tcp"
#     }
#   ]
#   log_configuration = {
#     logDriver = "awslogs",
#     options = {
#       awslogs-group         = "/ecs/${aws_ecr_repository.this[count.index].name}",
#       awslogs-region        = "us-east-1",
#       awslogs-stream-prefix = "ecs"
#     }
#   }
# }

# resource "aws_ecs_task_definition" "this" {
#   family = var.name

#   task_role_arn            = aws_iam_role.ecs_task_role.arn
#   execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
#   network_mode             = "awsvpc"
#   cpu                      = var.container_cpu
#   memory                   = var.container_memory
#   requires_compatibilities = ["FARGATE"]

#   container_definitions = jsonencode(
#     module.ecs_container_definition.*.json_map_object
#   )

#   lifecycle {
#     ignore_changes = [
#       # Ignore container_definitions b/c this will be managed by CodePipeline
#       container_definitions,
#     ]
#   }

#   tags = local.tags
# }

# resource "aws_cloudwatch_log_group" "this" {
#   count = length(aws_ecr_repository.this)

#   name = "/ecs/${aws_ecr_repository.this[count.index].name}"

#   tags = local.tags
# }

# ECS Service
# https://github.com/cn-terraform/terraform-aws-ecs-fargate-service

#------------------------------------------------------------------------------
# AWS ECS SERVICE
#------------------------------------------------------------------------------

# locals {
#   # Default to variable if exists, else create new cluster
#   ecs_cluster_arn  = var.ecs_cluster_arn == "" ? aws_ecs_cluster.this[0].arn : var.ecs_cluster_arn
#   ecs_cluster_name = var.ecs_cluster_name == "" ? aws_ecs_cluster.this[0].name : var.ecs_cluster_name
# }

# resource "aws_ecs_cluster" "this" {
#   count = var.ecs_cluster_arn == "" ? 1 : 0

#   name = var.name

#   tags = local.tags
# }

# resource "aws_ecs_service" "this" {
#   name                    = var.name
#   cluster                 = local.ecs_cluster_arn
#   desired_count           = var.desired_count
#   enable_ecs_managed_tags = true
#   launch_type             = "FARGATE"

#   load_balancer {
#     target_group_arn = aws_lb_target_group.lb_http_tgs.arn
#     container_name   = aws_ecr_repository.this[0].name
#     container_port   = 80
#   }

#   network_configuration {
#     security_groups  = concat([aws_security_group.ecs_tasks_sg.id], var.security_groups)
#     subnets          = var.host_in_public_subnets ? var.public_subnets : var.private_subnets
#     assign_public_ip = var.host_in_public_subnets ? true : false
#   }
#   task_definition = aws_ecs_task_definition.this.arn

#   lifecycle {
#     ignore_changes = [
#       # Ignore task_definition b/c this will be managed by CodePipeline
#       task_definition,
#     ]
#   }

#   tags = local.tags
# }

#------------------------------------------------------------------------------
# AWS LOAD BALANCER - Target Groups
#------------------------------------------------------------------------------
resource "aws_lb_target_group" "lambda_api" {
  name                          = "${var.name}-lambda-api"
  protocol                      = "HTTPS"
  vpc_id                        = var.vpc_id
  #deregistration_delay          = 300
  #slow_start                    = 0
  #load_balancing_algorithm_type = "round_robin"
  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }
  # health_check {
  #   enabled             = false
  #   interval            = 30
  #   # path                = var.health_check_path
  #   # protocol            = "HTTP"
  #   # timeout             = 5
  #   # healthy_threshold   = 3
  #   # unhealthy_threshold = 3
  #   # matcher             = "200"
  # }
  target_type = "lambda"
  tags = {
    Name = "${var.name}-lambda-api"
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb_target_group_attachment" "lambda_api" {
  target_group_arn = aws_lb_target_group.lambda_api.arn
  target_id        = var.lambda_api_function_arn
  depends_on       = [aws_lambda_permission.lambda_api]
}

resource "aws_lambda_permission" "lambda_api" {
  statement_id  = "AllowExecutionFromlb"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_api_function_arn
  principal     = "elasticloadbalancing.amazonaws.com"
  source_arn    = aws_lb_target_group.lambda_api.arn
}

#------------------------------------------------------------------------------
# AWS LOAD BALANCER - Listeners
#------------------------------------------------------------------------------

locals {
  alb_listener_rule_host = var.alb_listener_rule_host == "" ? aws_route53_record.app.name : var.alb_listener_rule_host
}

data "aws_lb_listener" "this" {
  load_balancer_arn = var.alb_arn
  port              = var.is_dns_private_zone ? 80 : 443
}

resource "aws_lb_listener_rule" "host_header_path_pattern" {
  listener_arn = data.aws_lb_listener.this.arn

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.lambda_api.arn
  }

  condition {
    host_header {
      values = [local.alb_listener_rule_host]
    }
  }

  condition {
    path_pattern {
      values = [var.alb_listener_rule_path_pattern]
    }
  }
}

resource "aws_lb_listener_certificate" "this" {
  count = var.is_dns_private_zone ? 0 : 1

  listener_arn    = data.aws_lb_listener.this.arn
  certificate_arn = aws_acm_certificate.this[0].arn
}

#------------------------------------------------------------------------------
# AWS SECURITY GROUP - ECS Tasks, allow traffic only from Load Balancer
#------------------------------------------------------------------------------
# resource "aws_security_group" "ecs_tasks_sg" {
#   name        = "${var.name}-ecs-tasks-sg"
#   description = "Allow inbound access from the LB only"
#   vpc_id      = var.vpc_id

#   tags = {
#     Name = "${var.name}-ecs-tasks-sg"
#   }
# }

# resource "aws_security_group_rule" "egress" {
#   security_group_id = aws_security_group.ecs_tasks_sg.id
#   type              = "egress"
#   from_port         = 0
#   to_port           = 0
#   protocol          = "-1"
#   cidr_blocks       = ["0.0.0.0/0"]
# }

# resource "aws_security_group_rule" "ingress_through_http" {
#   security_group_id        = aws_security_group.ecs_tasks_sg.id
#   type                     = "ingress"
#   from_port                = 80
#   to_port                  = 80
#   protocol                 = "tcp"
#   source_security_group_id = var.alb_sg_id
# }

#------------------------------------------------------------------------------
# CodePipeline
#------------------------------------------------------------------------------

resource "aws_codepipeline" "this" {
  name     = var.name
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = var.code_pipeline_s3_bucket_name
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["SourceArtifact"]

      configuration = {
        "BranchName" : var.source_branch_name
        "ConnectionArn" : var.codestar_connection_arn
        "FullRepositoryId" : var.source_full_repository_id
        "OutputArtifactFormat" : "CODE_ZIP"
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["SourceArtifact"]
      output_artifacts = ["BuildArtifact"]
      version          = "1"

      configuration = {
        ProjectName = local.codebuild_project_name
      }
    }
  }

  # stage {
  #   name = "Deploy"

  #   action {
  #     name            = "Deploy"
  #     category        = "Deploy"
  #     owner           = "AWS"
  #     provider        = "ECS"
  #     input_artifacts = ["BuildArtifact"]
  #     version         = "1"

  #     configuration = {
  #       "ClusterName" : local.ecs_cluster_name
  #       "ServiceName" : aws_ecs_service.this.name
  #     }
  #   }
  # }
}

resource "aws_iam_role" "codepipeline_role" {
  name = "${var.name}-codepipeline-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codepipeline.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "codepipeline_policy" {
  name = "${var.name}-codepipeline-policy"
  role = aws_iam_role.codepipeline_role.id

  policy = templatefile("${path.module}/codepipeline_policy.tpl", {
    code_pipeline_s3_bucket_name = var.code_pipeline_s3_bucket_name
  })
}

#------------------------------------------------------------------------------
# CodeBuild
#------------------------------------------------------------------------------

resource "aws_codebuild_project" "this" {
  name        = local.codebuild_project_name
  description = "CodeBuild project for ${var.name}"

  service_role = aws_iam_role.codebuild_role.arn

  artifacts {
    type = "CODEPIPELINE"
    name = aws_codepipeline.this.name
  }

  cache {
    type  = "LOCAL"
    modes = ["LOCAL_DOCKER_LAYER_CACHE"]
  }

  environment {
    type                        = "LINUX_CONTAINER"
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:5.0"
    image_pull_credentials_type = "CODEBUILD"
    #privileged_mode             = true

    environment_variable {
      name  = "ENV"
      value = var.env
    }

    environment_variable {
      name  = "NODE_ENV"
      value = var.node_env
    }

    environment_variable {
      name  = "BRANCH_NAME"
      value = var.source_branch_name
    }

    environment_variable {
      name  = "AWS_ACCOUNT_ID"
      value = local.account_id
    }

    environment_variable {
      name = "S3_ARTIFACTS_BUCKET_NAME"
      value = var.s3_artifacts_name
    }

  }

  source {
    type = "CODEPIPELINE"
  }

  tags = local.tags
}

resource "aws_iam_role" "codebuild_role" {
  name = "${var.name}-codebuild-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "codebuild_policy" {
  role = aws_iam_role.codebuild_role.name

  policy = templatefile("${path.module}/codebuild_policy.tpl", {
    account_id                   = local.account_id
    code_pipeline_s3_bucket_name = var.code_pipeline_s3_bucket_name
    codebuild_project_name       = local.codebuild_project_name
    name                         = var.name
  })
}

#------------------------------------------------------------------------------
# Configuration parameters
#------------------------------------------------------------------------------

# resource "aws_ssm_parameter" "auth_jwt_authority" {
#   name      = "/${var.name}/app/auth/jwt-authority"
#   type      = "SecureString"
#   value     = var.auth_jwt_authority
#   overwrite = true

#   tags = local.tags
# }

# resource "aws_ssm_parameter" "auth_cognito_users_pool_id" {
#   name      = "/${var.name}/app/auth/pool-id"
#   type      = "SecureString"
#   value     = var.auth_cognito_users_pool_id
#   overwrite = true
# }

# resource "aws_ssm_parameter" "auth_client_id" {
#   name      = "/${var.name}/app/auth/client-id"
#   type      = "SecureString"
#   value     = var.auth_client_id
#   overwrite = true
# }

# resource "aws_ssm_parameter" "auth_aud" {
#   name      = "/${var.name}/app/auth/aud"
#   type      = "SecureString"
#   value     = var.auth_aud
#   overwrite = true
# }
