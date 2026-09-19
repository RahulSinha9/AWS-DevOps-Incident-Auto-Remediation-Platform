# Terraform Infrastructure

This Terraform stack creates the AWS foundation for the AWS DevOps Incident & Auto-Remediation Platform.

## Resources

- VPC
- Public subnets in two Availability Zones
- Internet Gateway
- ECR repository
- ECS Fargate cluster
- ECS task definition and service
- Application Load Balancer
- ECS security groups
- CloudWatch log group
- CloudWatch CPU and ALB 5xx alarms
- EventBridge alarm-state rule
- SQS incident queue
- SQS dead-letter queue
- SNS notification topic
- DynamoDB incident/audit table
- Secrets Manager placeholder
- IAM execution and application/remediation roles
- ECS CPU target-tracking autoscaling
- Optional PostgreSQL RDS instance

## Important cost note

This is a real AWS infrastructure stack. Some resources can generate charges, especially:

- Application Load Balancer
- ECS Fargate
- NAT Gateway if added later
- RDS
- CloudWatch
- Data transfer

The current lab design intentionally avoids a NAT Gateway and runs Fargate tasks in public subnets with public IPs to keep the learning environment simpler and cheaper.

Destroy the environment when finished:

```bash
terraform destroy
```

## 1. Configure

```bash
cp terraform.tfvars.example terraform.tfvars
```

Review the values.

## 2. Initialize

```bash
terraform init
```

## 3. Format and validate

```bash
terraform fmt
terraform validate
```

## 4. Review

```bash
terraform plan
```

## 5. Create infrastructure

```bash
terraform apply
```

Type `yes` after reviewing the plan.

## 6. Get important outputs

```bash
terraform output
```

The most useful output is:

```text
alb_dns_name
ecr_repository_url
ecs_cluster_name
ecs_service_name
incident_queue_url
incident_table_name
```

## 7. Deploy the application image

The first Terraform deployment uses the image from `container_image`.

After the ECR repository exists:

```bash
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
```

Build:

```bash
docker build -t aws-devops-incident-platform:latest ..
```

Tag:

```bash
docker tag aws-devops-incident-platform:latest \
  <ECR_REPOSITORY_URL>:v1
```

Push:

```bash
docker push <ECR_REPOSITORY_URL>:v1
```

Then update `container_image` in `terraform.tfvars`:

```hcl
container_image = "<ECR_REPOSITORY_URL>:v1"
```

Apply again:

```bash
terraform apply
```

For the long-term workflow, GitHub Actions should build and push the image and then deploy the new ECS task definition.

## 8. Test the platform

Get the ALB URL:

```bash
terraform output -raw alb_dns_name
```

Health check:

```bash
curl http://$(terraform output -raw alb_dns_name)/health
```

API documentation:

```text
http://<ALB_DNS_NAME>/docs
```

## 9. Test an incident

The CloudWatch alarms are connected to EventBridge.

```text
ECS / ALB metric
       ↓
CloudWatch Alarm
       ↓
EventBridge
       ↓
SQS incident queue
       ↓
Incident platform
       ↓
Analysis
       ↓
Policy
       ↓
Remediation / approval
```

## Security design

The platform task role is deliberately limited.

It can read:

- CloudWatch
- ECS
- ALB
- RDS

It can consume messages from the incident queue and write incident state to DynamoDB.

It has only limited ECS service-update capability for the remediation workflow.

It does **not** have broad permissions such as:

- `iam:*`
- `ec2:*`
- `s3:DeleteBucket`
- `*` on all AWS APIs

High-risk remediation should remain behind an approval mechanism.

## RDS scenario

Set:

```hcl
enable_rds = true
```

Then provide a password securely.

Because RDS creates ongoing AWS cost, keep it disabled until you are ready to test the database scenario.

## Production improvements

Before using this architecture for a real production environment:

1. Move ECS tasks to private subnets.
2. Add controlled egress through a NAT Gateway or VPC endpoints.
3. Put RDS in private database subnets.
4. Use ACM + HTTPS on the ALB.
5. Add WAF.
6. Use AWS Secrets Manager for application secrets.
7. Use GitHub OIDC instead of long-lived CI credentials.
8. Split Terraform into reusable modules.
9. Add remote encrypted Terraform state with locking.
10. Add CloudTrail and centralized audit logging.
11. Add explicit approval tokens for risky remediation.
12. Add multi-account IAM boundaries and SCPs where appropriate.
