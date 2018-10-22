import requests
import geocoder
import csv
import time
import random
import pickle
from route import Route
from client import Client
from depot import Depot

def data_processing(adresse_file):
    liste_client = []
    liste_coords = []
    liste_adresses = []
    lat = []
    lng = []

    # converti les adresses en coordonnées et calcule la matrice des temps de trajets
    with open(adresse_file, 'r') as f:
        adresses = csv.reader(f) 
        for adresse in adresses:
            liste_adresses.append(adresse)
            g = geocoder.osm(adresse[0], headers = {'referer' : "CVRP_TI"}, timeout = 60)
            coords = g.json
            print(adresse)
            x = coords["lng"]
            y = coords["lat"]
            lat.append(y)
            lng.append(x)
            liste_coords.append(str(x) + "," + str(y))
            time.sleep(1) # maximum d'1 requete par seconde d'après les termes d'usage d'osm

    r = requests.get("http://127.0.0.1:5000/table/v1/driving/" + ";".join(liste_coords))
    data = r.json()
    
    # creer le dépot le premier élement de la liste d'adresses
    liste_client.append(Depot(liste_adresses[0], 0, lat[0], lng[0], data["durations"][0]))

    # creer les clients
    for i in range(1, len(liste_adresses)):
        adresse = liste_adresses[i]
        matrice_temps = data["durations"][i]
        chargement = random.randint(10, 30) #faire ça plus tard
        liste_client.append(Client(adresse, i, lat[i], lng[i], matrice_temps, chargement))
        # forme les premieres routes [depots --> client --> depot]
        #liste_client[i].route = Route(i, [liste_client[0], liste_client[i], liste_client[0]])
        #liste_client[i].route.actualiser()
    
    return liste_client

if __name__ == "__main__":
   data = data_processing("adresse.csv")
   pickle.dump(data, open("data.p", "wb"))