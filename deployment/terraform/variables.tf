variable "prefix" {
  description = "A name which will be pre-pended to the resources created"
  type        = string
  default     = "mSi-app"
}

variable "vpc_id" {
  description = "The VPC to deploy the collector within"
  type        = string
}

variable "subnet_id" {
  description = "The subnet to deploy the collector within"
  type        = string
}

variable "instance_type" {
  description = "The instance type to use"
  type        = string
  default     = "t3.medium"
}

variable "ssh_key_name" {
  description = "The name of the SSH key-pair to attach to all EC2 nodes deployed"
  type        = string
}

variable "ssh_ip_allowlist" {
  description = "The list of CIDR ranges to allow SSH traffic from"
  type        = list(any)
  default     = ["0.0.0.0/0"]
}
