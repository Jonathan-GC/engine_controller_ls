from optparse import Values
import tkinter as tk
from tkinter import filedialog
import os
from os import listdir, sep
from os.path import isdir, join, abspath

#file_image = tk.PhotoImage(file="extractText/Icono2.png")

# Este diccionario conecta los IDs de los ítems de Tk con
# su correspondiente archivo o carpeta.
#fsobjects = {}

global Ruta_seleccionada


def abrir_directorio(PunteroArbol=None):

    #Seleccionar el directorio y permitir solamente Video del tipo mp4 y avi
    directorio_abierto = filedialog.askdirectory()

    #Captura de la ruta del archivo
    if directorio_abierto != "":
        os.chdir(directorio_abierto)
        #Cargar la ruta y llamar a la funcion para listar los directorios
        load_tree(PunteroArbol, os.getcwd())

    else:
        return None

def listardir(path):
    #Listar los directorios pertenecientes a la ruta de carpeta seleccionada
    try:
        return listdir(path)
    except PermissionError:
        print("No tienes suficientes permisos para acceder a",
            path)
        return []

def load_tree(PunteroArbol=None, path="", parent=""):
    """
    Carga el contenido del directorio especificado y lo añade
    a la lista como ítemes hijos del ítem "parent".
    """
    
    #print(type(PunteroArbol))
    #PunteroArbol.insert("", tk.END, text="Elemento 99")
    
    for fsobj in listdir(path):
        fullpath = join(path, fsobj)
        #buscar si es mp4 o avi
        if fullpath.endswith(".mp4") or fullpath.endswith(".avi"):
            child = insert_item(fsobj, fullpath, parent, PunteroArbol)
            if isdir(fullpath):
                for sub_fsobj in listdir(fullpath):
                    insert_item(sub_fsobj, join(fullpath, sub_fsobj), child, PunteroArbol)

def insert_item(name, path, parent="", PunteroArbol=None,):
            """
            Añade un archivo o carpeta a la lista y retorna el identificador
            del ítem.
            """
            #iid = PunteroArbol.insert(parent, tk.END, text=name, tags=("fstag",), image=get_icon(path))
            
            #Remplazar los "\" por el "/" reconocido de python
            path = path.replace("\\", "/")

            #Insertar los valores
            iid = PunteroArbol.insert(parent, tk.END, text=name, tags=("video",), values=(path))
            #self.fsobjects[iid] = path
            return iid

#def item_selected(event):
#    print("joder tio")


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk
    from os import listdir, sep
    from os.path import isdir, join, abspath
    class Application(ttk.Frame):
        
        def __init__(self, main_window):
            super().__init__(main_window)
            main_window.title("Explorador de archivos y carpetas")
            
            self.treeview = ttk.Treeview(self)
            self.treeview.grid(row=0, column=0, sticky="nsew")
            
            # Asociar el evento de expansión de un elemento con la
            # función correspondiente.
            self.treeview.tag_bind(
                "fstag", "<<TreeviewOpen>>", self.item_opened)
            
            # Expandir automáticamente.
            for w in (self, main_window):
                w.rowconfigure(0, weight=1)
                w.columnconfigure(0, weight=1)
            
            self.grid(row=0, column=0, sticky="nsew")
            
            # Este diccionario conecta los IDs de los ítems de Tk con
            # su correspondiente archivo o carpeta.
            self.fsobjects = {}
            
            self.file_image = tk.PhotoImage(file="C:/Users/Usuario/Downloads/engine_controller_ls/extractText/Icono2.png")
            self.folder_image = tk.PhotoImage(file="C:/Users/Usuario/Downloads/engine_controller_ls/extractText/Icono2.png")
            
            # Cargar el directorio raíz.
            self.load_tree(abspath(sep))
        
        def listdir(self, path):
            try:
                return listdir(path)
            except PermissionError:
                print("No tienes suficientes permisos para acceder a",
                    path)
                return []
        
        def get_icon(self, path):
            """
            Retorna la imagen correspondiente según se especifique
            un archivo o un directorio.
            """
            return self.folder_image if isdir(path) else self.file_image
        
        def insert_item(self, name, path, parent=""):
            """
            Añade un archivo o carpeta a la lista y retorna el identificador
            del ítem.
            """
            iid = self.treeview.insert(
                parent, tk.END, text=name, tags=("fstag",),
                image=self.get_icon(path))
            self.fsobjects[iid] = path
            return iid
        
        def load_tree(self, path, parent=""):
            """
            Carga el contenido del directorio especificado y lo añade
            a la lista como ítemes hijos del ítem "parent".
            """
            for fsobj in self.listdir(path):
                fullpath = join(path, fsobj)
                child = self.insert_item(fsobj, fullpath, parent)
                if isdir(fullpath):
                    for sub_fsobj in self.listdir(fullpath):
                        self.insert_item(sub_fsobj, join(fullpath, sub_fsobj),
                                        child)
            
        def load_subitems(self, iid):
            """
            Cargar el contenido de todas las carpetas hijas del directorio
            que se corresponde con el ítem especificado.
            """
            for child_iid in self.treeview.get_children(iid):
                if isdir(self.fsobjects[child_iid]):
                    self.load_tree(self.fsobjects[child_iid],
                                parent=child_iid)
        
        def item_opened(self, event):
            """
            Evento invocado cuando el contenido de una carpeta es abierto.
            """
            iid = self.treeview.selection()[0]
            self.load_subitems(iid)
    main_window = tk.Tk()
    app = Application(main_window)
    app.mainloop()