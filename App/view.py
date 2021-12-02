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
servicefile = "routes_full.csv"
airportsfile = "airports_full.csv"
citiesfile = "worldcities.csv"

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
        print(i)

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
        airport= controller.totalAiports(cont)
        print("El primer aeropuerto cargado fue")
        print(airport)
        city, cant = controller.totalCities(cont)
        print("La primer ciudad cargada fue")
        print(city)
        print("\nSe cargaron " + str(cant) + " ciudades")
        
    elif int(inputs[0]) == 3:
        vertex = input("Ingrese un aeropuerto a buscar: ")
        graph = input("En que catalogo desea buscar(connectionsod/connectionstd): \n >" )
        answer = controller.searchAdjacents(cont, graph, vertex)
        for i in lt.iterator(answer):
            print(i["vertexB"])
            print(lt.size(answer))
    elif int(inputs[0]) == 4:
        pass
    
    elif int(inputs[0]) == 5:
        ciudadp = input("Ingrese una ciudad de partida: ")
        respuestas = controller.getbyCities(cont, ciudadp)
        repeatedCities(respuestas)
        ciudadll = input("Ingrese una ciudad de llegada: ")
        respuestas = controller.getbyCities(cont, ciudadll)
        repeatedCities(respuestas)
        
                
        
    elif int(inputs[0]) == 6:
        pass
    
    elif int(inputs[0]) == 7:
        pass
    
    elif int(inputs[0]) == 8:
        pass
    

    else:
        sys.exit(0)
sys.exit(0)
