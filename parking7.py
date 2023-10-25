import threading
import random
import time
import tkinter as tk
import sys


class Estacionamiento:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.autos = []
        self.lock = threading.Lock()
        self.frecuencia_agregar = None
        self.frecuencia_retirar = None

    def set_frecuencia_agregar(self, frecuencia):
        self.frecuencia_agregar = frecuencia

    def set_frecuencia_retirar(self, frecuencia):
        self.frecuencia_retirar = frecuencia

    def agregar_auto(self):
        while True:
            with self.lock:
                if len(self.autos) < self.capacidad:
                    self.autos.append("Auto")
                    print("Auto agregado al estacionamiento. Autos en el estacionamiento:", len(self.autos))
                else:
                    print("El estacionamiento está lleno. No se puede agregar más autos.")
            time.sleep(self.frecuencia_agregar or random.choice([0.5, 1, 2]))

    def retirar_auto(self):
        while True:
            with self.lock:
                if len(self.autos) > 0:
                    auto_retirado = self.autos.pop(0)
                    print("Auto retirado del estacionamiento. Autos en el estacionamiento:", len(self.autos))
                else:
                    print("El estacionamiento está vacío. No hay autos para retirar.")
            time.sleep(self.frecuencia_retirar or random.choice([0.5, 1, 2]))


class InterfazGrafica:
    def __init__(self, root, estacionamiento):
        self.root = root
        self.estacionamiento = estacionamiento
        self.root.title("Estacionamiento")

        self.lbl_agregar = tk.Label(root, text="Frecuencia para Añadir Autos (segundos):")
        self.lbl_agregar.pack()
        self.entry_agregar = tk.Entry(root)
        self.entry_agregar.pack()

        self.lbl_retirar = tk.Label(root, text="Frecuencia para Sacar Autos (segundos):")
        self.lbl_retirar.pack()
        self.entry_retirar = tk.Entry(root)
        self.entry_retirar.pack()

        self.btn_set_frecuencia = tk.Button(root, text="Set Frecuencia", command=self.set_frecuencias)
        self.btn_set_frecuencia.pack()

        self.btn_iniciar = tk.Button(root, text="Iniciar", command=self.iniciar)
        self.btn_iniciar.pack()

        self.btn_salida = tk.Button(root, text="Salir", command=self.salir)
        self.btn_salida.pack()

        self.frecuencia_modificada = False

    def set_frecuencias(self):
        try:
            frecuencia_agregar = float(self.entry_agregar.get())
            frecuencia_retirar = float(self.entry_retirar.get())
            self.estacionamiento.set_frecuencia_agregar(frecuencia_agregar)
            self.estacionamiento.set_frecuencia_retirar(frecuencia_retirar)
            self.frecuencia_modificada = True
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos para las frecuencias.")

    def iniciar(self):
        if not self.frecuencia_modificada:
            self.estacionamiento.set_frecuencia_agregar(None)
            self.estacionamiento.set_frecuencia_retirar(None)
        self.entry_agregar.delete(0, tk.END)
        self.entry_retirar.delete(0, tk.END)

    def salir(self):
        self.root.destroy()
        sys.exit()


# Inicializar el estacionamiento con una capacidad de 12 autos
estacionamiento = Estacionamiento(capacidad=12)

# Crear hilos para el productor y el consumidor
hilo_productor = threading.Thread(target=estacionamiento.agregar_auto, daemon=True)
hilo_consumidor = threading.Thread(target=estacionamiento.retirar_auto, daemon=True)

# Iniciar los hilos
hilo_productor.start()
hilo_consumidor.start()

# Crear la interfaz gráfica
root = tk.Tk()
interfaz = InterfazGrafica(root, estacionamiento)
root.mainloop()

# Nota: Los hilos son infinitos y deben ser terminados manualmente si deseas detener el programa.
