provider "aws" {
  region = "us-east-1" # change if needed
}

resource "aws_instance" "analyzer_ec2" {
  ami           = "ami-08c40ec9ead489470" # Ubuntu 22.04 in us-east-1
  instance_type = "t3.micro"
  key_name      = "gitpod-key"                # must match an existing AWS key pair

  vpc_security_group_ids = [aws_security_group.analyzer_sg.id]

  tags = {
    Name = "securityheadersanalyzer"
  }
}

resource "aws_security_group" "analyzer_sg" {
  name        = "securityheadersanalyzer-sg"
  description = "Allow SSH and FastAPI"
  vpc_id      = "default" # uses default VPC, adjust if custom

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
