import os
import time
from git import Repo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Настройки
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
WATCH_PATH = os.path.join(REPO_PATH, 'important_files')
REMOTE_URL = 'https://github.com/defolmo/py-.git'
COMMIT_MESSAGE = 'Automatic backup commit'

# Инициализация Git репозитория
repo = Repo(REPO_PATH)
assert not repo.bare

# Класс для обработки событий файловой системы
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'File modified: {event.src_path}')
        self.commit_changes()

    def on_created(self, event):
        if event.is_directory:
            return
        print(f'File created: {event.src_path}')
        self.commit_changes()

    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f'File deleted: {event.src_path}')
        self.commit_changes()

    def commit_changes(self):
        print(f'Committing changes in {REPO_PATH}')
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()

# Функция для запуска наблюдателя
def start_observer():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_PATH, recursive=True)
    observer.start()
    print(f'Watching directory: {WATCH_PATH}')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_observer()
