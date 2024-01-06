EasyOCR es un módulo de Python que permite extraer texto de imágenes. En cuanto al apartado de deeplearning usa Pytorch. Y soporta más de 80 idiomas, puedes ver la lista de todos ellos en este enlace. 

Por cierto, si te estás preguntando, ¿qué pasa con el texto escrito a mano?, pues en su repo nos indican que podremos tener esta funcionalidad en un futuro. Al parecer aún la están desarrollando.

# Instalación de Packages

Para este modulo vamos a instalar easyocr con:
```pip install easyocr```. Automáticamente, se nos instalarán otros módulos como Numpy u OpenCV, entre otros. Sin embargo, hay que tomar en cuenta que se nos instala `OpenCV-Python-Headless` y este no nos permitirá realizar la visualización de imágenes o videos, por ello tendremos que desinstalarlo usado ```pip uninstall opencv-python-headless```.

Una vez desinstalado, podremos instalar OpenCV con pip install opencv-python. ¡Y listo!, ya tendríamos todos los paquetes a utilizar. a veces es necesario desinstalar opencv y volvel a instalarlo