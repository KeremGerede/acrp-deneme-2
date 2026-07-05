terraform {
  required_version = ">= 1.3.0"
}

variable "environment" {
  default = "demo"
}

locals {
  app_name = "agentic-devops-static-layout-test"

  database_username = "admin"
  database_password = "P@ssw0rdForStaticLayoutTest123!"

  vault_username = "demo-user"
  vault_password = "VaultPasswordForPdfLayoutTest456!"
}

resource "null_resource" "static_layout_test" {
  triggers = {
    app_name          = local.app_name
    environment       = var.environment
    database_username = local.database_username
    database_password = local.database_password
    vault_username    = local.vault_username
    vault_password    = local.vault_password
  }
}

output "static_layout_test_name" {
  value = local.app_name
}