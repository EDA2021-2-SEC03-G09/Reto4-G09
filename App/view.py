"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
servicefile = "routes-utf8-small.csv"
airportsfile = "airports-utf8-small.csv"
citiesfile = "worldcities-utf8.csv"

def repeatedCities(respuestas):
    if lt.size(respuestas) > 1:
        print("se encontraron " + str(lt.size(respuestas)) + " ciudades con el mismo nombre, por favor seleccione la correcta")
        print("-"*50)
        for i in lt.iterator(respuestas):
            print(i)
            print("-"*50)
        correcta = input("Seleccione la latitud de la ciudad de la que desee realizar la consulta: \n> ")
        for i in lt.iterator(respuestas):
            if correcta == i["Latitude"]:
                correcta = i
        return correcta
    else:
        return lt.firstElement(respuestas)

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar informacion de los vuelos")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")
    print("8- Comparar con servicio WEB externo")

def printAnswer(answer):
    for airport in lt.iterator(answer):
        name = dict.keys(airport)
        for nam in name:
            namii = nam
        print("Nombre del aeropuerto: " + namii)
        print("Informacion encontrada: \n" + str(airport[namii]))
        print("-"*100)
        print("-"*100)

def printaAirportInfo(answer):
    for airport in lt.iterator(answer):
        print("Codigo IATA: " + airport["key"])
        print("Nombre :"+ airport["value"]["Name"])
        print("City: "+ airport["value"]["City"])
        print("Pais: " + airport["value"]["Country"])
        print("-"*50)

def top(answer, todainfo):
    top= lt.newList()
    if lt.size(answer) >= 5:
        for i in range(0,5):
            lt.addFirst(top, lt.firstElement(answer))
            lt.removeFirst(answer)
        if todainfo:
            printaAirportInfo(top)
        else:
            printAnswer(top)
    else: 
        printAnswer(answer)
catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando ....")
        cont= controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando datos ....")
        controller.loadServices(cont, servicefile, airportsfile, citiesfile)
        numedges = controller.totalConnections(cont, "connectionsod")
        numvertex = controller.totalStops(cont,"connectionsod")
        print("\nSe cargaron " + str(numedges) + " rutas en el grafo general")
        print("Se cargaron " + str(numvertex) + " aeropuertos en el grafo general")
        numedges2 = controller.totalConnections(cont, "connectionstd")
        numvertex2 = controller.totalStops(cont,"connectionstd")
        print("\nSe cargaron " + str(numedges2) + " rutas en el bigrafo")
        print("Se cargaron " + str(numvertex2) + " aeropuertos en el bigrafo\n")
        airport, ultimo = controller.totalAiports(cont)
        print("El primer aeropuerto cargado fue")
        print(airport)
        print("El ultimo aeropuerto cargado fue")
        print(ultimo)
        city, cant = controller.totalCities(cont)
        print("La primer ciudad cargada fue")
        print(city)
        print("\nSe cargaron " + str(cant) + " ciudades")
        
        
    elif int(inputs[0]) == 3:
        respuesta, cant = controller.searchInter(cont)
        print("Se encontraron " + str(cant) + " aeropuertos interconectados")
        top(respuesta, False)
        
    elif int(inputs[0]) == 4:
        iata1 = input("Seleccione un primer aeropuerto: \n>")
        iata2 = input("Seleccione un segundo aeropuerto: \n>")
        cant, conect = controller.findSCC(cont, iata1, iata2)
        print("Se encontraron " + str(cant) + " aeropuertos conectados")
        if conect:
            print("El aeropuerto " + iata1 + " esta conectado con el aeropuerto " + iata2)
        else:
            print("El aeropuerto " + iata1 + " NO esta conectado con el aeropuerto " + iata2)

    
    elif int(inputs[0]) == 5:
        ciudadp = input("Ingrese una ciudad de partida: ")
        respuestas = controller.getbyCities(cont, ciudadp)
        ciudad1 = repeatedCities(respuestas)["Id"]
        ciudadll = input("Ingrese una ciudad de llegada: ")
        respuestas = controller.getbyCities(cont, ciudadll)
        ciudad2 = repeatedCities(respuestas)["Id"]
        sal, lleg, fly, ruta = controller.findShortest(cont, ciudad1, ciudad2)
        print("La distancia de la ciudad de origen al aeropuerto es de: " + str(round(sal, 2)))
        print("La distancia del aeropuerto de llegada a la ciudad de llegada es de: " + str(round(lleg, 2)))
        print("La distancia entre aeropuertos es de: " + str(fly))
        print("En total, se recorren " + str(round((sal+lleg+fly),2)) + " kilometros")
        print("La ruta area que se debe tomar es: \n")
        for i in lt.iterator(ruta):
            print(i)
            print("-"*50)

    elif int(inputs[0]) == 6:
        millas = float(input("Ingrese el numero de millas disponibles: \n>"))
        controller.searchPath(cont, millas)
    
    elif int(inputs[0]) == 7:
        iata = input("Ingrese el codigo del aeropuerto que dejara de funcionar: \n>")
        od = controller.closedAirport(cont, iata)
        print("Se encontraron " + str(lt.size(od)) + " que se verán afectados")
        print("\n" + "-"*50)
        top(od, True)


    elif int(inputs[0]) == 8:
        pass
    

    else:
        sys.exit(0)
sys.exit(0)
