import os
import json
import urllib.request
import zipfile
import shutil
import sys

VERSION_URL = "https://raw.githubusercontent.com/freezoloto/ArbitrageScanner/main/updater/version.json"
RELEASE_URL = "https://github.com/freezoloto/ArbitrageScanner/raw/main/releases/ArbitrageScanner.zip"

def download(url, path):
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, path)

def update():
    print("Checking for updates...")

    # читаем локальную версию
    local_version = "0"
    if os.path.exists("version.txt"):
        with open("version.txt", "r") as f:
            local_version = f.read().strip()

    # читаем удалённую версию
    with urllib.request.urlopen(VERSION_URL) as r:
        remote = json.loads(r.read().decode())
        remote_version = remote["version"]

    print(f"Local version: {local_version}")
    print(f"Remote version: {remote_version}")

    if remote_version == local_version:
        print("Already up to date.")
        return

    print("Updating...")

    # скачиваем архив
    download(RELEASE_URL, "update.zip")

    # распаковываем
    with zipfile.ZipFile("update.zip", "r") as zip_ref:
        zip_ref.extractall("update_tmp")

    # переносим файлы
    for item in os.listdir("update_tmp"):
        s = os.path.join("update_tmp", item)
        d = os.path.join(".", item)

        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.move(s, d)
        else:
            shutil.move(s, d)

    shutil.rmtree("update_tmp")
    os.remove("update.zip")

    # обновляем локальную версию
    with open("version.txt", "w") as f:
        f.write(remote_version)

    print("Update complete.")

if __name__ == "__main__":
    update()
    print("Launching ArbitrageScanner...")
    os.startfile("ArbitrageScanner.exe")

