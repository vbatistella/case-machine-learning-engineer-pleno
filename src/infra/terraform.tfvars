region              = "us-east-1"
model_bucket_name   = "picpay-desafio-sagemaker-model-bucket"
ecr_repository_name = "model-repository"
instance_type       = "ml.m5.large"
model_image_tag     = "latest"
model_data_url      = "s3://picpay-desafio-sagemaker-model-bucket/model/model.pickle"
model_name          = "anomalities-model"