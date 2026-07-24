# SelfMusic

Self Music es un proyecto que implementa una interfaz web para la reproducción de audios locales a través de una base de datos MariaDB y un backend en Python.

El objetivo es crear un sistema simple, minimalista, eficiente, fácil de usar con botones intuitivos y sin capas innecesarias que retrasen la reproducción en el navegador del usuario.

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

Debe ubicarse en la misma carpeta donde esté ubicado el archivo `main.py`.

#### Crear la base de datos y la(s) tabla(s)

El archivo `create_db.sql` contiene comados SQL que puede correr para crear una base de datos `selfmusic` con la tabla `music` y la tabla `users`.

#### Instalar las dependencias de Python

El archivo `requirements.txt` tiene los nombres de las librerías necesarias para poderlas instalar usando un entorno virtual con `pip`.

```bash
pip install -r requirements.txt
```

#### Crear y almacenar audios en la carpeta music

Cree la carpeta `music` en el mismo directorio donde se encuentre `main.py` y mueva hacia allí los audios que tenga disponible, SelfMusic NO provee ningún tipo de audio:

```bash
mkdir music
mv <RUTA_A_TUS_AUDIOS> music/
```

#### Registrar los audios en la base de datos

El script auxiliar `music.py` automatiza el registro del contenido en `music` extrayendo la metadata de cada audio, si el audio no tiene metadata o esta corrupto, este script no funcionará, simplemente ejecutelo asi:

```bash
python music.py
```

El script no extrae el género musical, por ello en todas las canciones será Null y deberá llenarlo manualmente o con un script propio.

#### Levantar el servidor:

Puede levantar el sistema usando FastAPI:

```bash
fastapi run

# O si está haciendo pruebas de desarrollo o debugging
fastapi dev
```

Si usa un certificado y una llave generados por ejemplo, con OpenSSL, puede usar directamente uvicorn y pasarle estos archivos:

```bash
uvicorn main:app --ssl-keyfile=./key.pem --ssl-certfile=./certificate.pem --port 8000 --host 0.0.0.0
```

#### Acceder desde el navegador

Con ello, puede acceder a [http://127.0.0.1:8000](http://127.0.0.1:8000) o a [https://127.0.0.1:8000](https://127.0.0.1:8000) si usó SSL.

Verá una interfaz con un buscador y una cabecera con botones de inicio de sesión y registro (estas funciones de usuarios aún no están implementadas), si se detectaron géneros musicales en la base de datos, se mostrará debajo del motor de búsqueda una sección de playlists que agrupan las canciones que corresponden a dichos géneros musicales.

Puede encontrar más documentación sobre las funciones visitando la documentación automática:

HTTP: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

HTTPS: [https://127.0.0.1:8000/docs](https://127.0.0.1:8000/docs)

Para el uso general de la interfaz esta documentación no es necesaria, solo lo es si es usuario avanzado o quiere investigar como se realizan las solicitudes al servidor.

## Licencia y Descargo de Responsabilidad Adicional

SelfMusic se distribuye bajo los términos de la GNU Affero General Public License Versión 3 o superior, además de los descargos de responsabilidad que incluye la licencia, se añade el descargo de responsabilidad por los audios que use el usuario.

SelfMusic NO incluye audios de prueba ni de ningún tipo, el usuario o desarrollador que despliegue SelfMusic ya sea en local o en producción, es responsable del contenido que incluya en su servidor.

El objetivo de este proyecto NO es la promoción de la piratería o el uso no autorizado de material ajeno, este es un proyecto educativo y accesible para todos en términos de código, se recomienda su uso con material del cual se tenga permiso y/o material propio.
