import boto3
import json
from pathlib import Path

CONFIG_PATH = Path("config/config.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


config = load_config()

BUCKET_NAME = config["bucket_name"]
S3_PREFIX = config.get("s3_prefix", "backups/")

s3 = boto3.client("s3")


def upload_file(local_file_path, s3_key):
    try:
        s3.upload_file(local_file_path, BUCKET_NAME, s3_key)
        print(f"[UPLOAD SUCCESS] {local_file_path} -> {s3_key}")
        return True
    except Exception as error:
        print(f"[UPLOAD ERROR] {error}")
        return False


def list_files():
    try:
        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=S3_PREFIX
        )

        files = []

        if "Contents" not in response:
            return files

        for obj in response["Contents"]:
            if obj["Key"].endswith("/"):
                continue

            files.append({
                "key": obj["Key"],
                "name": obj["Key"].replace(S3_PREFIX, "", 1),
                "size": obj["Size"],
                "last_modified": obj["LastModified"]
            })

        return files

    except Exception as error:
        print(f"[LIST ERROR] {error}")
        return []


def print_files():
    files = list_files()

    print("\nFiles in bucket:\n")

    if not files:
        print("Bucket is empty.")
        return

    for file in files:
        print(file["key"])


def download_file(s3_key, local_destination):
    try:
        s3.download_file(BUCKET_NAME, s3_key, local_destination)
        print(f"[DOWNLOAD SUCCESS] {s3_key} -> {local_destination}")
        return True
    except Exception as error:
        print(f"[DOWNLOAD ERROR] {error}")
        return False