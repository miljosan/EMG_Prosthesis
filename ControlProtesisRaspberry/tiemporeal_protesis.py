import serial
import numpy as np
import tensorflow as tf
import time
import RPi.GPIO as GPIO  # Biblioteca para manejar los GPIO

# Cargar el modelo previamente entrenado
model = tf.keras.models.load_model('/home/miguel/Desktop/tesis/models/mi_modelo_3clases.h5')

# Configuracion del puerto serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

BUFFER_SIZE = 300
buffer = []

# Etiquetas para las clases
clase_labels = {
    0: "descanso",
    1: "anularpinza",
    2: "punio",
}

# Configuracion de los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Asignar pines a las clases (ajustar la logica de activacion para invertir los estados)
GPIO_PINS = {
    "descanso": 22,     # Pin de descanso (se activa cuando estamos en descanso)
    "punio": 17,        # Pin de punio (se activa cuando estamos en punio)
    "anularpinza": 27   # Pin de anular pinza (se activa cuando estamos en pinza)
}

# Configurar pines como salida
for pin in GPIO_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Asegurar que todos los pines esten apagados inicialmente

# Funcion para activar el pin segon la prediccion
def activar_pin(clase_nombre):
    # Apagar todos los pines primero
    for pin in GPIO_PINS.values():
        GPIO.output(pin, GPIO.LOW)

    # Activar el pin correspondiente si existe
    if clase_nombre in GPIO_PINS:
        GPIO.output(GPIO_PINS[clase_nombre], GPIO.HIGH)
        print(f"Pin activado para: {clase_nombre}")

# Funcion para escribir la prediccion en un archivo de texto
def escribir_a_archivo(clase_nombre):
    try:
        with open('predicted_pose.txt', 'w') as file:
            file.write(clase_nombre)  # Escribir la prediccion en el archivo
            print(f"Escrito en archivo: {clase_nombre}")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")

# Funcion para predecir en tiempo real
def predecir_en_tiempo_real():
    global buffer
    try:
        while True:
            if ser.in_waiting > 0:
                sensor_data = ser.readline().decode('utf-8').strip()
                print(f"Dato recibido: {sensor_data}")

                try:
                    sensor_value = int(sensor_data)
                    buffer.append(sensor_value)

                    if len(buffer) == BUFFER_SIZE:
                        # Formatear la entrada para el modelo
                        input_data = np.array(buffer).reshape(1, BUFFER_SIZE)

                        # Realizar la prediccion
                        start_time = time.time()
                        prediccion = model.predict(input_data)
                        tiempo_prediccion = time.time() - start_time

                        # Determinar la clase predicha
                        clase_predicha = np.argmax(prediccion)
                        clase_nombre = clase_labels.get(clase_predicha, "Desconocido")

                        print(f"Prediccion final: {clase_nombre}")
                        print(f"Tiempo de prediccion: {tiempo_prediccion:.4f} segundos")

                        # Escribir la clase predicha en el archivo
                        escribir_a_archivo(clase_nombre)

                        # Activar el pin correspondiente
                        activar_pin(clase_nombre)

                        # Reiniciar el buffer
                        buffer = []

                except ValueError:
                    print("Dato recibido no valido.")

    except KeyboardInterrupt:
        print("Interrupcion por teclado. Limpiando pines...")
        GPIO.cleanup()  # Liberar los pines GPIO al salir

    except Exception as e:
        print(f"Error inesperado: {e}")
        ser.reset_input_buffer()  # Vaciar el buffer en caso de error
        GPIO.cleanup()  # Asegurarse de limpiar los pines GPIO

# Iniciar prediccion en tiempo real
predecir_en_tiempo_real()
