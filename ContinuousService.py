import numpy as np

import ListaZdarzen


class ContinuousService:
    def __init__(self, lam, mi, ro, acs, obsluzonych_zdarzen, czas_obslugi_imag, czas_obslugi_real, zdarzen_w_kolejce,
                 max_czas_symulacji, czasy_przyjscia, czasy_rozpoczecia, odst_mdz_zgl
                 ):

        self.lam = lam
        self.mi = mi
        self.ro = ro
        self.acs = acs  # aktualny czas symulacji

        self.obsluzonych_zdarzen = obsluzonych_zdarzen  # liczba obsluzonych zdarzen (Real)
        self.czas_obslugi_imag = czas_obslugi_imag  # czas obslugi klientow IMAG (do prawdopodobienstwa)
        self.czas_obslugi_real = czas_obslugi_real  # czas obslugi klientow REAL (do klientow w systemie)
        self.zdarzen_w_kolejce = zdarzen_w_kolejce  # liczba zdarzen w kolejce

        self.max_czas_symulacji = max_czas_symulacji
        self.czasy_przyjscia = czasy_przyjscia  # czasy przyjścia do obsługi (Real)
        self.czasy_rozpoczecia = czasy_rozpoczecia  # czasy rozpoczęcia obsługi (Real)

        self.lista_zdarzen = list()
        self.lista = ListaZdarzen.ListaZdarzen(self.lista_zdarzen)  # Obiekt listy zdarzen

        self.lista_czasow = list()
        self.ile_zdarzen = list()

        self.odst_mdz_zgl = odst_mdz_zgl

########################################################
    # Metody generujace losowe czasy i liczące niezbędne parametry

    def gen_t_obslugi(self):
        return -np.log(1 - np.random.random()) / self.mi

    def gen_t_przyjscia(self):
        return -np.log(1 - np.random.random()) / self.lam

    def obl_sr_licz_kl_w_buf(self):
        suma = 0
        for i in range(len(self.ile_zdarzen) - 1):
            suma += ((self.lista_czasow[i + 1] - self.lista_czasow[i]) * self.ile_zdarzen[i])
        return suma / self.acs

    def obl_sr_licz_kl_w_sys(self):
        wynik = self.obl_sr_licz_kl_w_buf() + self.czas_obslugi_real / self.acs
        return wynik

    def obl_sr_czas_ocz_na_obs(self):
        suma = 0
        for i in range(self.obsluzonych_zdarzen):
            suma += (self.czasy_rozpoczecia[i] - self.czasy_przyjscia[i])
        return suma / self.obsluzonych_zdarzen

    def obl_sr_czas_przej_przez_sys(self):
        suma = 0
        for i in range(self.obsluzonych_zdarzen):
            suma += (self.czasy_rozpoczecia[i] - self.czasy_przyjscia[i] + 1 / self.mi)
        return suma / self.obsluzonych_zdarzen
