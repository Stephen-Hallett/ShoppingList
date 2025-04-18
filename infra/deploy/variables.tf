#AZURE VARIABLES
variable "subscription_id" {
  type = string
}

variable "client_id" {
  type = string
}

variable "client_secret" {
  type = string
}

variable "tenant_id" {
  type = string
}

# GHCR Token
variable "ghcr-token" {
  type = string
}

# variable "user_object_id" {
#   type = string
# }

#COMMON VARIABLES
variable "project_id" {
  type = string
}

variable "env" {
  type = string
}

variable "location" {
  type    = string
  default = "australiaeast"
}

variable "hash_key" {
  type = string
}

