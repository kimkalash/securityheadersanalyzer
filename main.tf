provider "aws" {
  region = "us-east-1" # change region if needed
}

# 🔎 Fetch the default VPC dynamically (fixes the "default" error)
data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "analyzer_sg" {
  name        = "securityheadersanalyzer-sg"
  description = "Allow SSH and FastAPI"
  vpc_id      = data.aws_vpc.default.id

  # Allow SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow FastAPI
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "analyzer_ec2" {
  ami           = "ami-08c40ec9ead489470" # Ubuntu 22.04 in us-east-1
  instance_type = "t3.micro"
  key_name      = "gitpod-key2"            # matches the key pair you imported into AWS

  vpc_security_group_ids = [aws_security_group.analyzer_sg.id]

  tags = {
    Name = "securityheadersanalyzer"
  }
}

# Print the instance public IP after apply
output "ec2_public_ip" {
  description = "Public IP of the Security Header Analyzer EC2"
  value       = aws_instance.analyzer_ec2.public_ip
}
