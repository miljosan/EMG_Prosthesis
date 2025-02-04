# EMG_Prosthesis
En este repositorio se encuentran los códigos para el funcionamiento de la prótesis de brazo
Crear un Entorno Virtual (Virtual Environment)
Esto es importante para mantener tu instalación de Python organizada y evitar conflictos de dependencias. Esto solo es necesario la primera vez.

a) Crear una carpeta para el proyecto
Antes de crear el entorno virtual, crea una carpeta donde estará tu proyecto.

b) Abrir la terminal o consola Dependiendo de tu sistema operativo, abre la terminal o línea de comandos.

c) Navega a la carpeta donde quieres trabajar
Usa el comando cd para ir a la carpeta donde estará tu proyecto:

cd ruta/de/tu/proyecto

d) Crea un entorno virtual
Ejecuta este comando para crear un entorno virtual llamado venv:

python -m venv venv

Esto creará una carpeta llamada venv en tu proyecto.

e) Activa el entorno virtual
Dependiendo de tu sistema operativo, usa el siguiente comando para activarlo:

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate

Una vez activado, deberías ver algo como (venv) al inicio de tu terminal, indicando que el entorno está activo.

Actualizar pip, setuptools, y wheel
Asegúrate de que las herramientas de instalación estén actualizadas:

pip install --upgrade pip setuptools wheel

Instalar las Dependencias Necesarias

a) Instalar TensorFlow

pip install tensorflow

b) Otras dependencias comunes

pip install numpy pandas matplotlib

Descargar archivos y ejecutar el código
Si estás en Windows, descarga los archivos necesarios y colócalos en la carpeta de tu proyecto. Luego:

Abre la consola

Activa el entorno virtual

Conecta el sensor a un puerto USB

Ejecuta el archivo tiemporeal4.py:

python tiemporeal4.py

Esto mostrará los datos recibidos, hará predicciones y escribirá los resultados en predicted_pose.txt.

Si estás en Raspberry Pi, usa la carpeta control_protesis_raspberry y sigue el mismo procedimiento con los comandos correspondientes a Raspberry Pi. Ejecuta:

python tiemporeal_protesis.py

Usar el archivo en Blender
Para usar Blender:

Descarga el contenido de la carpeta blender

Abre el archivo de la prótesis en Blender

En Blender, entra a la pestaña de Scripting

Ejecuta el script preconfigurado dándole Play
Esto permitirá recibir las predicciones del archivo predicted_pose.txt y visualizar los resultados en Blender.

