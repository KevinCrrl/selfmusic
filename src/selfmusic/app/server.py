# Copyright (C) 2026 KevinCrrl
# SPDX-License-Identifier: AGPL-3.0-or-later

from os import path
import random
import sys

from starlette.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import dotenv_values
import mariadb

VERSION = "0.2"

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
    print("OK: MariaDB conectado...")

cur = conn.cursor(dictionary=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")
app.mount("/music", StaticFiles(directory="music"), name="music")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    cur.execute("SELECT type FROM music GROUP BY type")
    playlists = cur.fetchall()
    playlists_msg = "Playlist por géneros musicales:"
    if len(playlists) == 0:
        playlists_msg = "Sin géneros musicales que recomendar :("
    context = {
        "request": request,
        "playlist_msg": playlists_msg,
        "playlists": playlists,
        "version": VERSION
    }
    return templates.TemplateResponse(request, "index.html", context)


@app.get("/player", response_class=HTMLResponse)
def player(request: Request, mid: int):
    cur.execute("SELECT * FROM music WHERE id = ?", (mid,))
    music = cur.fetchone()
    if music is None:
        print("ERROR: None detectado...")
        context = {
            "request": request,
            "error": "Este id no corresponde a un audio existente."
        }
        return templates.TemplateResponse(request, "error.html", context)

    mpath = f"music/{music['filename']}"

    if path.exists(mpath):
        cur.execute(
            "SELECT id, name FROM music WHERE type = ?",
            (music["type"],))

        recoms = cur.fetchall()
        random.shuffle(recoms)
        context = {
            "request": request,
            "file": mpath,
            "name": music["name"],
            "artist": music["artist"],
            "image": music["image"],
            "array": [],  # Array simulado
            # 5 primeros resultados, no se usa LIMIT en el query
            # dado que dará los mismos resultados y se busca que
            # sean diferentes en cada visita
            "recoms": recoms[:5],
            "content_msg": "Contenido relacionado:"
        }
        return templates.TemplateResponse(request, "player.html", context)

    print(f"ERROR: {mpath}: mid no encontrado.")
    context = {
        "request": request,
        "error": "Esta canción pudo ser eliminada del servidor."
    }
    return templates.TemplateResponse(
        request=request, name="error.html", context=context)


@app.get("/search", response_class=HTMLResponse)
def s_engine(request: Request, value: str):
    term = f"%{value}%"
    cur.execute(
        "SELECT id, name FROM music WHERE name LIKE ? \
OR artist LIKE ? OR type LIKE ?",
        (term, term, term))

    results = cur.fetchall()

    message = "Resultados de búsqueda:"

    if len(results) == 0:
        message = "No hay resultados para esta búsqueda."

    context = {
        "request": request,
        "message": message,
        "results": results
    }
    return templates.TemplateResponse(request, "search.html", context)


@app.get("/playlist")
def playlist(request: Request, genre: str):
    cur.execute(
        "SELECT id, name, artist, image, filename FROM music WHERE type = ?",
        (genre,))
    array: list = cur.fetchall()
    if array is None:
        print("None detectado")
        context = {
            "request": request,
            "error": "No existe una playlist con el género indicado."
        }
        return templates.TemplateResponse(request, "error.html", context)
    random.shuffle(array)
    context = {
        "request": request,
        "file": f"music/{array[0]['filename']}",
        "name": array[0]["name"],
        "artist": array[0]["artist"],
        "image": array[0]["image"],
        "recoms": [],  # recon simulado
        "content_msg": ""
    }
    del array[0]
    context["array"] = array
    return templates.TemplateResponse(request, "player.html", context)


@app.get("/license")
def license_info(request: Request):
    return templates.TemplateResponse(request, "license.html")
