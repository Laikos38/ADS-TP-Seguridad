# ADS-TP-Seguridad
Trabajo práctico para Arquitectura de Software 2021.

#### Integrantes
- Avalle Borgiani Isaías
- Díaz Mac William Rodrigo Tomás
- Maurino Juan Francisco

----------------------

## Ejecutar
Puede descargar los ejecutables desde la sección de Releases, o bien clonar el repositorio ejecutando:

 `git clone https://github.com/Laikos38/ADS-TP-Seguridad.git && cd ADS-TP-Seguridad`

 `pip install -r requirements.txt`

 `python3 main.py`

 ---------------

### API Key Virus Total
Ingresar a [Virus Total](https://www.virustotal.com/), registrarse y luego copiar la API key asignada a su perfil.

Luego registrar en su sistema operativo la variable de entorno `VT_API_KEY` con el valor de la API Key asignada por Virus Total:

Para Windows: `setx VT_API_KEY xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Para Linux: `export VT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
