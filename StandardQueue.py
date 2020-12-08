import ListaZdarzen
import numpy as np

############################## -- Metody generujace losowe czasy

def gen_t_obslugi(mi):

    return -np.log(1-np.random.random())/mi


def gen_t_przyjscia(lam):

    return -np.log(1-np.random.random())/lam


def obl_sr_licz_kl_w_buf(lista_czasow, zdarzen_w_czasie, czas_symulacji):
    suma = 0

    for i in range(1000, len(zdarzen_w_czasie)-1):
        suma += ((lista_czasow[i+1] - lista_czasow[i]) * zdarzen_w_czasie[i])

    return suma/czas_symulacji


def obl_sr_licz_kl_w_sys(lista_czasow, zdarzen_w_czasie, obsluga_real, czas_symulacji):

    wynik = obl_sr_licz_kl_w_buf(lista_czasow, zdarzen_w_czasie, czas_symulacji) + obsluga_real/czas_symulacji

    return wynik


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

lam = 1
mi = 4
ro = lam/mi

max_czas_symulacji = 10000
max_zdarzen = 1000

acs = 0.0                                   # aktualny czas symulacji

obsluzonych_zdarzen = 0                     # liczba obsluzonych zdarzen (Real)
czas_p_zero = 0                             # suma czasu trwania stanu p0
czas_obslugi_real = 0                       # czas obslugi klientow REAL (do klientow w systemie)
zdarzen_w_kolejce = 0                       # liczba zdarzen w kolejce

czasy_przyjscia = []                        # czasy przyjścia do obsługi (Real)
czasy_rozpoczecia = []                      # czasy rozpoczęcia obsługi (Real)

tz = ["PRZYJSCIE_REAL", "PRZYJSCIE_IMAG"]

lista_zdarzen = list()
lista = ListaZdarzen.ListaZdarzen(lista_zdarzen)    # Obiekt listy zdarzen

lista_czasow = list()             #test
ile_zdarzen = list()                # test

# Inicjalizuje listę pierwszym zdarzeniem

lista.put(tz[0], 0, gen_t_obslugi(mi), gen_t_przyjscia(lam))

# zapisuje kiedy przyjdzie kolejny klient
odst_mdz_zgl = lista_zdarzen[-1].t_nastepne

print("Kolejka MM1 - Standardowa")
print()
print("mi = " + str(mi))
print("lam = " + str(lam))
print("max czas symulacji = " + str(max_czas_symulacji))
print("Rozpoczynam symulację... \n")

#while obsluzonych_zdarzen <= max_zdarzen:
while acs <= max_czas_symulacji:

    if lista_zdarzen[-1].t_przyjscia < max_czas_symulacji:
        lista.put(tz[0], odst_mdz_zgl, gen_t_obslugi(mi), gen_t_przyjscia(lam))

    odst_mdz_zgl = lista_zdarzen[-1].t_nastepne + lista_zdarzen[-1].t_przyjscia
    lista.sortuj_liste(lista_zdarzen)
    zdarzen_w_kolejce = 0

    for i in range (len(lista_zdarzen)):
        if lista_zdarzen[i].t_przyjscia < acs:
            zdarzen_w_kolejce += 1

    lista_czasow.append(acs)
    ile_zdarzen.append(zdarzen_w_kolejce)       # test

    if acs >= lista_zdarzen[0].t_przyjscia:

        zdarzenie = lista.get()         # Obsługuje zdarzenie, usuwam z listy zdarzeń
        zdarzen_w_kolejce -= 1          # Czy potrzebne?
        obsluzonych_zdarzen += 1

        czas_obslugi_real += zdarzenie.t_obslugi

        czasy_przyjscia.append(zdarzenie.t_przyjscia)
        czasy_rozpoczecia.append(acs)

        acs += zdarzenie.t_obslugi      # Aktualny czas zwiększam o czas obsługi zdarzenia

        # print("Aktualny czas (rozp. obslugi): " + str(acs))
        # print("Czas przyjscia: " + str(zdarzenie.t_przyjscia))
        # print("Czas do następnego zdarzenia: " + str(zdarzenie.t_nastepne))
        # print("Czas obsługi: " + str(zdarzenie.t_obslugi))
        # print()

    else:
        lista.sortuj_liste(lista_zdarzen)
        czas_p_zero += lista_zdarzen[0].t_przyjscia - acs   # licze czas trwania stanu p0
        acs = lista_zdarzen[0].t_przyjscia                  # aktualny czas ustawiam = czas przyjscia nastepnego zdarzenia


    #     print("NIE OBSLUGUJE ZDARZENIA!!!")
    #
    # print("Na liście znajduje się: " + str(zdarzen_w_kolejce) + " zdarzenia")
    #
    # print("Czas po obsłudze: " + str(acs))



