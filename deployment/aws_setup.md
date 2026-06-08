# AWS Setup

This document outlines the minimum steps to deploy PharmaIQ on AWS.

## Recommended Services
- Amazon ECS / EKS for container orchestration
- Amazon RDS for PostgreSQL
- Amazon S3 for document storage
- Amazon ECR for container image hosting

## Deployment Steps
1. Build and push frontend and backend Docker images to ECR.
2. Create a PostgreSQL RDS instance.
3. Configure environment variables in ECS/EKS and AWS Parameter Store.
4. Deploy `docker-compose.yml` locally for development, and migrate to ECS Task Definitions for production.
5. Use AWS CloudWatch for logs and Amazon EventBridge for scheduled model monitoring jobs.
