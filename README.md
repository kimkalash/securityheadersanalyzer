A FastAPI-based web application for analyzing HTTP security headers.
The app helps teams identify missing or misconfigured headers such as Strict-Transport-Security (HSTS), Content-Security-Policy (CSP), X-Frame-Options (XFO), and others.

 Problem Statement

Many web applications omit or misconfigure critical HTTP security headers, leaving exploitable gaps. This tool provides:

1) User registration & authentication (JWT-based).

2) Secure submission of URLs to analyze.

3) Automated header checks with JSON reports.

4) Persistent storage of users and scans for tracking.

Features

1) Authentication

Register/login with hashed passwords (bcrypt).
JWT tokens for secure API access.

Scanning

 Submit a URL for header analysis.

 Detect presence/absence/misconfiguration of key headers:

1) Strict-Transport-Security

2) Content-Security-Policy

3) X-Frame-Options

4) X-Content-Type-Options

5) Referrer-Policy

6) Permissions-Policy


Database

User: id, username, email, hashed_password

Scan: id, url, user_id, created_at, headers JSON

Relationship: User → Scans

Reports

JSON results per header (present/missing/weak).

List & delete scans per user.



Tech Stack

Backend: FastAPI + Uvicorn

Database: PostgreSQL (local dev with SQLite fallback)

ORM: SQLAlchemy

Auth & Security: bcrypt, JWT

HTTP Client: httpx

Containerization: Docker, docker-compose

CI/CD: GitHub Actions (pytest, build, push image


Getting Started
Prerequisites

Python 3.12+

Docker & docker-compose (for containerized setup)

# Clone repo
git clone <repo-url>
cd security-header-analyzer

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=sqlite:///./test.db" > .env
echo "JWT_SECRET=your-secret" >> .env
echo "JWT_ALGORITHM=HS256" >> .env

# Run app
uvicorn app.main:app --reload

Docker
docker-compose up --build
App runs at: http://localhost:8000/docs

Testing
pytest
