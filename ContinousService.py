import ListaZdarzen
import numpy as np

############################## -- Metody generujace losowe czasy

def gen_t_obslugi(mi):

    return -np.log(1-np.random.random())/mi


def gen_t_przyjscia(lam):

    return -np.log(1-np.random.random())/lam


def obl_sr_licz_kl_w_buf():
    x=1 # TODO


def obl_sr_licz_kl_w_sys():
    x=1 # TODO


def obl_sr_czas_ocz_na_obs(czasy_przyjscia, czasy_rozpoczecia, zdarzen):
    suma = 0
    for i in range(zdarzen):
        suma += (czasy_rozpoczecia[i] - czasy_przyjscia[i])


    return suma / zdarzen

def obl_sr_czas_przej_przez_sys(czasy_przyjscia, czasy_rozpoczecia, zdarzen, mi):
    suma = 0

    for i in range(zdarzen):
        suma += (czasy_rozpoczecia[i] - czasy_przyjscia[i] + 1/mi)

    return suma / zdarzen

####################################### Inicjalizacja zmiennych

lam = 3
mi = 4

max_czas_symulacji = 10000
max_zdarze = 1000

acs = 0.0                                   # aktualny czas symulacji

obsluzonych_zdarzen = 0                     # liczba obsluzonych zdarzen (Real)
czas_obslugi_imag = 0                       # czas obslugi klientow IMAG (do prawdopodobienstwa)
zdarzen_w_kolejce = 0                       # liczba zdarzen w kolejcee

czasy_przyjscia = []                        # czasy przyjścia do obsługi (Real)
czasy_rozpoczecia = []                      # czasy rozpoczęcia obsługi (Real)

suma_zdarzen = 0                            # obl. sr. w kolejce (test)
count = 0                                   # obl. sr. w kolejce (test)

tz = ["PRZYJSCIE_REAL", "PRZYJSCIE_IMAG"]

lista_zdarzen = list()
lista = ListaZdarzen.ListaZdarzen(lista_zdarzen)    # Obiekt listy zdarzen

# Inicjalizuje listę pierwszym zdarzeniem

lista.put(tz[0], 0, gen_t_obslugi(mi), gen_t_przyjscia(lam))

# zapisuje kiedy przyjdzie kolejny klient
odst_mdz_zgl = lista_zdarzen[-1].t_nastepne

print("Rozpoczynam symulację... Kolejka MM1 - Continouous Service")
print()
print("mi = " + str(mi))
print("lam = " + str(lam))
print("max czas symulacji = " + str(max_czas_symulacji))
print()

#while obsluzonych_zdarzen <= max_zdarzen:
while acs <= max_czas_symulacji:

    if lista_zdarzen[-1].t_przyjscia < max_czas_symulacji:
        lista.put(tz[0], odst_mdz_zgl, gen_t_obslugi(mi), gen_t_przyjscia(lam))

    odst_mdz_zgl = lista_zdarzen[-1].t_nastepne + lista_zdarzen[-1].t_przyjscia
    lista.sortuj_liste(lista_zdarzen)
    zdarzen_w_kolejce = 0

    for i in range (len(lista_zdarzen)):
        if lista_zdarzen[i].t_przyjscia <= acs:
            zdarzen_w_kolejce += 1

    # Testowo - do obliczenia sr. klien. w kolejce
    suma_zdarzen += zdarzen_w_kolejce
    count += 1

    if zdarzen_w_kolejce > 0 and acs >= lista_zdarzen[0].t_przyjscia:

        zdarzenie = lista.get()         # Obsługuje zdarzenie, usuwam z listy zdarzeń
        zdarzen_w_kolejce -= 1          # Czy potrzebne?
        obsluzonych_zdarzen += 1

        czasy_przyjscia.append(zdarzenie.t_przyjscia)
        czasy_rozpoczecia.append(acs)

        acs += zdarzenie.t_obslugi      # Aktualny czas zwiększam o czas obsługi zdarzenia

        # print("Aktualny czas (rozp. obslugi): " + str(acs))
        # print("Czas przyjscia: " + str(zdarzenie.t_przyjscia))
        # print("Czas do następnego zdarzenia: " + str(zdarzenie.t_nastepne))
        # print("Czas obsługi: " + str(zdarzenie.t_obslugi))
        # print()
    else:
        lista.put(tz[1], acs, gen_t_obslugi(mi), gen_t_przyjscia(lam))
        lista.sortuj_liste(lista_zdarzen)
        acs = lista_zdarzen[0].t_przyjscia

        zdarzenie = lista.get()

        czas_obslugi_imag += zdarzenie.t_obslugi
        acs += zdarzenie.t_obslugi

    #     print("OBSLUGUJE IMAGIARY!!!")
    #
    # print("Na liście znajduje się: " + str(zdarzen_w_kolejce) + " zdarzenia")
    #
    # print("Czas po obsłudze: " + str(acs))

print("-" * 40)
print()
print("Sredni czas oczekiwania na obsluge Wq = " + str(obl_sr_czas_ocz_na_obs(czasy_przyjscia, czasy_rozpoczecia, obsluzonych_zdarzen)))
print("Sredni czas przejscia przez system W = " + str(obl_sr_czas_przej_przez_sys(czasy_przyjscia, czasy_rozpoczecia, obsluzonych_zdarzen, mi)))
print("Srednia liczba zdarzen w kolejce (test):" + str(suma_zdarzen/count))
print("Pr-biestwo, że serwer jest zajęty obsługą IMAGINARY (wzgl. czasu symulacji): " + str(czas_obslugi_imag/acs))

print()
print("-" * 40)

