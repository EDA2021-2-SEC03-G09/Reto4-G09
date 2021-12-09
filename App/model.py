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


from DISClib.Algorithms.Graphs.bellmanford import distTo, hasPathTo
from DISClib.Algorithms.Graphs.bfs import pathTo
from DISClib.Algorithms.Graphs.dfo import DepthFirstOrder, comparenames
from DISClib.Algorithms.Graphs.dfs import DepthFirstSearch
from DISClib.Algorithms.Graphs.prim import PrimMST, edgesMST
from DISClib.Algorithms.Graphs.scc import KosarajuSCC, connectedComponents, reverseGraph, sccCount, stronglyConnected
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from math import radians, cos, sin, asin, sqrt
from DISClib.ADT.graph import gr, indegree, outdegree
from DISClib.Utils import error as error
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim
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
    airs = analyzer["connectionsod"] 
    lststops = mp.keySet(analyzer['airports'])
    for key in lt.iterator(lststops):
        lstroutes = mp.get(analyzer['airports'], key)['value']
        for route in lt.iterator(lstroutes):
            devuelta = mp.get(analyzer["airports"], route)
            if devuelta is not None:
                devuelta = mp.get(analyzer["airports"], route)["value"]
                pos = lt.isPresent(devuelta, key)
                if pos != 0:
                    distance = gr.getEdge(airs, key, route)["weight"]
                    addStop(analyzer, "connectionstd", key)
                    addStop(analyzer, "connectionstd", route)
                    addConnection(analyzer,"connectionstd", key, route, distance)
                

def addAirportInfo(analyzer, airport, primero):
    mp.put(analyzer["airportsInfo"], "ultimo", airport)
    if primero:
        mp.put(analyzer["airportsInfo"], "primero", airport)
    if mp.get(analyzer["airportsInfo"], airport["IATA"]) is None:
        info = {"Name": "", "City": "", "Country": "", "Latitude": "", "Longitude":""}
        info["Name"] = airport["Name"]
        info["City"] = airport["City"]
        info["Country"] = airport["Country"]
        info["Latitude"] = airport["Latitude"]
        info["Longitude"] = airport["Longitude"]
        mp.put(analyzer["airportsInfo"], airport["IATA"], info)

def addCityInfo(analyzer, airport):
    mp.put(analyzer["countries"], "ultimo", airport)
    info = {"City": "", "IATA": "", "Country": "", "Latitude": "", "Longitude":"", "Population": 0, "Id": ""}
    info["IATA"] = airport["iso3"]
    info["City"] = airport["city"]
    info["Country"] = airport["country"]
    info["Latitude"] = airport["lat"]
    info["Longitude"] = airport["lng"]
    info["Population"] = airport["population"]
    info["Id"] = airport["id"]
    info["Admin"] = airport["admin_name"]
    info["Capital"] = airport["admin_name"]
    mp.put(analyzer["countries"], info["Id"], info)
# Funciones para creacion de datos

def addConnection(analyzer, graph, origin, destination, distance):
    edge = gr.getEdge(analyzer[graph], origin, destination)
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
    primero = mp.get(analyzer["airportsInfo"], "primero")
    ultimo = mp.get(analyzer["airportsInfo"], "ultimo")
    return primero, ultimo

def totalCities(analyzer):
    ultimo = mp.get(analyzer["countries"], "ultimo")
    cant = mp.size(analyzer["countries"])
    return ultimo, cant

def getCities(analyzer, city):
    countries = analyzer["countries"]
    samename = lt.newList()
    cities = mp.keySet(countries)
    for cityrep in lt.iterator(cities):
        info = mp.get(countries, cityrep)
        info = me.getValue(info)
        try: 
            if info["City"] == city:
                lt.addLast(samename, info)
        except Exception:
            pass
    return samename
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
def compareKeys(airport1, airport2):
    if (airport1["key"]== airport2["key"]):
        return 0
    elif (airport1["key"] > airport2["key"]):
        return 1
    else: 
        return -1


def compareAirports(airport, keys):
    airportcode = (keys["key"])
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

def compareNums(route1, route2):
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1


