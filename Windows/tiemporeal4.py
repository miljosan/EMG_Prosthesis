import serial
import numpy as np
import tensorflow as tf
import time
import os
from tkinter import *
import threading  # Para manejar hilos

# Cargar el modelo previamente entrenado
model = tf.keras.models.load_model('models/mi_modelo8.h5')

# Configuración del puerto serial
ser = serial.Serial('COM3', 115200, timeout=1)

BUFFER_SIZE = 300
buffer = []

# Etiquetas para las clases
clase_labels = {
    0: "descanso",
    1: "indice",
    2: "anularpinza",
    3: "punio",
    4: "anular",
    5: "medio"
}

# Función para escribir la predicción en un archivo de texto
def escribir_a_archivo(clase_nombre):
    try:
        with open('predicted_pose.txt', 'w') as file:
            file.write(clase_nombre)  # Escribir la predicción en el archivo
            print(f"Escrito en archivo: {clase_nombre}")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")

# Función para predecir en tiempo real
def predecir_en_tiempo_real():
    global buffer
    while True:
        try:
            if ser.in_waiting > 0:
                sensor_data = ser.readline().decode('utf-8').strip()
                print(f"Dato recibido: {sensor_data}")

                try:
                    sensor_value = int(sensor_data)
                    buffer.append(sensor_value)

                    if len(buffer) == BUFFER_SIZE:
                        # Formatear la entrada para el modelo
                        input_data = np.array(buffer).reshape(1, BUFFER_SIZE)

                        # Realizar la predicción
                        start_time = time.time()
                        prediccion = model.predict(input_data)
                        tiempo_prediccion = time.time() - start_time

                        # Determinar la clase predicha
                        clase_predicha = np.argmax(prediccion)
                        clase_nombre = clase_labels.get(clase_predicha, "Desconocido")

                        print(f"Predicción final: {clase_nombre}")
                        print(f"Tiempo de predicción: {tiempo_prediccion:.4f} segundos")

                        # Escribir la clase predicha en el archivo
                        escribir_a_archivo(clase_nombre)

                        # Reiniciar el buffer
                        buffer = []

                except ValueError:
                    print("Dato recibido no válido.")

        except Exception as e:
            print(f"Error inesperado: {e}")
            ser.reset_input_buffer()  # Vaciar el buffer en caso de error

# Función para actualizar el contenido del label
def update_label():
    if os.path.exists('predicted_pose.txt'):
        with open('predicted_pose.txt', 'r') as file:
            contenido = file.read()
        label.config(text=f"Predicción actual:\n{contenido}")  # Salto de línea con \n
    else:
        label.config(text="Esperando datos...")
    root.after(1000, update_label)

# Configuración de la ventana principal de Tkinter
root = Tk()
root.title("Visualizador de Predicciones")
label = Label(root, text="Esperando datos...", font=("Arial", 90), justify="center")
label.pack(pady=20)

# Iniciar la actualización del label
update_label()

# Crear un hilo para la predicción en tiempo real
thread = threading.Thread(target=predecir_en_tiempo_real, daemon=True)
thread.start()

# Ejecutar la ventana principal
root.mainloop()
