import boto3
import json
import logging

from pathlib import Path


CONFIG_PATH = Path("config/config.json")


LOGS_FOLDER = Path("logs")
LOGS_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOGS_FOLDER / "activity.log"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def load_config():

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


config = load_config()

BUCKET_NAME = config["bucket_name"]

S3_PREFIX = config.get("s3_prefix", "backups/")


s3 = boto3.client("s3")


def upload_file(local_file_path, s3_key):

    try:

        s3.upload_file(
            local_file_path,
            BUCKET_NAME,
            s3_key
        )

        success_message = (
            f"[UPLOAD SUCCESS] "
            f"{local_file_path} -> {s3_key}"
        )

        print(success_message)

        logging.info(success_message)

        return True

    except Exception as error:

        error_message = (
            f"[UPLOAD ERROR] {error}"
        )

        print(error_message)

        logging.error(error_message)

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
                "name": obj["Key"].replace(
                    S3_PREFIX,
                    "",
                    1
                ),
                "size": obj["Size"],
                "last_modified": obj["LastModified"]
            })

        logging.info(
            f"[LIST FILES] Retrieved {len(files)} files"
        )

        return files

    except Exception as error:

        error_message = (
            f"[LIST ERROR] {error}"
        )

        print(error_message)

        logging.error(error_message)

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

        s3.download_file(
            BUCKET_NAME,
            s3_key,
            local_destination
        )

        success_message = (
            f"[DOWNLOAD SUCCESS] "
            f"{s3_key} -> {local_destination}"
        )

        print(success_message)

        logging.info(success_message)

        return True

    except Exception as error:

        error_message = (
            f"[DOWNLOAD ERROR] {error}"
        )

        print(error_message)

        logging.error(error_message)

        return False


def delete_file(s3_key):

    try:

        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=s3_key
        )

        success_message = f"[DELETE SUCCESS] {s3_key}"

        print(success_message)

        logging.info(success_message)

        return True

    except Exception as error:

        error_message = f"[DELETE ERROR] {s3_key} | {error}"

        print(error_message)

        logging.error(error_message)

        return False


def delete_files(s3_keys):

    results = []

    for s3_key in s3_keys:

        result = delete_file(s3_key)

        results.append({
            "key": s3_key,
            "success": result
        })

    return results