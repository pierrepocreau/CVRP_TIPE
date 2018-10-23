class Route:
    """ Sequence de client partant du dépot et arrivant au dépot """
    def __init__(self, depot, client):
        self.client = client
        self.longeur = 0
        self.depot = depot
        self.chargement = 0
        self.client.link_to_depot(self.depot, self)

        self.actualiser()

    def actualiser_chargement(self, c):
        # ATTENTION pas plus de 1000 appels
        if c.n != self.depot:
            return c.q + self.actualiser_chargement(c.n)         
        else:
            return c.q
    
    def actualiser_longeur(self, c):
        c.route = self #c connait ça route
        if c.n != self.depot:
            return c.dn() + self.actualiser_longeur(c.n)
        else:
            return c.dn()
    
    #Je viens d'ajouter ça, pas reellement nécesaire
    def actualiser_clients(self, c):
        c.route = self
        if c.n != self.depot:
            self.actualiser_clients(c.n)
        
    
    def actualiser(self):
        self.actualiser_clients(self.depot)
        self.chargement = self.actualiser_chargement(self.depot)
        self.longeur = self.actualiser_longeur(self.depot)