########################################################

    def uruchom_MM1CS(self):

        print("\n\nKolejka M/M/1 - Continuous Service\n")
        print("\tmi = " + str(self.mi))
        print("\tlam = " + str(self.lam))
        print("\tro = " + str(self.lam / self.mi))
        print("\tmax czas symulacji = " + str(self.max_czas_symulacji))
        print("\nRozpoczynam symulację... \n")

        tz = ["PRZYJSCIE_REAL", "PRZYJSCIE_IMAG"]

        self.lista.put(tz[0], 0, self.gen_t_obslugi(), self.gen_t_przyjscia())
        self.odst_mdz_zgl = self.lista_zdarzen[-1].t_nastepne

        while not self._zakoncz_symulacje():

            if self.lista_zdarzen[-1].t_przyjscia < self.max_czas_symulacji:
                self.lista.put(tz[0], self.odst_mdz_zgl, self.gen_t_obslugi(), self.gen_t_przyjscia())

            self.odst_mdz_zgl = self.lista_zdarzen[-1].t_nastepne + self.lista_zdarzen[-1].t_przyjscia
            self.lista.sortuj_liste(self.lista_zdarzen)
            zdarzen_w_kolejce = 0

            for i in range(len(self.lista_zdarzen)):
                if self.lista_zdarzen[i].t_przyjscia < self.acs:
                    zdarzen_w_kolejce += 1

            self.lista_czasow.append(self.acs)
            self.ile_zdarzen.append(zdarzen_w_kolejce)  # test

            if self.acs >= self.lista_zdarzen[0].t_przyjscia:

                zdarzenie = self.lista.get()  # Obsługuje zdarzenie, usuwam z listy zdarzeń
                zdarzen_w_kolejce -= 1
                self.obsluzonych_zdarzen += 1

                self.czas_obslugi_real += zdarzenie.t_obslugi

                self.czasy_przyjscia.append(zdarzenie.t_przyjscia)
                self.czasy_rozpoczecia.append(self.acs)

                self.acs += zdarzenie.t_obslugi  # Aktualny czas zwiększam o czas obsługi zdarzenia
            else:
                self.lista.put(tz[1], self.acs, self.gen_t_obslugi(), self.gen_t_przyjscia())   # dla ostatniego punktu zadania
                self.lista.sortuj_liste(self.lista_zdarzen)                                     # w put(): t_obslugi = 1/mi
                self.acs = self.lista_zdarzen[0].t_przyjscia                                    # MM1_CS_Wyniki_v2.txt

                zdarzenie = self.lista.get()

                self.czas_obslugi_imag += zdarzenie.t_obslugi
                self.acs += zdarzenie.t_obslugi

        # Wyświetlenie wyników
        # E[W] = Wq; E[T] = W; E[Q] = Lq; E[N] = L
        print("-"*40 + "\n\nŚredni czas oczekiwania na obsługę E[W] = "
              + str(self.obl_sr_czas_ocz_na_obs())
              + "\t[Teoretycznie: Wq = " + str(self.ro / (self.lam * (1-self.ro))) + "]\n"

              + "Średni czas przejścia przez system E[T] = "
              + str(self.obl_sr_czas_przej_przez_sys())
              + "\t[Teoretycznie: W = " + str((2 - self.ro) * self.ro / (self.lam * (1 - self.ro))) + "]\n"

              + "Średnia liczba klientów w buforze  E[Q] = "
              + str(self.obl_sr_licz_kl_w_buf())
              + "\t[Teoretycznie: Lq = " + str(self.ro / (1 - self.ro)) + "]\n"

              + "Średnia liczba klientow w systemie E[N] = "
              + str(self.obl_sr_licz_kl_w_sys())
              + "\t[Teoretycznie: L = " + str((2 - self.ro) * self.ro / (1 - self.ro)) + "]\n"

              + "Prawdopodobieństwo, że serwer jest zajęty obsługą klienta typu IMAGINARY (wzgl. czasu symulacji) = "
              + str(self.czas_obslugi_imag/self.acs) + "\n\n" + "-"*40)

        # Zapis do pliku
        do_pliku = open("MM1_CS_Wyniki.txt", 'a')

        do_pliku.write("-" * 10 + " DANE SYMULACJI " + "-" * 10 + "\n\n"
                       + "\tmi = " + str(self.mi) + "\n"
                       + "\tlam = " + str(self.lam) + "\n"
                       + "\tro = " + str(self.lam / self.mi) + "\n"
                       + "\tmax czas symulacji = " + str(self.max_czas_symulacji) + "\n\n"

                       + "-" * 10 + " WYNIKI SYMULACJI - M/M/1 CONTINUOUS SERVICE " + "-" * 10 + "\n\n"
                       + "Średni czas oczekiwania na obsługę E[W] = "
                       + str(self.obl_sr_czas_ocz_na_obs())
                       + "\t[Teoretycznie: Wq = " + str(self.ro / (self.lam * (1-self.ro))) + " ]\n"

                       + "Średni czas przejścia przez system E[T] = "
                       + str(self.obl_sr_czas_przej_przez_sys())
                       + "\t[Teoretycznie: W = " + str((2 - self.ro) * self.ro / (self.lam * (1 - self.ro))) + " ]\n"

                       + "Średnia liczba klientow w buforze  E[Q] = "
                       + str(self.obl_sr_licz_kl_w_buf())
                       + "\t[Teoretycznie: Lq = " + str(self.ro / (1 - self.ro)) + " ]\n"

                       + "Średnia liczba klientów w systemie E[N] = "
                       + str(self.obl_sr_licz_kl_w_sys())
                       + "\t[Teoretycznie: L = " + str((2 - self.ro) * self.ro / (1 - self.ro)) + " ]\n"

                       + "Prawdopodobieństwo, że serwer jest zajęty obsługą klienta typu IMAGINARY (wzgl. czasu symulacji) = "
                       + str(self.czas_obslugi_imag/self.acs) + "\n\n\n")

    def _zakoncz_symulacje(self):
        przekroczenie = self.acs >= self.max_czas_symulacji
        if przekroczenie:
            print("Zakończono symulację ze względu na przekroczenie czasu.")
            return True
        else:
            return False
