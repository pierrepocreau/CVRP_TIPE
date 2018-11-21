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
    
    #n'existe pas dans le fichier xml d'origine
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

def determination_ordre_operations():
    op =  ["a", "b", "c", "d"]
    min_moyenne = 10000
    ordre_op = ["a", "b", "c", "d"]
    for i in permutations(op):
        _, moyenne = full_benchmark(i, afficher = False, localsearch = True, verbose = False)
        #_, moyenne = solo_instance(op, "A-n48-k07.xml", afficher = False, localsearch = True, verbose = False)
        print(moyenne, i)
        if moyenne < min_moyenne:
            min_moyenne = moyenne
            ordre_op = i
    return ordre_op, min_moyenne

def full_benchmark(ordre_op, afficher = False, localsearch = False, verbose = False):
    #test tout les instances augerat a

    solutions = {}
    problemes = []

    for f in os.listdir(dossier_donnees):

        data, opti = get_data(f)
        cout, routes = resolution(ordre_op, data, afficher, localsearch, verbose)
        diff_percent = (abs(cout - opti) / opti )* 100
        solutions[f] = (opti, cout, diff_percent)
        print(f, len(routes), opti, cout, diff_percent)
        #    resolution(ordre_op, data, True, True, True)
    moyenne_perc = sum([value[-1] for key, value in solutions.items()]) / len(solutions)

    return solutions, moyenne_perc

def solo_instance(ordre_op, instance, afficher = False, localsearch = False, verbose = False):
    #test une seule instance
    file = os.path.join(os.getcwd(), instance)
    data, opti = get_data(file)
    cout, route = resolution(ordre_op, data, afficher, localsearch, verbose)
    diff = (abs(cout - opti)/ opti) * 100
    return route, diff

if __name__ == "__main__":
    doc = os.getcwd()
    dossier_donnees = os.path.join(doc, "augerat-1995-set-a")
    os.chdir(dossier_donnees)
    ordre_op = ["c", "d", "b", "a"] #semble être le mieux
    solutions = solo_instance(ordre_op, "A-n60-k09.xml", afficher = True, localsearch = True, verbose = False)
    solutions, moyenne = full_benchmark(ordre_op, afficher = False, localsearch = False, verbose = False)
    for key, values in solutions.items():
        pass
        #print("opti: ", values[0], "solution: ", values[1], "diff: ", values[-1])
    print(moyenne)
    #op, min_m = determination_ordre_operations()
    #print(op, min_m)