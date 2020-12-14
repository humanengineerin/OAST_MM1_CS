from TestStandardQueue import StandardQueue
from TestContinuousService import ContinuousService


if __name__ == "__main__":

    # Parametry początkowe symulacji
    MAX_CZAS_SYMULACJI = 6000
    while True:
        lam = int(input("\nProszę wprowadzić wartość lambda wybierając z {1,2,3}: "))
        if lam in [1, 2, 3]:
            break
        else:
            print("Wybrano nieprawidłową wartość lambda. Proszę spróbować ponownie.\n")
    mi = 4
    ro = lam / mi
    acs = 0.0
    obsluzonych_zdarzen = 0  # liczba obsluzonych zdarzen (Real)
    czas_obslugi_imag = 0  # czas obslugi klientow IMAG (do prawdopodobienstwa)
    czas_obslugi_real = 0  # czas obslugi klientow REAL (do klientow w systemie)
    zdarzen_w_kolejce = 0
    czasy_przyjscia = []
    czasy_rozpoczecia = []
    odst_mdz_zgl = 0
    czas_p_zero = 0

    # Instancje obiektów kolejek
    standard = StandardQueue(
        lam=lam,
        mi=mi,
        ro=ro,
        acs=acs,
        obsluzonych_zdarzen=obsluzonych_zdarzen,
        czas_p_zero=czas_p_zero,
        czas_obslugi_real=czas_obslugi_real,
        max_czas_symulacji=MAX_CZAS_SYMULACJI,
        zdarzen_w_kolejce=zdarzen_w_kolejce,
        czasy_przyjscia=czasy_przyjscia,
        czasy_rozpoczecia=czasy_rozpoczecia,
        odst_mdz_zgl=odst_mdz_zgl
    )

    continuous_service = ContinuousService(
        lam=lam,
        mi=mi,
        ro=ro,
        acs=acs,
        obsluzonych_zdarzen=obsluzonych_zdarzen,
        czas_obslugi_imag=czas_obslugi_imag,
        max_czas_symulacji=MAX_CZAS_SYMULACJI,
        czas_obslugi_real=czas_obslugi_real,
        zdarzen_w_kolejce=zdarzen_w_kolejce,
        czasy_przyjscia=czasy_przyjscia,
        czasy_rozpoczecia=czasy_rozpoczecia,
        odst_mdz_zgl=odst_mdz_zgl
    )

    # Uruchomienie symulacji
    while True:
        kolejka = input("\nProszę wybrać rodzaj kolejki do symulacji, wpisując odpowiednią cyfrę, gdzie:\n"
                        "   1) Standardowa kolejka M/M/1  2) Kolejka M/M/1 Continuous Service: ")
        if kolejka == "1":
            wynik_standard = standard.uruchom_MM1()
            break
        if kolejka == "2":
            wynik_continuous = continuous_service.uruchom_MM1CS()
        else:
            print("Wprowadzono nieprawidłowy numer wyboru kolejki. Proszę spróbować ponownie.\n")
