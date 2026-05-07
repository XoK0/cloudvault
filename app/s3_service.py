import boto3
import json
from pathlib import Path

CONFIG_PATH = Path("config/config.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


config = load_config()

BUCKET_NAME = config["bucket_name"]

s3 = boto3.client("s3")


def upload_file(local_file_path, s3_key):
    try:
        s3.upload_file(local_file_path, BUCKET_NAME, s3_key)

        print(f"[UPLOAD SUCCESS] {local_file_path} -> {s3_key}")

    except Exception as error:
        print(f"[UPLOAD ERROR] {error}")


def list_files():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)

        print("\nFiles in bucket:\n")

        if "Contents" not in response:
            print("Bucket is empty.")
            return

        for obj in response["Contents"]:
            print(obj["Key"])

    except Exception as error:
        print(f"[LIST ERROR] {error}")


def download_file(s3_key, local_destination):
    try:
        s3.download_file(BUCKET_NAME, s3_key, local_destination)

        print(f"[DOWNLOAD SUCCESS] {s3_key} -> {local_destination}")

    except Exception as error:
        print(f"[DOWNLOAD ERROR] {error}")