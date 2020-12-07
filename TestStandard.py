import ListaZdarzen
import numpy as np

############################## -- Metody generujace losowe czasy

def gen_t_obslugi(mi):

    return -np.log(1-np.random.random())/mi


def gen_t_przyjscia(lam):

    return -np.log(1-np.random.random())/lam

def obl_sr_licz_kl_w_buf():
    x=1

def obl_sr_licz_kl_w_sys():
    x=1

def obl_sr_czas_ocz_na_obs(czasy_przyjscia, czasy_rozpoczecia, zdarzen):
    suma = 0
    for i in range(zdarzen):
        suma += (czasy_rozpoczecia[i] - czasy_przyjscia[i])

    wynik = suma / zdarzen

    return wynik

def obl_sr_czas_przej_przez_sys(czasy_przyjscia, czasy_rozpoczecia, zdarzen, mi):
    suma = 0

    for i in range(zdarzen):
        suma += (czasy_rozpoczecia[i] - czasy_przyjscia[i] + 1/mi)
    wynik = suma / zdarzen

    return wynik

####################################### Inicjalizacja zmiennych

lam = 3
mi = 4
ro = lam/mi

max_czas_symulacji = 3000

acs = 0.0                   # aktualny czas symulacji

obsluzonych_zdarzen = 0                    # liczba obsluzonych zdarzen (Real)
czasy_przyjscia = []                  # czasy przyjścia do obsługi (Real)
czasy_rozpoczecia = []                   # czasy rozpoczęcia obsługi (Real)

szwk_suma = 0
szwk_czas = 0


tz = ["PRZYJSCIE_REAL", "PRZYJSCIE_IMAG"]

lista_zdarzen = list()
lista = ListaZdarzen.ListaZdarzen(lista_zdarzen)    # Obiekt listy zdarzen

# Inicjalizuje listę pierwszym zdarzeniem

lista.put(tz[0], 0, gen_t_obslugi(mi), gen_t_przyjscia(lam))
odst_mdz_zgl = lista_zdarzen[-1].t_nastepne
zdarzen_w_kolejce = 1

while acs <= max_czas_symulacji:

    lista.put(tz[0], odst_mdz_zgl, gen_t_obslugi(mi), gen_t_przyjscia(lam))
    ile_zdarzen = 0
    odst_mdz_zgl = lista_zdarzen[-1].t_nastepne + lista_zdarzen[-1].t_przyjscia
    lista.sortuj_liste(lista_zdarzen)

    for i in range (len(lista_zdarzen)):
        if lista_zdarzen[i].t_przyjscia <= acs:
            ile_zdarzen += 1

    zdarzen_w_kolejce_old = zdarzen_w_kolejce
    zdarzen_w_kolejce = ile_zdarzen

    if zdarzen_w_kolejce != zdarzen_w_kolejce_old:
        szwk_suma += (acs - szwk_czas) * zdarzen_w_kolejce_old
        szwk_czas = acs


    if len(lista_zdarzen) > 0 and acs >= lista_zdarzen[0].t_przyjscia:

        zdarzenie = lista.get()
        zdarzen_w_kolejce -= 1
        czasy_przyjscia.append(zdarzenie.t_przyjscia)
        czasy_rozpoczecia.append(acs)
        obsluzonych_zdarzen += 1
        acs += zdarzenie.t_obslugi

        print("Aktualny czas (rozp. obslugi): " + str(acs))
        print("Czas przyjscia: " + str(zdarzenie.t_przyjscia))
        print("Czas do następnego zdarzenia: " + str(zdarzenie.t_nastepne))
        print("Czas obsługi: " + str(zdarzenie.t_obslugi))
        print()
    else:
        lista.sortuj_liste(lista_zdarzen)
        acs = lista_zdarzen[0].t_przyjscia
        print("NIE OBSLUGUJE ZDARZENIA!!!")

    print("Na liście znajduje się: " + str(zdarzen_w_kolejce) + " zdarzenia")

    print("Czas po obsłudze: " + str(acs))

print("-" * 40)
print()
print("Sredni czas oczekiwania na obsluge Wq = " + str(obl_sr_czas_ocz_na_obs(czasy_przyjscia, czasy_rozpoczecia, obsluzonych_zdarzen)))
print("Sredni czas przejscia przez system W = " + str(obl_sr_czas_przej_przez_sys(czasy_przyjscia, czasy_rozpoczecia, obsluzonych_zdarzen, mi)))
print(szwk_suma/acs)
print("-" * 40)
print()

# Niestety ale ten kod generuje dużo za dużo zdarzeń. Przydałoby się to usprawnić
for i in range(200):
    print(lista_zdarzen[i].t_przyjscia, end =", ")