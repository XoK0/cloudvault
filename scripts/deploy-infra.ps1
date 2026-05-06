$BucketName = "cloudvault-rodrigo-t14-2026"
$Region = "us-east-1"

Write-Host "Creating S3 bucket..."

aws s3api create-bucket `
    --bucket $BucketName `
    --region $Region

Write-Host "Enabling versioning..."

aws s3api put-bucket-versioning `
    --bucket $BucketName `
    --versioning-configuration Status=Enabled

Write-Host "Bucket created successfully."