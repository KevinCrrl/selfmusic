# SelfMusic

Self Music es un proyecto que implementa una interfaz web para la reproducción de audios locales a través de una base de datos MariaDB y un backend en Python.

El objetivo es crear un sistema simple, minimalista, eficiente, fácil de usar con botones intuitivos y sin capas innecesarias que retrasen la reproducción en el navegador del usuario.

## Documentos del repositorio

Tareas planeadas POR HACER: [TODO](docs/TODO.md)
Códido de Conducta: [CoC](docs/CODE_OF_CONDUCT.md)
Créditos: [CREDITS](docs/CREDITS.md)

## Hostear SelfMusic en local

### Entorno y programas necesarios

SelfMusic puede correr en cualquier sistema operativo en el que se pueda instalar Python y MariaDB correctamente configurados.

#### Crear un .env

El .env es necesario para no dejar secretos dentro del código fuente, como su usuario y contraseña de MariaDB.

el .env para SelfMusic debe seguir esta estructura:

```
USER=fakeuser
PASSWORD=fakepassword123
HOST=fakehost
PORT=3306
DATABASE=selfmusic
```

Debe ubicarse en la misma carpeta donde esté ubicado el archivo `main.py` (src/selfmusic).

#### Crear la base de datos y la(s) tabla(s)

El archivo `create_db.sql` contiene comados SQL que puede correr para crear una base de datos `selfmusic` con la tabla `music`.

#### Instalar las dependencias de Python

El archivo `requirements.txt` tiene los nombres de las librerías necesarias para poderlas instalar usando un entorno virtual con `pip`.

```bash
pip install -r requirements.txt
```

#### SelfMusic CLI

Dentro de src/selfmusic la carpeta `app` contiene una CLI para administrar el servidor y la base de datos, puede ver los comandos disponibles asi:

```bash
cd src/selfmusic
python -m app.selfmusic --help
```

En esta documentación tambien encontrará los usos comunes de esta CLI.

#### Registrar los audios en la base de datos

Con la CLI de SelfMusic puede automatizar el registro del contenido en `music` extrayendo la metadata de cada audio, si el audio no tiene metadata o esta corrupto, este script no funcionará, simplemente ejecutelo asi:

```bash
# En src/selfmusic
python -m app.selfmusic add-music <RUTA_A_TU_CONTENIDO>
```

#### Levantar el servidor:

Puede levantar el sistema usando FastAPI:

```bash
# En src/selfmusic
python -m app.selfmusic serve
```

Si usa un certificado y una llave generados por ejemplo, con OpenSSL, puede usar directamente uvicorn y pasarle estos archivos:

```bash
# En src/selfmusic
python -m app.selfmusic serve --ssl --key <KEY_FILE> --certificate <CERTIFICATE_FILE>
```

Puede consultar más personalizaciones del comando serve usando:

```bash
python -m app.selfmusic serve --help
```

#### Acceder desde el navegador

Con ello, puede acceder a [http://127.0.0.1:8000](http://127.0.0.1:8000) o a [https://127.0.0.1:8000](https://127.0.0.1:8000) si usó SSL.

Verá una interfaz con un buscador y una cabecera con el nombre del proyecto, si se detectaron géneros musicales en la base de datos, se mostrará debajo del motor de búsqueda una sección de playlists que agrupan las canciones que corresponden a dichos géneros musicales, al final hay un footer con enlaces como la documentación de la API y la licencia en formato HTML.

Puede encontrar más documentación sobre las funciones visitando la documentación automática:

HTTP: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

HTTPS: [https://127.0.0.1:8000/docs](https://127.0.0.1:8000/docs)

Para el uso general de la interfaz esta documentación no es necesaria, solo lo es si es usuario avanzado o quiere investigar como se realizan las solicitudes al servidor.

## Licencia y Descargo de Responsabilidad Adicional

SelfMusic se distribuye bajo los términos de la GNU Affero General Public License Versión 3 o superior, además de los descargos de responsabilidad que incluye la licencia, se añade el descargo de responsabilidad por los audios que use el usuario.

SelfMusic NO incluye audios de prueba ni de ningún tipo, el usuario o desarrollador que despliegue SelfMusic ya sea en local o en producción, es responsable del contenido que incluya en su servidor.

El objetivo de este proyecto NO es la promoción de la piratería o el uso no autorizado de material ajeno, este es un proyecto educativo y accesible para todos en términos de código, se recomienda su uso con material del cual se tenga permiso y/o material propio.

Este repositorio contiene únicamente código fuente y no recolecta datos de ningún tipo. La base de datos solo está pensada para almacenar información relacionada con el audio en el servidor. Si realizas un fork o despliegas este proyecto, asumes la total responsabilidad sobre su administración, la privacidad de los datos y cualquier funcionalidad adicional que decidas integrar (como analíticas, anuncios, rastreadores o sistema de usuarios más allá de playlists).
