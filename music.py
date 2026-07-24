# Copyright (C) 2026 KevinCrrl
# SPDX-License-Identifier: AGPL-3.0-or-later

import sys
from os import listdir, path
import base64

import mariadb
from dotenv import dotenv_values
from tinytag import TinyTag

values = dotenv_values()

try:
    conn = mariadb.connect(
        user=values["USER"],
        password=values["PASSWORD"],
        host=values["HOST"],
        port=int(values["PORT"]),
        database=values["DATABASE"]
    )
except mariadb.Error as e:
    print(f"ERROR: {e}")
    sys.exit(1)
else:
    print("OK: MariaDB connected...")

cur = conn.cursor()

for file in listdir("new"):
    tag = TinyTag.get(path.join("new", file), image=True)
    print(f"name: {tag.title}")
    try:
        image = base64.b64encode(tag.images.any.data).decode("utf-8")
    except AttributeError:
        image = None
    try:
        cur.execute(
            "INSERT INTO music (name, artist, filename, image) VALUES (?, ?, ?, ?)",
            (tag.title, tag.artist, file, image))
    except mariadb.IntegrityError as e:
        print(f"{e} en archivo {file}")

conn.commit()
conn.close()
