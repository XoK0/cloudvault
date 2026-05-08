from s3_service import upload_file
from s3_service import print_files

LOCAL_FILE = "README.md"

S3_KEY = "backups/README.md"

upload_file(LOCAL_FILE, S3_KEY)

print_files()