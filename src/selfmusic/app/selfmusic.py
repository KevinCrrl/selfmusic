# Copyright (C) 2026 KevinCrrl
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Manejador de SelfMusic, con el objetivo de centralizar
el despliegue del servidor, registro de contenido en la
base de datos, entre otras tareas.
"""

from os import listdir, path, makedirs
import shutil as sh
import base64
import sys

from tinytag import TinyTag
import uvicorn as uvc
import mariadb
import typer

from app.server import VERSION, conn, cur

cli = typer.Typer()


@cli.command("add-music", help="Añade los audios de una carpeta a la base \
de datos y copia el archivo a la carpeta music/")
def add_music(directory: str = "new",
              fallback_image: str = "static/favicon.ico"):
    fallback_exists = path.exists(fallback_image)
    if not path.exists(directory):
        print(f"ERROR: {directory} no existe.")
        sys.exit(1)
    if not path.exists("music"):
        makedirs("music")
    failed = 0
    for file in listdir(directory):
        dir_file = path.join(directory, file)
        tag = TinyTag.get(dir_file, image=True)
        try:
            image = base64.b64encode(tag.images.any.data).decode("utf-8")
        except AttributeError:
            if fallback_exists:
                with open(fallback_image, "rb") as img:
                    image = base64.b64encode(img.read()).decode("utf-8")
            else:
                print("ADVERTENCIA: La imagen de fallback especificada no \
existe!")
                image = None
        try:
            cur.execute(
                "INSERT INTO music (name, artist, filename, image, type) \
VALUES (?, ?, ?, ?, ?)",
                (tag.title, tag.artist, file, image, tag.genre))
        except mariadb.IntegrityError as e:
            print(f"{e} en archivo {file}")
            failed += 1
        else:
            sh.copy(dir_file, "music")

    conn.commit()

    print()
    if failed > 0:
        print(f"Proceso terminado con {failed} archivos con error.")
    else:
        print("Proceso terminado sin errores.")


@cli.command("serve", help="Inicia el servidor SelfMusic")
def serve(ssl: bool = False, host: str = "0.0.0.0", port: int = 8000,
          key: str = "key.pem", certificate: str = "certificate.pem"):
    if ssl:
        uvc.run("app.server:app", host=host, port=port, ssl_keyfile=key,
                ssl_certfile=certificate)
    else:
        uvc.run("app.server:app", host=host, port=port)

    # Cerrar conexión ya que cuando se pulsa Ctrl + C para cerrar
    # el proceso de uvicorn, Typer "atrapa" el error de interrupción
    # por teclado y no permite cerrar la conexión al final
    conn.close()


@cli.command("version", help="Muesta la versión de SelfMusic")
def version():
    print(f"SelfMusic Versión {VERSION}")


if __name__ == "__main__":
    cli()
    conn.close()