def buildAnswer(nodeinfo, out, inside):
    info = {"City": "", "Country": "", "IATA": "", "Inbound": 0, "Outbound": 0}
    info["City"] = nodeinfo["value"]["City"]
    info["Country"] = nodeinfo["value"]["Country"]
    info["IATA"] = nodeinfo["key"]
    info["Inbound"] = inside
    info["Outbound"] = out
    dic = {nodeinfo["value"]["Name"]: info}
    return dic

def searchInter(analyzer):
    routes = analyzer["connectionsod"]
    total = lt.newList(cmpfunction=compareNums)
    connected = gr.numVertices(routes)
    nodes = gr.vertices(routes)
    for node in lt.iterator(nodes):
        out = gr.outdegree(routes, node)
        inside = gr.indegree(routes, node)
        nodeinfo = mp.get(analyzer["airportsInfo"], node)
        if out > 1 and inside > 1:
            answer = buildAnswer(nodeinfo, out, inside)
            lt.addLast(total, answer)
        elif out == 1 or inside == 1:
            adyacentes = gr.adjacents(routes,node)
            if lt.size(adyacentes) > 1:
                answer = buildAnswer(nodeinfo, out, inside)
                lt.addLast(total, answer)  
    return total, connected

def findSCC(analyzer, iata1, iata2):
    routes = analyzer["connectionsod"]
    scc = KosarajuSCC(routes)
    cant = connectedComponents(scc)
    present = gr.vertices(routes)
    conect = False
    if lt.isPresent(present, iata1) != 0 and lt.isPresent(present, iata2):
        conect = stronglyConnected(scc, iata1, iata2)
    return cant, conect

def findShortest(analyzer, ciudad1, ciudad2):
    busq = om.newMap(omaptype="RBT", comparefunction=compareRoutes)
    busq2 = om.newMap(omaptype="RBT", comparefunction=compareRoutes)
    airports = analyzer["airportsInfo"]
    keys = mp.keySet(airports)
    city1 = mp.get(analyzer["countries"], ciudad1)
    lat1, lon1 = getCoords(city1) 
    city2 = mp.get(analyzer["countries"], ciudad2)
    lat2, lon2 = getCoords(city2)
    for key in lt.iterator(keys):
        key = mp.get(airports, key)
        airportlat = key["value"]["Latitude"]
        airportlon = key["value"]["Longitude"]
        distance = haversine(float(lat1), float(lon1), float(airportlat), float(airportlon))
        distance2 = haversine(float(lat2), float(lon2), float(airportlat), float(airportlon))
        om.put(busq, distance, key["key"])
        om.put(busq2, distance2, key["key"])
    distancesal = om.minKey(busq)
    airport1 = om.get(busq, distancesal)
    distancelleg = om.minKey(busq2)
    airport2 = om.get(busq2, distancelleg)
    estbusqueda = djk.Dijkstra(analyzer["connectionsod"], airport1["value"])
    path = djk.distTo(estbusqueda, airport2["value"])
    camino = djk.pathTo(estbusqueda, airport2["value"])
    rutaair = lt.newList()
    for airport in lt.iterator(camino):
        lt.addLast(rutaair, airport)

    return distancesal, distancelleg, path, rutaair


def searchPath(analyzer, millas):
    routes = analyzer["connectionstd"]
    kms = millas * 1.6
    tot_msts = PrimMST(routes)
    rutas = DepthFirstSearch(routes, "LIS")
    camino = prim.prim

def closedAirport(analyzer, iata):
    lista = lt.newList(cmpfunction=compareKeys)
    vecinosod = gr.adjacents(analyzer["connectionsod"], iata)
    for i in lt.iterator(vecinosod):
        info = mp.get(analyzer["airportsInfo"], i)
        lt.addLast(lista, info)
    return lista


def getCoords(city):
    lat = city["value"]["Latitude"]
    lon = city["value"]["Longitude"]
    return lat, lon

def haversine(lat1, lon1, lat2, lon2):

      R = 6372.8 # this is in miles.  For Earth radius in kilometers use 6372.8 km

      dLat = radians(lat2 - lat1)
      dLon = radians(lon2 - lon1)
      lat1 = radians(lat1)
      lat2 = radians(lat2)

      a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
      c = 2*asin(sqrt(a))

      return R * c