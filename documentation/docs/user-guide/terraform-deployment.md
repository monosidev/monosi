---
id: terraform-deployment
title: Deploying MonoSi with Terraform (AWS)
sidebar_label: Terraform (AWS)
---

MonoSi provides a starting point for deploying the application via Terraform. You can find the Terraform files in the `deployment/terraform` subdirectory.

Note: MonoSi Terraform files have currently only been tested and in use with AWS. If you run into issues, reach out on Slack.

## Prerequisites

MonoSi does not currently support creating a VPC or SSH key for you in these files. You will need to create/obtain:
1. SSH Key
2. VPC (and note it's ID)
3. Subnet (and note it's ID)

## Steps

1. Install Terraform on your computer, [find instructions here](https://learn.hashicorp.com/tutorials/terraform/install-cli)
2. Clone the MonoSi repository
```
git clone https://github.com/monosidev/monosi && cd monosi
```
3. Change directory to terraform files.
```
cd deployment/terraform
```
4. Update terraform.tfvars with your SSH key name, VPC ID, and subnet ID.
5. Ensure that you are authenticated locally with terraform to AWS. See [terraform docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication-and-configuration) for more details.
5. Run `terraform init`
6. Run `terraform plan` to preview changes.
7. Run `terraform apply` to start the deployment and wait for it to complete (this may take some time).
8. Terraform should provide the IP of the EC2 instance it is being deployed on. You can visit MonoSi at that address on port 3000.

