# variables.tf

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "model_bucket_name" {
  description = "S3 bucket name to store model artifacts"
  type        = string
  default     = "sagemaker-model-bucket"
}

variable "ecr_repository_name" {
  description = "ECR repository name for storing Docker image"
  type        = string
  default     = "model-repository"
}

variable "instance_type" {
  description = "Instance type for the SageMaker endpoint"
  type        = string
  default     = "ml.m5.large"
}

variable "model_image_tag" {
  description = "The tag for the Docker image in ECR"
  type        = string
  default     = "latest"
}

variable "model_data_url" {
  description = "S3 path to the model artifact"
  type        = string
  default     = "s3://my-sagemaker-model-bucket/model/model.pkl"
}

variable "model_name" {
  description = "Name of the model"
  type        = string
  default     = "model"
}
