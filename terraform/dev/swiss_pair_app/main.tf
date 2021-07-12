# ------------------------------------------------------------------------------
# Create the core VPC network infrastructure
# ------------------------------------------------------------------------------

locals {
  name      = "swiss-pair-app"
  namespace = "swiss-pair-app"
  env       = "development"
  node_env = "Development"
  is_prod   = false

  domain_name   = "ikenley.com"
  dns_subdomain = "swisspair"
}

terraform {
  required_version = ">= 0.14"

  backend "s3" {
    profile = "terraform-dev"
    region  = "us-east-1"
    bucket  = "924586450630-terraform-state"
    key     = "swiss_pair_app/terraform.tfstate"
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = "terraform-dev"
}

data "terraform_remote_state" "core" {
  backend = "s3"
  config = {
    profile = "terraform-dev"
    bucket  = "924586450630-terraform-state"
    key     = "core/terraform.tfstate"
    region  = "us-east-1"
  }
}

# ------------------------------------------------------------------------------
# Resources
# ------------------------------------------------------------------------------

module "swiss_pair_app" {
  source = "../../modules/swiss_pair_app"

  name          = local.name
  namespace     = local.namespace
  env           = local.env
  node_env      = local.node_env
  is_prod       = local.is_prod
  domain_name   = local.domain_name
  dns_subdomain = local.dns_subdomain

  vpc_id           = data.terraform_remote_state.core.outputs.vpc_id
  vpc_cidr         = data.terraform_remote_state.core.outputs.vpc_cidr
  azs              = data.terraform_remote_state.core.outputs.azs
  public_subnets   = data.terraform_remote_state.core.outputs.public_subnets
  private_subnets  = data.terraform_remote_state.core.outputs.private_subnets
  database_subnets = data.terraform_remote_state.core.outputs.database_subnets

  #host_in_public_subnets = true

  alb_arn   = data.terraform_remote_state.core.outputs.alb_public_arn
  alb_sg_id = data.terraform_remote_state.core.outputs.alb_public_sg_id

  code_pipeline_s3_bucket_name = data.terraform_remote_state.core.outputs.code_pipeline_s3_bucket_name
  source_full_repository_id    = "ikenley/pySwissPairer"
  source_branch_name           = "main"
  codestar_connection_arn      = "arn:aws:codestar-connections:us-east-1:924586450630:connection/73e9e607-3dc4-4a4d-9f81-a82c0030de6d"
  s3_artifacts_name            = data.terraform_remote_state.core.outputs.code_pipeline_s3_bucket_name

  lambda_api_function_arn = "arn:aws:lambda:us-east-1:924586450630:function:swiss-pair-app-api"

  tags = {
    Environment = "dev"
  }
}
