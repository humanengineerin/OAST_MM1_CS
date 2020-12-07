import Zdarzenie


class ListaZdarzen:

    def __init__(self, lista_zdarzen):
        self.lista_zdarzen = lista_zdarzen


    def put(self, typ, t_przyjscia, t_obslugi, t_nastepne):
        temp = Zdarzenie.Zdarzenie(typ = typ,
                                   t_przyjscia = t_przyjscia,
                                   t_obslugi = t_obslugi,
                                   t_nastepne = t_nastepne,
                                   )
        self.lista_zdarzen.append(temp)

    def get(self):
        temp = self.lista_zdarzen[0]
        self.lista_zdarzen.pop(0)
        return temp

    @staticmethod
    def sortuj_liste(lista):
        lista.sort(key=lambda zdarzenie: zdarzenie.t_przyjscia)