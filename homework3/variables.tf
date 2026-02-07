variable "credentials" {
  description = "My Credentials File"
  default     = "./my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "terraform-485315"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BQ dataset name"
  type        = string
  default     = "my_dataset"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-485315-terra-bucket"
}