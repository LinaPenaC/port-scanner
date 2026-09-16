# Aplicación de Escáner de Puertos

Proyecto desarrollado para la asignatura **Redes de Computadores**.

La aplicación permite ingresar una **URL, dominio o dirección IP** y realizar un escaneo de puertos utilizando **Nmap**. Los resultados se presentan mediante una interfaz gráfica desarrollada con **Flet**, incluyendo información sobre los puertos abiertos, los servicios detectados y recomendaciones básicas de seguridad.

## Tecnologías utilizadas

- **Python** — lenguaje principal del proyecto.
- **Nmap** — herramienta utilizada como motor para realizar el escaneo de puertos.
- **python-nmap** — librería que permite utilizar Nmap desde Python.
- **Flet** — framework utilizado para desarrollar la interfaz gráfica.
- **pytest / Flet Testing** — herramientas utilizadas para las pruebas del proyecto.

## Estructura del proyecto

```text
port-scanner/
│
├── src/
│   ├── assets/
│   │   ├── icon.png
│   │   └── splash_android.png
│   │
│   ├── modules/
│   │   ├── __init__.py
│   │   └── port_scanner.py
│   │
│   └── main.py
│
├── tests/
│   └── test_main.py
│
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
````

 ## Requisitos

 Antes de ejecutar el proyecto es necesario tener instalado:

 - Python 3.10 o superior.
- Nmap.
- Las dependencias de Python del proyecto.

 ### Instalar Nmap

 Nmap debe estar instalado en el sistema operativo, ya que `python-nmap` funciona como una interfaz para ejecutar Nmap.

 En Windows se puede comprobar la instalación desde PowerShell con:

```
nmap --version
```

 La aplicación fue desarrollada y probada utilizando **Nmap 7.991 en Windows**.

 ## Instalación

 ### 1\. Clonar el repositorio

```
git clone <URL_DEL_REPOSITORIO>
cd port-scanner
```

 ### 2\. Crear un ambiente virtual

```
python -m venv .venv
```

 Activar el ambiente virtual en Windows:

```
.venv\Scripts\activate
```

 ### 3\. Instalar las dependencias

 Las principales dependencias del proyecto son Flet y `python-nmap`.

 Si se utiliza `pip`:

```
pip install flet
pip install python-nmap
```

 También se puede instalar el proyecto utilizando la configuración definida en `pyproject.toml`.

 ## Ejecución

 Desde la carpeta raíz del proyecto se puede ejecutar la aplicación con:

```
flet run src/main.py
```

 La aplicación abrirá la interfaz gráfica del escáner.

 ### Ejecución como aplicación web

 También es posible ejecutar la aplicación mediante Flet en modo web:

```
flet run --web src/main.py
```

 ## Uso

 1. Abrir la aplicación.
2. Introducir una URL, dominio o dirección IP en el campo de texto.
3. Presionar el botón **Escanear**.
4. Esperar a que finalice el escaneo.
5. Revisar el informe generado.

 Actualmente se analizan inicialmente los siguientes puertos:

 | Puerto | Servicio habitual |
| --- | --- |
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 8080 | HTTP alternativo |

Estos puertos fueron seleccionados para la primera versión debido a que corresponden a servicios de red comunes y permiten validar el funcionamiento del escáner y del sistema de recomendaciones.

 ## Ejemplo

 Como objetivo de prueba se puede utilizar:

```
scanme.nmap.org
```

 También se puede utilizar una dirección IP propia o un equipo de laboratorio autorizado para realizar pruebas.

 El informe muestra información similar a:

```
Informe de escaneo para: scanme.nmap.org
Host analizado: 45.33.32.156 (up)

Puertos abiertos encontrados:
  - Puerto 22/tcp (ssh)
  - Puerto 80/tcp (http)
```

 Los resultados pueden variar dependiendo del estado actual del servidor analizado.

 ## Arquitectura básica

 La aplicación separa la interfaz gráfica de la lógica de escaneo:

```
Usuario
   │
   ▼
Interfaz Flet
   │
   ▼
PortScanner
   │
   ▼
python-nmap
   │
   ▼
Nmap
   │
   ▼
Resultados del escaneo
   │
   ▼
Informe y recomendaciones
```

 La clase principal del escáner se encuentra en:

```
src/modules/port_scanner.py
```

 ## Estado del proyecto

 Actualmente el proyecto cuenta con una primera versión funcional que permite:

 - Recibir una URL, dominio o dirección IP.
- Extraer el host a partir de la entrada.
- Ejecutar un escaneo mediante Nmap.
- Detectar puertos abiertos.
- Identificar los servicios asociados.
- Generar un informe.
- Mostrar recomendaciones básicas de seguridad.
- Presentar los resultados mediante una interfaz gráfica en Flet.

 El proyecto continuará desarrollándose para ampliar las funcionalidades y mejorar la interfaz y los informes en la siguiente etapa.

 ## Nota de uso

 El escáner debe utilizarse únicamente sobre sistemas propios o sobre equipos para los cuales se tenga autorización para realizar pruebas de red.

