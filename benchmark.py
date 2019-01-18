import xml.etree.ElementTree as ET
import os
from data_processing import *
from resolution import resolution
from itertools import permutations

###Resout une instance d'augerat A (ou toutes)###

def distance(c1, c2):
    return ((c1.lat - c2.lat)**2 + (c1.lng - c2.lng)**2)**(1/2)

def get_data(file):
    tree = ET.parse(file)
    root = tree.getroot()
    liste_clients = []
    client_id = 0
    
    #rajoute cout de la solution optimale qui n'existe pas dans le fichier xml d'origine
    opti = float(root[0][-1].text)

    for client in root.iter("node"):
        #coordonnees des clients
        c_x = float(client[0].text)
        c_y = float(client[1].text)

        if client.attrib["type"] == "0":
            liste_clients.append(Depot("", 0, c_y, c_x, []))
        else:
            liste_clients.append(Client("", client_id, c_y, c_x, [], 0))
        client_id +=1
    
    for request in root.iter("request"):
        #requete de chargement
        client_id = int(request.attrib["id"])
        chargement = float(request[0].text)
        liste_clients[client_id].q = chargement
    
    for client1 in liste_clients:
        #calcul de la matrice de temps
        matrice_temps = []
        for client2 in liste_clients:
            matrice_temps.append(distance(client1, client2))
        client1.matrice_temps = matrice_temps
    
    return liste_clients, opti

def benchmark(afficher = False, localsearch = False, verbose = False):
    #test tout les instances augerat a

    solutions = {}
    problemes = []

    for f in os.listdir(dossier_donnees):

        data, opti = get_data(f)
        cout, routes = resolution(data, afficher, localsearch, verbose)
        diff_percent = (abs(cout - opti) / opti )* 100
        solutions[f] = (opti, cout, diff_percent)
        if verbose: print(f, len(routes), opti, cout, diff_percent)

    moyenne_perc = sum([value[-1] for key, value in solutions.items()]) / len(solutions)
    average_deviation = sum([abs(value[-1] - moyenne_perc) for key, value in solutions.items()]) / len(solutions) #je suis pas sur de ça..

    return solutions, moyenne_perc, average_deviation

def instance(instance, afficher = False, localsearch = False, verbose = False):
    #test une seule instance
    file = os.path.join(os.getcwd(), instance)
    data, opti = get_data(file)
    cout, route = resolution(data, afficher, localsearch, verbose)
    diff = (abs(cout - opti)/ opti) * 100
    return route, diff

if __name__ == "__main__":
    doc = os.getcwd()
    dossier_donnees = os.path.join(doc, "augerat-1995-set-a")
    os.chdir(dossier_donnees)
    #solutions = instance("A-n60-k09.xml", afficher = True, localsearch = False, verbose = False)
    solutions, moyenne, average_deviation = benchmark(afficher = False, localsearch = True, verbose = True)
    print(moyenne)
    print(average_deviation)