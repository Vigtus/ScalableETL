terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = "e234bf79-f975-4e99-8c3a-37c6811c32ee"
  tenant_id       = "ab840be7-206b-432c-bd22-4c20fdc1b261"
}

terraform {
  backend "local" {
    path = "state/terraform.tfstate"
  }
}
