from pytube import YouTube
import os

def descargar_videos(palabras_clave, carpeta_destino="../sources/Dictionary"):

    #Crear la carpeta de Destino sino existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)


    #busqueda de youtube con palabras clave
    consulta = "".join(palabras_clave)
    busqueda_url = f'https://www.youtube.com/results?search_query={consulta}'
    pagina_busqueda = YouTube(busqueda_url)

    # Obtener los enlaces de los videos de los resultados de búsqueda
    video_links = pagina_busqueda.video_urls

    # Descargar cada video y guardar en la carpeta de destino
    for link in video_links:
        try:
            video = YouTube(link)
            video_stream = video.streams.filter(file_extension="mp4").first()
            video_stream.download(output_path=carpeta_destino)
            print(f"Video '{video.title}' descargado exitosamente.")
        except Exception as e:
            print(f"No se pudo descargar el video {link}. Error: {str(e)}")

if __name__ == "__main__":
    palabras_clave = input("Ingresa las palabras clave para buscar videos en YouTube (separadas por espacio): ").split()
    descargar_videos(palabras_clave)
    


