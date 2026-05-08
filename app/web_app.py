from pathlib import Path

import webbrowser
import threading
import time

from flask import Flask, render_template, request, redirect, url_for, send_file

from s3_service import (
    upload_file,
    list_files,
    download_file,
    delete_file,
    delete_files,
    S3_PREFIX
)


app = Flask(__name__)


def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")


BASE_DIR = Path(__file__).resolve().parent.parent

TEMP_UPLOADS = BASE_DIR / "temp_uploads"
WEB_DOWNLOADS = BASE_DIR / "cloudvault_downloads"

TEMP_UPLOADS.mkdir(exist_ok=True)
WEB_DOWNLOADS.mkdir(exist_ok=True)


@app.route("/")
def index():

    files = list_files()

    return render_template(
        "index.html",
        files=files
    )


@app.route("/upload", methods=["POST"])
def upload():

    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        return redirect(url_for("index"))

    local_path = TEMP_UPLOADS / uploaded_file.filename

    uploaded_file.save(local_path)

    s3_key = f"{S3_PREFIX}{uploaded_file.filename}"

    upload_file(str(local_path), s3_key)

    local_path.unlink(missing_ok=True)

    return redirect(url_for("index"))


@app.route("/download")
def download():

    s3_key = request.args.get("key")

    if not s3_key:
        return redirect(url_for("index"))

    file_name = Path(s3_key).name

    local_destination = WEB_DOWNLOADS / file_name

    success = download_file(
        s3_key,
        str(local_destination)
    )

    if not success:
        return redirect(url_for("index"))

    return send_file(
        local_destination,
        as_attachment=True
    )


@app.route("/delete", methods=["POST"])
def delete():

    s3_key = request.form.get("key")

    if s3_key:
        delete_file(s3_key)

    return redirect(url_for("index"))


@app.route("/delete-selected", methods=["POST"])
def delete_selected():

    selected_keys = request.form.getlist("selected_files")

    if selected_keys:
        delete_files(selected_keys)

    return redirect(url_for("index"))


if __name__ == "__main__":

    threading.Thread(
        target=open_browser
    ).start()

    app.run(
        debug=True,
        use_reloader=False
    )