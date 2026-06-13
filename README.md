# Kalkulator Macierzy - Instrukcja uruchomienia

Ten plik zawiera instrukcję krok po kroku, jak pobrać kod z GitHuba, zainstalować niezbędne biblioteki oraz uruchomić projekt w środowisku PyCharm.

## Krok 1: Utworzenie projektu lokalnego w PyCharm

1. Otwórz **PyCharm**.
2. Wybierz opcję **New Project** (Nowy Projekt).
3. Wskaż lokalizację dla nowego projektu na swoim dysku i kliknij **Create** (Utwórz).

## Krok 2: Inicjalizacja repozytorium i dodanie zdalnego repozytorium (remote)

1. Otwórz wbudowany terminal w PyCharm (zakładka **Terminal** na dole ekranu) lub użyj zewnętrznego terminala w folderze projektu.
2. Zanim przejdziesz dalej, sprawdź czy PyCharm automatycznie wygenerował plik domyślny `main.py`. Jeżeli powstał plik `main.py`, **usuń go**, aby uniknąć konfliktów podczas pobierania kodu.
3. Zainicjalizuj lokalne repozytorium Git za pomocą polecenia:
   ```bash
   git init
   ```
4. Dodaj zdalne repozytorium o nazwie `origin` (zastąp `<URL_REPOZYTORIUM>` adresem swojego repozytorium na GitHubie):
   ```bash
   git remote add origin <URL_REPOZYTORIUM>
   ```

## Krok 3: Pobranie kodu ze zdalnego repozytorium (Pull)

Pobierz aktualny kod z gałęzi master za pomocą komendy:
```bash
git pull origin master
```

## Krok 4: Instalacja wymaganych bibliotek

Aby zainstalować wszystkie wymagane biblioteki i zależności z pliku `requirements.txt`:
1. Upewnij się, że Twoje środowisko wirtualne (Virtual Environment / venv) jest aktywne. W PyCharm terminal zazwyczaj automatycznie aktywuje środowisko wirtualne (oznaczone jako `(venv)` przed znakiem zachęty terminala).
2. Uruchom poniższe polecenie w terminalu:
   ```bash
   pip install -r requirements.txt
   ```

## Krok 5: Uruchomienie programu

Po pomyślnej instalacji zależności możesz uruchomić program:
1. W terminalu wpisz:
   ```bash
   python main.py
   ```
2. Alternatywnie w PyCharm kliknij prawym przyciskiem myszy na plik `main.py` w drzewie projektu i wybierz **Run 'main'** (lub kliknij zieloną ikonę odtwarzania w prawym górnym rogu).
