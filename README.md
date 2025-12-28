# 🚀 Sistema de Reuniones Inteligentes

¡Bienvenido al **Sistema de Reuniones Inteligentes**! Esta es una solución integral desarrollada en **Python** que utiliza **Streamlit** para la interfaz de usuario y servicios automatizados para la gestión eficiente de reuniones.

## 📁 Estructura del Repositorio

* `app.py`: Interfaz principal y lógica de navegación (Streamlit).
* `email_service.py`: Lógica de backend para el envío de notificaciones.
* `test_email_connection.py`: Script de diagnóstico para la configuración de correo.
* `check_requirements.py`: Validador automático de dependencias.
* `requirements.txt`: Archivo con todas las librerías necesarias.
* `Dockerfile`: Configuración para despliegue en contenedores.
* `.env`: Configuración de variables sensibles (no incluir en producción).

## 🛠️ Requisitos Previos

* Python 3.9 o superior.
* Pip (gestor de paquetes de Python).
* Una cuenta de correo configurada para envío SMTP (ej. Gmail con contraseña de aplicación).

## 🚀 Instalación y Configuración rápida

### 1. Clonar y preparar entorno
```bash
git clone [https://github.com/DarkYenque2002/Sistema-de-Reuniones-Inteligentes.git](https://github.com/DarkYenque2002/Sistema-de-Reuniones-Inteligentes.git)
cd Sistema-de-Reuniones-Inteligentes
python -m venv venv
# Activar: 
# Windows: .\venv\Scripts\activate | Linux/Mac: source venv/bin/activate
pip install -r requirements.txt

2. Configurar Variables de Entorno
Crea un archivo llamado .env y añade tus credenciales:

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=tu_usuario@gmail.com
EMAIL_PASS=tu_clave_de_aplicacion

3. Ejecución
Para iniciar la plataforma:

streamlit run app.py

Desarrollado por DarkYenque2002
---

# 2. GUÍA DE COMPILACIÓN Y EJECUCIÓN (Visual Studio Code)
(Sigue estos comandos en la terminal de VS Code uno por uno)

### Paso A: Preparación del Entorno (Lado Backend)
Asegúrate de estar en la carpeta raíz del proyecto.

1.  **Crear el entorno virtual:**
    ```powershell
    python -m venv venv
    ```
2.  **Activar el entorno:**
    * Si usas **PowerShell** (Windows): `.\venv\Scripts\Activate.ps1`
    * Si usas **Git Bash** o **Linux**: `source venv/bin/activate`
3.  **Instalar todas las dependencias:**
    ```powershell
    pip install -r requirements.txt
    ```

### Paso B: Pruebas de Backend
Antes de lanzar la interfaz, valida que los servicios funcionan:

1.  **Verificar requisitos:**
    ```powershell
    python check_requirements.py
    ```
2.  **Probar conexión de correo:**
    ```powershell
    python test_email_connection.py
    ```

### Paso C: Ejecución del Frontend (Streamlit)
Streamlit levantará automáticamente el backend y el frontend en un servidor local.

1.  **Lanzar aplicación:**
    ```powershell
    streamlit run app.py
    ```
2.  **Ver en navegador:** Abre `http://localhost:8501` en tu navegador.

### Paso D: Compilación con Docker (Opcional)
Si quieres empaquetar todo el sistema en un contenedor:

1.  **Construir la imagen:**
    ```powershell
    docker build -t sistema-reuniones .
    ```
2.  **Correr el contenedor:**
    ```powershell
    docker run -p 8501:8501 sistema-reuniones
    ```



