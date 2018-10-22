class Client:
    """ Client = 1 adresse à livrer"""
    def __init__(self, adresse, id, lat, lng, matrice_temps, q = 30):
        self.adresse = adresse
        self.lat = lat
        self.lng = lng
        self.id = id
        self.q = q
        self.matrice_temps = matrice_temps
        self.p = [] #prev client
        self.n = [] #next client
    
    def d(self, c2):
        return self.matrice_temps[c2.id]

    def dn(self):
        return self.d(self.n)
    
    def link_to_depot(self, depot, route):
        #Utile pour creation des routes
        self.route = route
        self.n, self.p = depot, depot
        depot.n, depot.p = self, self