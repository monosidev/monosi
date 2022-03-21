output "instance" {
  value       = aws_instance.monosi.*.private_ip
  description = "PrivateIP address details"
}