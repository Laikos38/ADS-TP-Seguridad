# ADS-TP-Seguridad - SERVER
Trabajo práctico para Arquitectura de Software 2021.

#### Integrantes
- Avalle Borgiani Isaías
- Díaz Mac William Rodrigo Tomás
- Maurino Juan Francisco

----------------------

## Ejecutar
### Instalar dependencias:
`pip install -r requirements.txt`

### API Key Virus Total
Ingresar a [Virus Total](https://www.virustotal.com/), registrarse y luego copiar la API key asignada a su perfil.

Luego registrar en su sistema operativo la variable de entorno `VT_API_KEY` con el valor de la API Key asignada por Virus Total:

Para Windows: `setx VT_API_KEY xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Para Linux: `export VT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Django secret key
Setear como variable de entorno la secret key de django:

Para Windows: `setx DJANGO_SECRET xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Para Linux: `export DJANGO_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
### Crear BD SQLite:
`cd ./server/ADSserver`

`python3 manage.py migrate`

### Ejecutar servidor de desarrollo:
`python3 manage.py runserver`

----------------------

## Docker
`cd ./server/ADSserver`

`docker build --tag server:latest .`

`docker run -p 8000:8000 -e "VT_API_KEY=XXXXXXXXXXXXXXXXXXXX" -e "DJANGO_SECRET=XXXXXXXXXXXXXXXXXXXX" server`