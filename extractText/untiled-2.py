cadena1 = "Silencio nocturno, estrellas testigos de secretos eternos."
cadena2 = "quiero decirte que una de las formas mas comunesles decir."
cadena3 = "Caminos cruzados, destinos entrelazados en el tiempo de IA"
cadena4 = "Baila bajo la lluvia, celebra la vida con alegría de todos"

cadena1 = "mi mama me ama"
cadena2 = "tarzan de papa"
cadena3 = "mija no me ama"
#cadena4 = "m1la No m3 ama"

x = [ord(letra) for letra in cadena1]
y = [ord(letra) for letra in cadena2]
z = [ord(letra) for letra in cadena3]
x1 = [ord(letra) for letra in cadena4]

frases = [x, y, z, x1]

promedioX = sum(x)/len(x)
promedioY = sum(y)/len(y)
promedioZ = sum(z)/len(z)
promedioA = sum(x1)/len(x1)

print(promedioX, promedioY, promedioZ, promedioA)

def calcular_similitud(i, j):
    a = np.array(frases[i])
    b = np.array(frases[j])

    from sklearn.metrics.pairwise import cosine_similarity
    X = [a]
    Y = [b]

    #print ("coseno de similitud: ", cosine_similarity(X, Y))



    from scipy.spatial.distance import cosine
    print("coseno de vectores: ", cosine(a, b))


    #print(stats.pearsonr(a, b))

    dist = np.sqrt(np.sum(np.square(a - b)))
    #print("distancia vectorial: ", dist)

    #dist = np.linalg.norm(a - b)
    print("*" * 20)



import numpy as np
from scipy import stats


calcular_similitud(0, 1)
calcular_similitud(0, 2)
calcular_similitud(0, 3)
calcular_similitud(1, 2)
calcular_similitud(1, 3)
calcular_similitud(2, 3)

