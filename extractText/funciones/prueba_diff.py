from ast import For
from difflib import SequenceMatcher

from sympy import Segment

def encontrar_similares(lista):
    grupos_similares = []

    for i, cadena1 in enumerate(lista):
        grupo = [cadena1]

        for j, cadena2 in enumerate(lista[i+1:]):
            ratio = SequenceMatcher(None, cadena1, cadena2).ratio()

            if ratio >= 0.8:  # Puedes ajustar este umbral según tus necesidades
                grupo.append(cadena2)

        if not any(set(grupo) <= set(existing_grupo) for existing_grupo in grupos_similares):
            grupos_similares.append(grupo)

    return grupos_similares

# Ejemplo de uso
lista_original = ["hola mundo", "hola mundi", "python", "pythoon", "gato", "gatoo", "perro", "perrro"]
grupos_similares = encontrar_similares(lista_original)

# Crear una lista más simple
lista_simple = [grupo[0] for grupo in grupos_similares]

print("Lista original:", lista_original)
print("Lista simple:", lista_simple)

ratio = SequenceMatcher(None, "joder", "joderr").ratio()
print(ratio)

print(set(["a", "a", "b", "c", "b"]))

LISTA = [ 
    [15, 'Bueno para respondera esta pregunta', 55],
    [60, 'quiero decirte que unade las formas mas comuneses decir', 65],
    [70, 'quiero decirte que una de las formas mas comunesles decir', 80],
    [85, 'quiero decirte que unade las formas mas comunes es decir', 85],
    [90, 'quiero decirte que una de las formas mas comunes es decir', 90],
    [95, 'quiero decirte que unade las formas mas comunes es decir', 100],
    [105, 'quiero decirte que una de las-formas mas comunes es decir', 105],
    [110, 'quiero decirteque una de las formasmas comunes es decir', 110],
    [115, 'quiero decirtequeuna de lasformas masicomunes es eecir', 120],
    [125, 'quiero decirtequeuna de lasformas mascomunes es eecir', 125],
    [130, 'quiero decirtequeunade lasformas mascomunes es decir', 130],
    [135, 'quiero decirte quuna de lasformas mascomunes es eecir', 135],
    [140, 'quiero decirteque una de lasformas mas comunes es eecir', 145],
    [150, 'quiero decirte que una de las formas mas comunes es decir', 150],
    [155, 'feliz dia', 160],
    [165, 'felizdia', 190],
    [195, 'yesdeesta manera', 200],
    [205, 'yes deesta manera', 205],
    [210, 'yesdeesta manera', 210],
    [215, 'yesdeestamanera', 215],
    [220, 'yesdeesta manera', 230],
    [235, 'FELIZ', 285],
    [290, 'DiA', 695],
    [700, 'espero te sirvas', 0],
]

palabras = []
for i, segmento in enumerate(LISTA):
    a, frase, b = segmento
    print(i, a, frase, b)
    palabras.append(frase)

K = encontrar_similares(palabras)

print(K)

# Crear una lista más simple
lista_simple = [grupo[0] for grupo in K]
print(lista_simple)
        