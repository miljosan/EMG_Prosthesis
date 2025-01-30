import os
from tkinter import *

# Funcion para actualizar el contenido de un label
def update_label():
    if os.path.exists("/home/miguel/Desktop/tesis/predicted_pose.txt"):
        with open("/home/miguel/Desktop/tesis/predicted_pose.txt", "r") as file:
            contenido = file.read()
        label.config(text=f"Prediccion actual:\n{contenido}")  # Salto de linea con \n
    else:
        label.config(text="Esperando datos...")  # Mensaje predeterminado si no hay archivo
    root.after(1000, update_label)  # Actualiza cada segundo

# Configuraciin de la ventana principal de Tkinter
root = Tk()
root.title("Visualizador de Predicciones")
label = Label(root, text="Esperando datos...", font=("Arial", 120), justify="center")  # Centrado
label.pack(pady=20)

# Iniciar la actualizaciin del label
update_label()

# Ejecutar la ventana principal
root.mainloop()
