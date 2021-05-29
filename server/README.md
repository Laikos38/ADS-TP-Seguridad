# ADS-TP-Seguridad - SERVER
Trabajo práctico para Arquitectura de Software 2021.

#### Integrantes
- Avalle Borgiani Isaías
- Díaz Mac William Rodrigo Tomás
- Maurino Juan Francisco
<br/><br/>

----------------------
<br/>

## Ejecutar
### Instalar dependencias:
`pip install -r requirements.txt`
<br/><br/>
### API Key Virus Total
Ingresar a [Virus Total](https://www.virustotal.com/), registrarse y luego copiar la API key asignada a su perfil.

Luego registrar en su sistema operativo la variable de entorno `VT_API_KEY` con el valor de la API Key asignada por Virus Total:

Para Windows: `setx VT_API_KEY xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Para Linux: `export VT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
<br/><br/>
### Crear BD SQLite:
`cd ./server/ADSserver`

`python3 manage.py migrate`
<br/><br/>
### Ejecutar servidor de desarrollo:
`python3 manage.py runserver`
<br/><br/>

----------------------
<br/>

## Docker
TODO: Dockerizar proyecto.