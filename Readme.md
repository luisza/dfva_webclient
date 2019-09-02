# DFVA Web Client

Este cliente permite hacer parte de las funcionalidades de firma de documentos
de forma simple y permite demostrar el funcionamiento de dfva_python.

# Instalación 

    yum install -y python36 python36-virtualenv python36-certifi

    virtualenv-3 -p python36 ~/env_dfvawebclient
    source  ~/env_dfvawebclient/bin/activate

    git clone https://github.com/luisza/dfva_webclient.git
    cd dfva_webclient
    pip install -r requirements.txt 
    python3.6  manage.py runserver 0.0.0.0:8000 --insecure --noreload

# Archivos de interés

Debido a que este es un proyecto de demostración y varios archivos no son necesarios para entender el procedimiento se describen cuales 

- `src/webinterface/static/` Archivos js, css e imágenes
- `src/webinterface/sign.py` 

```
# Muestra el botón de firmado
def sign_file(request)
# Envía a firmar el documento deseado
def sign_terms_document(request, pk)
# Verifica la transacción
def termsigned_check(request, pk)
```
- `src/dfva_webclient/settings.py`  Archivo de configuración de la aplicación
- `src/webinterface/url.py` Archivo con las rutas que se atienden en la aplicaicón
- `src/webinterface/upload.py` Permite la subida parcial de archivos.

# Aspectos importantes 

Este proyecto solo pretende mostrar cómo usar dfva_python, por lo que no detalla algunas particulares de seguridad, por ejemplo es recomendable
guardar variables de control en la sesión para prevenir que entes externos puedan consultar las transacciones.
Además la información se almacena en disco y no en base de datos.    
