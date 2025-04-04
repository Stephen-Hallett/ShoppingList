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

variable "user_object_id" {
  type = string
}

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

#APP SERVICE PLAN VARIABLES
variable "asp_sku_name" {
  type = string
}

variable "asp_os_type" {
  type = string
}

#WEB APP VARIABLES
variable "app_name" {
  type = string
}
