import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class StoreItem:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

root = tk.Tk()
root.title('Tienda - Objetos Comprados')
root.geometry('620x200')

# Define las columnas
columns = ('name', 'category', 'price')

tree = ttk.Treeview(root, columns=columns, show='headings')

# Define los encabezados
tree.heading('name', text='Nombre del Objeto')
tree.heading('category', text='Categoría')
tree.heading('price', text='Precio')

# Genera datos de muestra
store_items = [
    StoreItem('Camisa', 'Ropa', 25.99),
    StoreItem('Pantalón', 'Ropa', 39.99),
    StoreItem('Gorra', 'Accesorio', 12.49),
    StoreItem('Zapatos', 'Calzado', 54.99)
]

# Agrega datos al Treeview
for item in store_items:
    tree.insert('', tk.END, values=(item.name, item.category, item.price))

def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        formatted_price = '{:.2f}'.format(float(record[2]))  # Convertir a float y formatear el precio a dos decimales
        showinfo(title='Información', message=f'Nombre: {record[0]}\nCategoría: {record[1]}\nPrecio: ${formatted_price}')

tree.bind('<<TreeviewSelect>>', item_selected)

tree.grid(row=0, column=0, sticky='nsew')

# Agrega una barra de desplazamiento
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# Ejecuta la aplicación
root.mainloop()