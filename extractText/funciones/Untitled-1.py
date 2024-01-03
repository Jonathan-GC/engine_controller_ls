from tkinter import ttk
import tkinter as tk
def cambio_de_temperatura():
    print(spin_temp.get())
    print(spin_temp.get()[:2])
    temp = float(spin_temp.get()[:2])
    if temp <= 17:
        consumo = "Bajo"
    elif temp <= 24:
        consumo = "Medio"
    elif temp <= 30:
        consumo = "Alto"
    etiqueta_consumo["text"] = f"Consumo de energía: {consumo}."
root = tk.Tk()
root.config(width=300, height=200)
root.title("Termostato virtual")
etiqueta_temp = ttk.Label(text="Temperatura:")
etiqueta_temp.place(x=20, y=30, width=100)
etiqueta_consumo = ttk.Label()
etiqueta_consumo.place(x=20, y=80)
spin_temp = ttk.Spinbox(from_=10, to=30, increment=0.5, format="%.1fºC",
                        command=cambio_de_temperatura)
spin_temp.insert(1,"20ºC")
spin_temp["state"] = "readonly"
spin_temp.set("10.9°C")
cambio_de_temperatura()
spin_temp.place(x=105, y=30, width=70)

root.mainloop()