print("-" * 40)
print()
print("Sredni czas oczekiwania na obsluge Wq = " + str(obl_sr_czas_ocz_na_obs(czasy_przyjscia, czasy_rozpoczecia, obsluzonych_zdarzen))             + "\t[Teoretycznie: Wq = " + str(ro ** 2 / (lam * (1 - ro))) + " ]")
print("Sredni czas przejscia przez system W = " + str(obl_sr_czas_przej_przez_sys(czasy_przyjscia, czasy_rozpoczecia, obsluzonych_zdarzen, mi))     + "\t[Teoretycznie: W = " + str(ro / (lam * (1 - ro))) + " ]")
print("Srednia liczba klientow w kolejce Lq (t_2):" + str(obl_sr_licz_kl_w_buf(lista_czasow, ile_zdarzen, acs))                                  + "\t[Teoretycznie: Lq = " + str(ro ** 2 / (1 - ro)) + " ]")
print("Srednia liczba klientow w systemie L (t): " + str(obl_sr_licz_kl_w_sys(lista_czasow, ile_zdarzen, czas_obslugi_real, acs))                + "\t[Teoretycznie: L = " + str(ro / (1 - ro)) + " ]")
print("p0 = " + str(czas_p_zero/acs))
print()
print("-" * 40)

# Zapis do pliku
do_pliku = open("MM1_Standard_Wyniki.txt", 'a')

do_pliku.write("-" * 10 + " DANE SYMULACJI " + "-" * 10 + "\n\n")
do_pliku.write("mi = " + str(mi) + "\n")
do_pliku.write("lam = " + str(lam) + "\n")
do_pliku.write("max czas symulacji = " + str(max_czas_symulacji) + "\n")

do_pliku.write("-" * 10 + " WYNIKI SYMULACJI - MM1 STANDARD QUEUE " + "-" * 10 + "\n\n")
do_pliku.write("Sredni czas oczekiwania na obsluge Wq = " + str(obl_sr_czas_ocz_na_obs(czasy_przyjscia, czasy_rozpoczecia, obsluzonych_zdarzen))             + "\t[Teoretycznie: Wq = " + str(ro ** 2 / (lam * (1 - ro))) + " ]\n")
do_pliku.write("Sredni czas przejscia przez system W = " + str(obl_sr_czas_przej_przez_sys(czasy_przyjscia, czasy_rozpoczecia, obsluzonych_zdarzen, mi))     + "\t[Teoretycznie: W = " + str(ro / (lam * (1 - ro))) + " ]\n")
do_pliku.write("Srednia liczba klientow w kolejce Lq (t_2):" + str(obl_sr_licz_kl_w_buf(lista_czasow, ile_zdarzen, acs))                                  + "\t[Teoretycznie: Lq = " + str(ro ** 2 / (1 - ro)) + " ]\n")
do_pliku.write("Srednia liczba klientow w systemie L (t): " + str(obl_sr_licz_kl_w_sys(lista_czasow, ile_zdarzen, czas_obslugi_real, acs))                + "\t[Teoretycznie: L = " + str(ro / (1 - ro)) + " ]\n")
do_pliku.write("p0 = " + str(czas_p_zero/acs) + "\n\n")



