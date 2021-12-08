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
 """

from App.model import addRouteConnections
from DISClib.ADT.graph import numVertices
import config as cf
import model
import csv
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    analyzer = model.newAnalyzer()
    return analyzer
# Funciones para la carga de datos
def loadServices(analyzer, servicesfile, airportsfile, citiesfile):
    servicesfile = cf.data_dir + servicesfile
    airportsfile = cf.data_dir + airportsfile
    citiesfile = cf.data_dir + citiesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"), delimiter=",")
    input_file2 = csv.DictReader(open(airportsfile, encoding="utf-8"), delimiter=",")
    input_file3 = csv.DictReader(open(citiesfile, encoding="utf-8"), delimiter=",")
    for airport in input_file2:
        model.addAirportInfo(analyzer, airport)
    for city in input_file3:
        model.addCityInfo(analyzer, city)
    for service in input_file:
        model.addAirportConnection(analyzer, service)
    model.addRouteConnections(analyzer)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def totalStops(analyzer, graph):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer, graph)


def totalConnections(analyzer, graph):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer, graph)

def searchAdjacents(analyzer, graph, vertex):
    return model.searchAdjacents(analyzer, graph, vertex)

def totalAiports(analyzer):
    return model.totalAirports(analyzer)

def totalCities(analyzer):
    return model.totalCities(analyzer)

def getbyCities(analyzer, city):
    return model.getCities(analyzer, city)

def searchInter(analyzer):
    return model.searchInter(analyzer)

def findSCC(analyzer, iata1, iata2):
    return model.findSCC(analyzer, iata1, iata2)

def findShortest(analyzer, city1, city2):
    return model.findShortest(analyzer, city1, city2)