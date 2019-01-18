from data_processing import data_processing
from route import Route
import matplotlib.pyplot as plt
import pickle
import copy

class Solver:
    def __init__(self, data, charge_vehicule):
        self.data = data
        self.charge_vehicule = charge_vehicule
        self.depot = self.data[0]
        self.routes = [Route(copy.deepcopy(self.depot), client) for client in self.data[1:]] #Chaque route est caractérisé par 1 depot (c'est le même dépot)
        self.temps_economise = []
        self.nb_clients = len(self.data)
    
    def chargement_disp(self, route):
        # q libre dans le camion pour cette route
        return self.charge_vehicule - route.chargement
    
    def cout_solution(self):
        return sum([r.actualiser_longeur(r.depot) for r in self.routes])
    
    #pas nécessaire
    def del_routes_vide(self):
        routes_vide = []
        for r in self.routes:
            if r.depot.n == r.depot:
                routes_vide.append(r)
        
        for r in routes_vide:
            self.routes.remove(r)
    
    ###CONSTRUCTION PREMIERE SOLUTION###

    def merge_routes(self, c1, c2):
        # fusionne la route du client1 et du client2
        if c1.route.chargement + c2.route.chargement <= self.charge_vehicule:
            c1.n, c2.p = c2, c1
            
            last_c2_route = c2.route.depot.p
            last_c2_route.n = c1.route.depot
            c1.route.depot.p = last_c2_route

            self.routes.remove(c2.route)
            c1.route.actualiser()
                   
    def contrainte_fusion(self, c1, c2):
        # Pour lier deux clients il faut qu'ils soient en bout de tournée
        if c1.route != c2.route and c1.n == c1.route.depot and c2.p == c2.route.depot:
            self.merge_routes(c1, c2)

    def calcule_temps_eco(self):
        # Calcule le temps economisé en liant 2 clients
        for c1 in self.data[1:]:
            for c2 in self.data[1:]:
                temps_eco = c1.dn() + c2.p.dn() - c1.d(c2) # JE SUIS SÛR QUE C'EST çA ???
                self.temps_economise.append(([c1, c2], temps_eco))
        self.temps_economise = sorted(self.temps_economise, key = lambda x: x[1], reverse = True)
    
    ###LOCAL SEARCH###

    def swap_tail(self, c1, c2, gain, verbose = False):
        #pas implemente encore
        coutp = self.cout_solution()

        c1.route.depot.p.n, c2.route.depot.p.n = c2.route.depot, c1.route.depot
        c1.route.depot.p, c2.route.depot.p = c2.route.depot.p, c1.route.depot.p

        c1.p.n, c2.p.n = c2, c1
        c1.p, c2.p = c2.p, c1.p

        c1.route, c2.route = c2.route, c1.route

        c1.route.actualiser()
        c2.route.actualiser()

        coutf = self.cout_solution()
        #if verbose: print("swap tail", (c1.id + 1, c2.id + 1), "gain th: ", gain, "vrai gain: ", coutp - coutf)
        

    def swap(self, c1, c2, gain, verbose = False):
        #echange c1 et c2

        c1.n, c2.n = c2.n, c1.n
        c1.p, c2.p = c2.p, c1.p
        
        c1.p.n, c1.n.p = c1, c1
        c2.p.n, c2.n.p = c2, c2

        c1.route, c2.route = c2.route, c1.route

        c1.route.actualiser()
        c2.route.actualiser()


        #if verbose: print("swap:", (c1.id+1, c2.id+1), "gain:", gain)
        self.del_routes_vide()
    
    def relocate(self, c1, c2, gain, verbose = False):
        #place c1 apres c2

        c1.p.n = c1.n
        c1.n.p = c1.p

        c2.n.p = c1
        c1.n = c2.n
        c1.p = c2
        c2.n = c1

        c1.n.route.actualiser()

        #if verbose: print("relocate ",(c1.id + 1, c2.id + 1), "gain:", gain)
        self.del_routes_vide()

    def invert(self, c1, c2, gain, verbose = False):
        #inverse c1 et c2 (sur la même route)
        c1.n, c2.p = c2.n, c1.p
        c1.p, c2.n = c2, c1

        c1.p.n, c1.n.p = c1, c1
        c2.p.n, c2.n.p = c2, c2

        c1.route.actualiser()

        #if verbose: print("invert:", (c1.id+1, c2.id+1), "gain:", gain)
        self.del_routes_vide()


    def contrainte_chargemnt(self, operation, c1, c2):
        #On verifie que effectue l'operation sur c1 et c2 ne viole pas la contraine de chargement du véhicule
        if operation == "reloc":
            diff_route_c2 = self.chargement_disp(c2.route) - c1.q
            return diff_route_c2 > 0

        elif operation == "swap":
            diff_route_c1 = self.chargement_disp(c1.route) - c2.q + c1.q
            diff_route_c2 = self.chargement_disp(c2.route) - c1.q + c2.q
            return diff_route_c1 > 0 and diff_route_c2 > 0

        elif operation == "tail_swap":
            c2_tail_chargement = c2.route.actualiser_chargement(c2)
            c1_tail_chargement = c1.route.actualiser_chargement(c1)
            diff_route_c1 = self.chargement_disp(c1.route) - c2_tail_chargement + c1_tail_chargement
            diff_route_c2 = self.chargement_disp(c2.route) - c1_tail_chargement + c2_tail_chargement
            return diff_route_c1 > 0 and diff_route_c2 > 0
    
    def operation_condition(self, operation, c1, c2):
        #Calcul le gain de l'operation si on peut l'effectuer sans violer les contraintes
        if operation == "reloc":
            if self.contrainte_chargemnt("reloc", c1, c2) and c1.n != c2 and c2.n != c1:
                return c1.p.dn() + c1.dn() + c2.dn() - c1.d(c2.n) - c2.d(c1) - c1.p.d(c1.n) #gain

        elif operation == "swap":
            if self.contrainte_chargemnt("swap", c1, c2) and c1.n != c2 and c2.n != c1:
                return c1.p.dn() + c1.dn() + c2.dn() + c2.p.dn() - c1.d(c2.n) - c2.p.d(c1) - c2.d(c1.n) - c1.p.d(c2) #gain
        
        elif operation == "tail_swap":
            if self.contrainte_chargemnt("tail_swap", c1, c2) and c1.route != c2.route and (c1.p != c1.route.depot or c2.p != c2.route.depot):
                return c1.p.dn() + c2.p.dn() - c2.p.d(c1) - c1.p.d(c2) #gain
        
        elif operation == "invert":
            if c1.n == c2:
                return c1.p.dn() + c2.dn() + c1.d(c2) - c2.d(c1) - c1.p.d(c2) - c1.d(c2.n)

        return -1
        
    ###AFFICHAGE###
        
    def show(self, figure_number):
        plt.figure(figure_number)
        c_x = [c.lng for c in self.data]
        c_y = [c.lat for c in self.data]
        plt.scatter(c_x, c_y, c = "r")
        for i in range(len(c_x)):
            plt.annotate(str(i+1), (c_x[i], c_y[i]))
        for r in self.routes:
            c = r.depot
            r_x = [c.lng]
            r_y = [c.lat]
            while c.n != r.depot:
                c = c.n
                r_x.append(c.lng)
                r_y.append(c.lat)
            r_x.append(r_x[0])
            r_y.append(r_y[0])
            plt.plot(r_x, r_y)