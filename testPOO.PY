#coding: utf-8

class Voiture:
    def __init__(self):
        self.nom = "Maser"
        self._roues = 4
    def allumer(self):
        print("Vroom vroom")

    @property
    def roues(self):
        print("Récupération du nombre de roues")
        return self._roues
    @roues.setter
    def roues(self, v):
        print("Changement du nombre de roues")
        self._roues = v

# Héritage de classe:
class VoitureSport(Voiture):
    def __init__(self):
        self.nom = "Sport"
# La classe fille hérite de tous les attributs et méthodes de la classe parente
# On peut surcharger les méthodes en redéfinissant une méthode du père dans la classe fille
    def allumer(self):
        print("Vroom vroom de voiture de sport")
# --> Polymorphisme: chaque classe a la méthode mais elle n'effectue pas la même tâche
car = Voiture()
i = car.roues
car.roues = 2

print(dir(car))
print(car.nom)
# print(car.nondéfini) Cause une erreur qui empêche le programme de se lancer
