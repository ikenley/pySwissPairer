variable "auth_jwt_authority" {
  description = "JWT Authority endpoint for user authentication"
  sensitive   = true
}
variable "auth_cognito_users_pool_id" {
  description = "External users Cognito UserPool id"
  sensitive   = true
}
variable "auth_client_id" {
  description = "External users Cognito client id"
  sensitive   = true
}
variable "auth_aud" {
  description = "Auth aud"
  sensitive   = true
}
