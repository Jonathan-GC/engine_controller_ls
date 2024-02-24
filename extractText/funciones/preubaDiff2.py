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

from difflib import SequenceMatcher

listaFiltrada = []
reducir = False
for i in range(len(LISTA)):
    
    if i > len(LISTA) -2:
        break

    cadena1 = LISTA[i][1]
    cadena2 = LISTA[i+1][1]

    ratio = SequenceMatcher(None, cadena1, cadena2).ratio()
    print(ratio)
    if ratio < 0.8:
        if reducir == False:
            reducir=True
        elif reducir == True:
            reducir = False


        if i > 1 and reducir:
            listaFiltrada.append([LISTA[i][0], LISTA[i][1], LISTA[i-1][2]])
        else:
            listaFiltrada.append([LISTA[i][0], LISTA[i][1], LISTA[i][2]])
    #    pass
    else:
        reducir = True
        
print(listaFiltrada)