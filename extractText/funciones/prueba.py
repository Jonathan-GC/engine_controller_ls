import tkinter as tk

raiz = tk.Tk()
raiz.attributes('-topmost', True)
raiz.etiqueta = tk.Label(
    raiz, text="Estoy por encima de todas las ventanas\nparzibyte.me")
raiz.etiqueta.pack(side="top")
app = tk.Frame()
app.pack()
app.mainloop()