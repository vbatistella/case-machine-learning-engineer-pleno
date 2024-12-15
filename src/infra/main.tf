terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.77.0"
    }
  }
}

provider "aws" {
}

# Artifacts bucket
resource "aws_s3_bucket" "model_bucket" {
  bucket = var.model_bucket_name
}

# Upload forest model to s3
resource "aws_s3_object" "forest_model" {
  bucket = aws_s3_bucket.model_bucket.bucket
  key    = "model/model.pkl"
  source = "/app/src/model/model.pkl"
  acl    = "private"
}

# Create an ECR repository
resource "aws_ecr_repository" "my_repo" {
  name                 = var.ecr_repository_name
  image_tag_mutability = "MUTABLE"
  repository_policy    = jsonencode({
    Version = "latest"
    Statement = [
      {
        Action    = "ecr:BatchGetImage"
        Effect    = "Allow"
        Principal = "*"
        Resource  = "*"
      }
    ]
  })
}

# BYOC SageMaker model.
resource "aws_sagemaker_model" "byoc_model" {
  name                 = "${var.model_name}"
  execution_role_arn   = aws_iam_role.sagemaker_execution_role.arn
  primary_container {
    image            = "${aws_ecr_repository.model_repository.repository_url}:${var.model_image_tag}"  # Docker image URI
    model_data_url   = var.model_data_url
    environment = {
      "ENV" = "DEV"
    }
  }
}

# IAM role for SageMaker
resource "aws_iam_role" "sagemaker_execution_role" {
  name               = "sagemaker-execution-role"
  assume_role_policy = data.aws_iam_policy_document.sagemaker_assume_role_policy.json
}

# SageMaker Policy
data "aws_iam_policy_document" "sagemaker_assume_role_policy" {
  statement {
    actions   = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
  }
}

# Policies to the SageMaker role
resource "aws_iam_policy_attachment" "sagemaker_policy_attachment" {
  name       = "sagemaker-policy-attachment"
  roles      = [aws_iam_role.sagemaker_execution_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# SageMaker endpoint configuration
resource "aws_sagemaker_endpoint_configuration" "byoc_endpoint_config" {
  name = "${var.model_name}-endpoint-config"

  production_variants {
    variant_name         = "AllTrafficVariant"
    model_name           = aws_sagemaker_model.byoc_model.name
    initial_instance_count = 1
    instance_type        = var.instance_type
  }

  data_capture_config {
    enable_capture = true
    initial_sampling_percentage = 100
    destination_s3_uri = "s3://picpay-sor-bucker/model/data-capture/"
    capture_options {
      capture_mode = "Input"
    }
    capture_options {
      capture_mode = "Output"
    }
    kms_key_id = "{KMS_KEY_FOR_ENCRYPTION}" 
  }
}

# SageMaker endpoint
resource "aws_sagemaker_endpoint" "byoc_endpoint" {
  name                 = "${var.model_name}-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.byoc_endpoint_config.name
}

# Define an autoscaling target for endpoint
resource "aws_appautoscaling_target" "sagemaker_autoscaling_target" {
  max_capacity       = 3
  min_capacity       = 1
  resource_id        = "endpoint/${aws_sagemaker_endpoint.byoc_endpoint.name}/variant/AllTrafficVariant"
  scalable_dimension = "sagemaker:variant:DesiredInstanceCount"
  service_namespace  = "sagemaker"
}

# Invocation based sacling
resource "aws_appautoscaling_policy" "sagemaker_scaling_policy" {
  name               = "${var.model_name}-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.sagemaker_autoscaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.sagemaker_autoscaling_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.sagemaker_autoscaling_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "SageMakerVariantInvocationsPerInstance"
    }
    # 100 invocations -> scale up
    target_value = 100
    scale_in_cooldown  = 60
    scale_out_cooldown = 60
  }
}
