"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr, indegree
from DISClib.Utils import error as error
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import dijsktra as djk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    try: 
        analyzer = {"airports": None,
                    "connectionsod": None,
                    "connectionstd": None,
                    "countries": None,
                    "paths": None}
        analyzer["airports"] = mp.newMap(numelements=9080, maptype="PROBING", comparefunction=compareAirports)
        analyzer["connectionsod"] = gr.newGraph(datastructure="ADJ_LIST",directed= True, size=93000, comparefunction=compareAirports)
        analyzer["connectionstd"] = gr.newGraph(datastructure="ADJ_LIST",directed= False, size=93000, comparefunction=compareAirports)
        analyzer["airportsInfo"] = mp.newMap(numelements=9080, maptype="PROBING", comparefunction=compareAirports)
        analyzer["countries"] = mp.newMap(numelements=41010, maptype="PROBING", comparefunction=compareAirports)
        return analyzer
    except Exception as exp: 
        error.reraise(exp, "model:newAnalyzer") 
# Funciones para agregar informacion al catalogo
def addAirportConnection(analyzer, service):
    try:
        origin, destination = formatVertex(service)
        cleanServiceDistance(service)
        distance = float(service["distance_km"])
        distance = abs(distance)
        addStop(analyzer,"connectionsod", origin)
        addStop(analyzer,"connectionsod",destination)
        addConnection(analyzer,"connectionsod",origin,destination,distance)
        addRouteStop(analyzer, service)
        return analyzer
    except Exception as exp:
        error.reraise(exp, "model:addAirportConnection")


def addStop(analyzer,graph, stopid):
    try:
        if not gr.containsVertex(analyzer[graph], stopid):
            gr.insertVertex(analyzer[graph], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, "model:addstop")

def addRouteStop(analyzer, service):
  
    entry = mp.get(analyzer['airports'], service['Departure'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareRoutes)
        lt.addLast(lstroutes, service['Destination'])
        mp.put(analyzer['airports'], service['Departure'], lstroutes)
        
    else:
        lstroutes = entry['value']
        info = service['Destination']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
            
    return analyzer

def addRouteConnections(analyzer):
  
    lststops = mp.keySet(analyzer['airports'])
    for key in lt.iterator(lststops):
        lstroutes = mp.get(analyzer['airports'], key)['value']
        for route in lt.iterator(lstroutes):
            devuelta = mp.get(analyzer["airports"], route)
            if devuelta is not None:
                devuelta = mp.get(analyzer["airports"], route)["value"]
                pos = lt.isPresent(devuelta, key)
                if pos != 0:
                    addStop(analyzer, "connectionstd", key)
                    addStop(analyzer, "connectionstd", route)
                    addConnection(analyzer,"connectionstd", key, route, 0)
                    addConnection(analyzer,"connectionstd", route, key, 0)
                
def addAirportInfo(analyzer, airport):
    if mp.get(analyzer["airportsInfo"], airport["IATA"]) is None:
        info = {"Name": "", "City": "", "Country": "", "Latitude": "", "Longitude":""}
        info["Name"] = airport["Name"]
        info["City"] = airport["City"]
        info["Country"] = airport["Country"]
        info["Latitude"] = airport["Latitude"]
        info["Longitude"] = airport["Longitude"]
        mp.put(analyzer["airportsInfo"], airport["IATA"], info)

def addCityInfo(analyzer, airport):
    exists = mp.get(analyzer["countries"], airport["city_ascii"])
    if exists is None:
        info = {"City": "", "IATA": "", "Country": "", "Latitude": "", "Longitude":"", "Population": 0, "Id": ""}
        info["IATA"] = airport["iso3"]
        info["City"] = airport["city"]
        info["Country"] = airport["country"]
        info["Latitude"] = airport["lat"]
        info["Longitude"] = airport["lng"]
        info["Population"] = airport["population"]
        info["Id"] = airport["id"]
        mp.put(analyzer["countries"], airport["city_ascii"], info)
# Funciones para creacion de datos

def addConnection(analyzer, graph, origin, destination, distance):
    edge = gr.getEdge(analyzer[graph], origin, destination)
    i = 1
    if edge is None:
        gr.addEdge(analyzer[graph], origin, destination, distance)
    return analyzer
# Funciones de consulta
def totalStops(analyzer, graph):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer[graph])


def totalConnections(analyzer, graph):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer[graph])

def totalAirports(analyzer):
    keys = mp.keySet(analyzer["airportsInfo"])
    return mp.get(analyzer["airportsInfo"], lt.firstElement(keys))

def totalCities(analyzer):
    keys = mp.keySet(analyzer["countries"])
    cant = mp.size(analyzer["countries"])
    return mp.get(analyzer["countries"], lt.firstElement(keys)), cant
# Funciones utilizadas para comparar elementos dentro de una lista
def cleanServiceDistance(service):

    if service['distance_km'] == '':
        service['distance_km'] = 0

def searchAdjacents(analyzer, graph, vertex):
    try:
        return gr.adjacentEdges(analyzer[graph], vertex)
    except Exception:
        print("El aeropuerto no posee rutas no dirigidas")

def formatVertex(service):
    
    dep = service['Departure'] 
    des = service["Destination"]
    return dep,des


def servesConnection(analyzer,graph, airport):
    connections = analyzer[graph]
    airportsinfo = analyzer["airportsInfo"]
    airports = gr.edges(connections)
    total = lt.newList(datastructure="SINGLE_LINKED")
    cant = 0
    for airport in lt.iterator(airports):
        out = gr.outdegree(connections, airport)
        inside = gr.indegree(connections, airport)
        if out > 1 and inside > 1:
            info = mp.get(airportsinfo, airport)["value"]
            display = {"Nombre": "", "Ciudad": "", "Pais": ""}
            display["Nombre"] = info["Name"]
            display["Ciudad"] = info["City"]
            display["Pais"] = info["Country"]
            display = {airport: display}
            lt.addLast(total, display)
            cant += 1
    return total, cant

            

# Funciones de ordenamiento


def compareAirports(airport, keys):
    airportcode = keys["key"]
    if (airport== airportcode):
        return 0
    elif (airport > airportcode):
        return 1
    else: 
        return -1

def compareRoutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1
