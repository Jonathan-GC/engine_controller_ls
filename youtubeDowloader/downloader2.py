from pytube import YouTube
import os

def Download(link, palabra):

    #Filtrar la palabra Clave
    palabra = palabra.strip()
    palabra = palabra.lower()
    #Crear la carpeta de Destino sino existe
    carpeta_destino = "../sources/Dictionary/" + str(palabra)
    cont_elements = 0
    
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
        print(os.path.exists(carpeta_destino))
    
    else:
        # Obtener la lista de archivos en la carpeta
        lista_archivos = os.listdir(carpeta_destino)

        # Contar la cantidad de elementos en la lista
        cantidad_items = len(lista_archivos)

        print(cantidad_items)

    

    # obtencion del link
    youtubeObject = YouTube(link)

    # Descargar en la mayor resolucion posible
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(output_path=carpeta_destino)
        os.rename(carpeta_destino + youtubeObject.title + ".mp4", str(cantidad_items+1)+".mp4")
    except:
        print("An error has occurred")
    print("Download is completed successfully")


link = input("Introcuzca la url: ")
carpeta = input("Introcuzca la palabra clave")
Download(link, carpeta)

