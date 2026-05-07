import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from s3_service import upload_file


WATCH_FOLDER = Path("C:/CloudVaultBackup")


class BackupHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        local_path = event.src_path

        file_name = Path(local_path).name

        s3_key = f"backups/{file_name}"

        print(f"[NEW FILE DETECTED] {file_name}")

        upload_file(local_path, s3_key)

    def on_modified(self, event):

        if event.is_directory:
            return

        local_path = event.src_path

        file_name = Path(local_path).name

        s3_key = f"backups/{file_name}"

        print(f"[FILE MODIFIED] {file_name}")

        upload_file(local_path, s3_key)


observer = Observer()

observer.schedule(
    BackupHandler(),
    str(WATCH_FOLDER),
    recursive=False
)

observer.start()

print(f"Watching folder: {WATCH_FOLDER}")

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    observer.stop()

observer.join()