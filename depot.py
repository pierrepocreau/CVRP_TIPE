class Depot:
    """ Depot = origine des livraisons """
    def __init__(self, adresse, id, lat, lng, matrice_temps):
        self.adresse = adresse
        self.id = id
        self.lat = lat
        self.lng = lng
        self.matrice_temps = matrice_temps
        self.q = 0
        self.n = []
        self.p = []

    def d(self, c):
        return self.matrice_temps[c.id]
    
    def dn(self):
        return self.d(self.n)
