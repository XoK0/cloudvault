from s3_service import download_file

S3_KEY = "backups/README.md"

LOCAL_DESTINATION = "cloudvault_downloads/README_downloaded.md"

download_file(S3_KEY, LOCAL_DESTINATION)