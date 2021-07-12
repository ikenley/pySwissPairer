# ------------------------------------------------------------------------------
# Prediction application
# ------------------------------------------------------------------------------

module "serverless_application" {
  source = "../serverless_application"

  name          = var.name
  env           = var.env
  node_env      = var.node_env
  is_prod       = var.is_prod
  domain_name   = var.domain_name
  dns_subdomain = var.dns_subdomain

  vpc_id           = var.vpc_id
  vpc_cidr         = var.vpc_cidr
  azs              = var.azs
  public_subnets   = var.public_subnets
  private_subnets  = var.private_subnets
  database_subnets = var.database_subnets

  #host_in_public_subnets = var.host_in_public_subnets

  alb_arn   = var.alb_arn
  alb_sg_id = var.alb_sg_id

  code_pipeline_s3_bucket_name = var.code_pipeline_s3_bucket_name
  source_full_repository_id    = var.source_full_repository_id
  source_branch_name           = var.source_branch_name
  codestar_connection_arn      = var.codestar_connection_arn
  s3_artifacts_name            = var.s3_artifacts_name

  lambda_api_function_arn = var.lambda_api_function_arn

  tags = var.tags
}

# ------------------------------------------------------------------------------
# Dynamo tables
# ------------------------------------------------------------------------------

# module "dynamo_users" {
#   source = "../../modules/dynamo_table"

#   namespace = var.namespace
#   env       = var.env
#   is_prod   = var.is_prod

#   name     = "Users"
#   hash_key = "Id"

#   attributes = [{ "name" : "Id", "type" : "S" }]

#   role_names = [
#     module.application.task_role_name,
#     module.lambda_revisit_prediction_function.lambda_role_name
#   ]
# }

# module "dynamo_predictions" {
#   source = "../../modules/dynamo_table"

#   namespace = var.namespace
#   env       = var.env
#   is_prod   = var.is_prod

#   name      = "Predictions"
#   hash_key  = "UserId"
#   range_key = "Id"

#   role_names = [
#     module.application.task_role_name,
#     module.lambda_revisit_prediction_function.lambda_role_name
#   ]

#   attributes = [
#     { "name" : "Id", "type" : "S" },
#     { "name" : "UserId", "type" : "S" },
#     { "name" : "RevisitOn", "type" : "S" }
#   ]

#   global_secondary_index = [{
#     name               = "RevisitOn"
#     write_capacity     = 1
#     read_capacity      = 1
#     hash_key           = "RevisitOn"
#     range_key          = "UserId"
#     projection_type    = "INCLUDE"
#     non_key_attributes = ["Id", "Name"]
#   }]
# }

# ------------------------------------------------------------------------------
# Lambda API  Function
# ------------------------------------------------------------------------------

# module "lambda_api" {
#   source = "terraform-aws-modules/lambda/aws"

#   function_name = "${var.namespace}-api"
#   description   = "API backend for serverless application"
#   handler       = "index.lambda_handler"
#   runtime       = "python3.8"
#   publish       = true

#   source_path = "${path.module}/hello_lambda"

#   environment_variables = {
#     Serverless             = "Terraform"
#     # USERS_TABLE_NAME       = module.dynamo_users.table_name
#     # PREDICTIONS_TABLE_NAME = module.dynamo_predictions.table_name
#     # SES_EMAIL_ADDRESS      = var.ses_email_address
#   }

#   tags = var.tags
# }

# resource "aws_iam_policy" "revisit_prediction_function" {
#   name = "${var.name}-revisit-prediction-function-policy"

#   policy = templatefile("${path.module}/revisit_prediction_function_policy.json", {
#     ses_email_arn = var.ses_email_arn
#   })
# }

# resource "aws_iam_role_policy_attachment" "revisit_prediction_function_attach" {
#   role       = module.lambda_revisit_prediction_function.lambda_role_name
#   policy_arn = aws_iam_policy.revisit_prediction_function.arn
# }

# module "eventbridge_revisit_prediction_function" {
#   source  = "terraform-aws-modules/eventbridge/aws"
#   version = "1.4.0"

#   #bus_name = "${var.namespace}-bus"
#   create_bus = false

#   rules = {
#     predictions = {
#       name                = "daily-revisit-predictions"
#       description         = "Check predictions once daily"
#       schedule_expression = "cron(0 10 ? * * *)"
#       enabled             = true
#     }
#   }

#   targets = {
#     predictions = [
#       {
#         name = "trigger-revisit-prediction-function"
#         arn  = module.lambda_revisit_prediction_function.lambda_function_arn
#       }
#     ]
#   }

#   tags = var.tags
# }

# resource "aws_lambda_permission" "allow_eventbridge_revisit_prediction_function" {
#   statement_id  = "AllowExecutionFromCloudWatch"
#   action        = "lambda:InvokeFunction"
#   function_name = module.lambda_revisit_prediction_function.lambda_function_name
#   principal     = "events.amazonaws.com"
#   source_arn    = module.eventbridge_revisit_prediction_function.eventbridge_rule_arns["predictions"]
# }
