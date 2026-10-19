# AGH Career Days 2026 · przygotowanie do warsztatu AI

Przygotuj laptop i sprawdź środowisko przed zajęciami. Zarezerwuj około 30 minut; instalacja Gita lub Pythona może potrwać dłużej.

**Zacznij od [instrukcji PDF](Przygotowanie_do_warsztatu.pdf).** Polecenia można z niej kopiować. Poniżej znajdziesz te same kroki w wersji do czytania na GitHubie.

## Co jest wymagane?

- Własny laptop i ładowarka.
- Git oraz Python **3.11 lub 3.12**.
- Wynik **`Local: PASSED`** w teście lokalnym.
- Wynik **`Notebook: PASSED`** w notebooku kontrolnym.

**Gemini API jest opcjonalne.** Jeśli masz własny dostęp do API bez włączania płatności, możesz sprawdzić również połączenie z modelem. Brak klucza lub problemy z dostępem do API nie wykluczają udziału. Na warsztacie dostępny będzie wariant lokalny (`AUTHORED_FIXTURE`), oparty na przygotowanym scenariuszu, bez połączenia z modelem.

W tym repozytorium znajdziesz **wyłącznie materiały przygotowawcze**. Właściwe ćwiczenie udostępnimy osobno. `Local: PASSED` potwierdza działanie tego pakietu i podstawowych bibliotek, nie całego ćwiczenia ani dostępności API w dniu zajęć.

## 1. Pobierz pliki

Zainstaluj [Gita](https://git-scm.com/downloads) oraz [Pythona](https://www.python.org/downloads/) w wersji 3.11 lub 3.12. Po instalacji otwórz nowe okno **PowerShella** na Windows lub **terminala** na macOS/Linux.

Wykonaj po jednym poleceniu:

```text
git clone https://github.com/ai-krk/agh-career-days-2026-prep.git agh-workshop
cd agh-workshop
```

Jeśli masz już aktualną kopię repo, otwórz jej folder zamiast klonować ponownie. Dalsze polecenia wykonuj z folderu z `check_gemini.py` i `requirements.txt`. **Nie ma tu podfolderu `lab`.** Nie kopiuj samego notebooka.

## 2. Utwórz środowisko i zainstaluj biblioteki

### Windows / PowerShell

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Masz Pythona 3.11? W dwóch pierwszych poleceniach zamień `-3.12` na `-3.11`.

Jeśli `py` nie działa, uruchom `python --version`. Gdy wskazuje 3.11 lub 3.12, możesz utworzyć środowisko poleceniem `python -m venv .venv`, a następnie wykonać powyższe polecenie instalacji bibliotek. Dla innej wersji zainstaluj 3.11 lub 3.12 i wybierz ją jawnie.

### macOS / Linux

```bash
python3 --version
```

Jeśli wynik wskazuje 3.11 lub 3.12:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```

Jeśli masz osobną instalację Pythona 3.12, użyj `python3.12 -m venv .venv` zamiast polecenia tworzącego środowisko przez `python3`.

**Po błędzie zatrzymaj się i rozwiąż problem przed kolejnym krokiem.** `pip install` nie instaluje Pythona. Nie musisz aktywować `.venv` ani zmieniać zabezpieczeń PowerShella: pełne ścieżki wskazują właściwe środowisko.

## 3. Sprawdź środowisko lokalne · WYMAGANE

Windows:

```powershell
.\.venv\Scripts\python.exe check_gemini.py --local-only
```

macOS / Linux:

```bash
./.venv/bin/python check_gemini.py --local-only
```

Oczekiwany wynik:

```text
Local: PASSED
Gemini: NOT_RUN
Code: local_only
```

**`Gemini: NOT_RUN` jest tu prawidłowe.** W tym trybie skrypt nie pyta o klucz, nie tworzy klienta API i nie wysyła żądania. Sprawdza wersję Pythona, biblioteki oraz plik notebooka kontrolnego. Instalacja bibliotek z poprzedniego kroku wymaga internetu; sam test lokalny nie łączy się z Gemini.

## 4. Uruchom notebook kontrolny · WYMAGANE

Windows:

```powershell
.\.venv\Scripts\python.exe -m jupyter lab
```

macOS / Linux:

```bash
./.venv/bin/python -m jupyter lab
```

Otwórz **`00_Sprawdz_srodowisko.ipynb`** i wykonaj obie komórki z kodem, po kolei, używając **Shift+Enter**. Oczekiwany końcowy wynik to **`Notebook: PASSED`**. Ten notebook działa wyłącznie lokalnie i nie zawiera ćwiczenia warsztatowego. Nie wpisuj do niego klucza.

Pozostaw otwarty terminal, z którego uruchomiono JupyterLab. Jeśli korzystasz z VS Code, zainstaluj rozszerzenia **Python** i **Jupyter**, otwórz folder repo i w **Select Kernel** wybierz Pythona ze środowiska `.venv` tego folderu. Notebook sprawdza właśnie to środowisko, nie dowolne `.venv`. Jeśli zgłosi błąd, postępuj zgodnie z komunikatem i uruchom obie komórki ponownie.

## 5. Sprawdź Gemini API · OPCJONALNE · LIVE_GEMINI

Możesz pominąć całą tę sekcję. Wyniki `Local: PASSED` i `Notebook: PASSED` wystarczą do udziału w wariancie lokalnym.

1. Zaloguj się na **własne konto Google** w [Google AI Studio](https://aistudio.google.com/).
2. Zapoznaj się z warunkami usługi i zasadami swojego projektu. W [API keys](https://aistudio.google.com/apikey) sprawdź klucz lub wybierz **Create API key** i własny projekt.
3. Sprawdź plan i limity. **Nie włączaj płatności ani nie dodawaj karty na potrzeby warsztatu.** Jeśli projekt jest płatny, API wymaga billingu lub zasady są niejasne, wybierz wariant lokalny.
4. Nie pożyczaj klucza. Traktuj go jak hasło: nie zapisuj w repozytorium, notebooku, mailu ani na zrzucie ekranu. Jeśli go ujawnisz, unieważnij go w AI Studio.

Dostęp do czatu Gemini lub oferty studenckiej nie potwierdza dostępu do **Gemini Developer API**. Free Tier zależy od dostępności i limitów projektu. Nie obchodź ograniczeń konta, regionu lub wieku. [Klucze API](https://ai.google.dev/gemini-api/docs/api-key) · [wymagania dostępu](https://ai.google.dev/gemini-api/docs/available-regions) · [cennik](https://ai.google.dev/gemini-api/docs/pricing) · [limity](https://ai.google.dev/gemini-api/docs/rate-limits).

W zwykłym terminalu, nie w notebooku, uruchom:

Windows:

```powershell
.\.venv\Scripts\python.exe check_gemini.py
```

macOS / Linux:

```bash
./.venv/bin/python check_gemini.py
```

Wpisz `TAK` tylko wtedy, gdy znasz i akceptujesz zasady własnego projektu. Następnie wklej klucz do ukrytego pola i naciśnij Enter. Brak znaków i gwiazdek jest normalny. Skrypt nie prosi o przesłanie klucza do zatwierdzenia.

Test wykonuje najwyżej **jedno żądanie**, bez automatycznego ponawiania, z limitem czasu żądania 30 sekund. Wysyła wyłącznie prosty tekst `Reply with exactly: OK`. Nie wysyła plików i nie zapisuje klucza. Brak ukrytego wejścia powoduje przerwanie testu, nie wyświetlenie klucza.

Oczekiwany wynik:

```text
Local: PASSED
Gemini: PASSED
Code: ok
```

`Gemini: PASSED` potwierdza uzyskanie pełnej odpowiedzi tekstowej w chwili testu. **Nie potwierdza bezpłatności, przyszłych limitów, poprawności narzędzi agenta ani prawdziwości odpowiedzi modelu.** Nie wykonuj testu wielokrotnie w pętli.

## Jeśli coś nie działa

| Wynik lub problem | Co zrobić |
| --- | --- |
| `git`, `py`, `python` lub `python3` nie działa | Sprawdź instalację i otwórz nowe okno terminala. |
| `python_version_unsupported` | Utwórz `.venv` przy użyciu Pythona 3.11 lub 3.12. |
| Brak `.venv/.../python` | Sprawdź folder roboczy i czy udało się utworzyć środowisko. |
| `local_setup_error` | Zachowaj komplet plików repo i zainstaluj biblioteki z `requirements.txt` w tym samym `.venv`. |
| `sdk_version_mismatch` | Ponownie zainstaluj wymagania z `requirements.txt`, używając Pythona ze swojego `.venv`. |
| Notebook używa innego Pythona | W VS Code wybierz kernel z `.venv` tego repo. W JupyterLab zatrzymaj serwer (Ctrl+C w terminalu) i uruchom go ponownie poleceniem z kroku 4. Wykonaj obie komórki ponownie. |
| `invalid_key_input`, `hidden_input_unavailable` | Użyj zwykłego terminala. Nie wpisuj klucza w widoczne pole; możesz pominąć API. |
| `access_denied`, `request_rejected` | Jeśli lokalna część działa, wybierz wariant lokalny. Nie twórz kont w celu obejścia ograniczeń. |
| `billing_required`, `rate_limited` | Przerwij próby API. Nie włączaj płatności ani nie obchodź limitów. |
| `model_unavailable` | Zgłoś kod lub wybierz wariant lokalny; nie zmieniaj modelu na przypadkowy. |
| `timeout`, `service_unavailable`, `connection_or_sdk_error` | Sprawdź internet. Nie wyłączaj weryfikacji TLS ani zabezpieczeń sieci. API możesz pominąć. |
| `no_text_response` | Nie otrzymano pełnej odpowiedzi tekstowej. To nie jest potwierdzenie działania API. |
| `Gemini: NOT_RUN` | Żądanie nie zostało wysłane. Przy `--local-only` to oczekiwany wynik. |
| `Gemini: INCOMPLETE` | Test przerwano po rozpoczęciu próby. Nie ma potwierdzenia powodzenia; nie ponawiaj go w pętli. |

Brak API nie wyklucza udziału. Jeśli problem dotyczy części lokalnej, napisz przed zajęciami na **[ju.gajdek@gmail.com](mailto:ju.gajdek@gmail.com)**. Podaj numer kroku, system i wartości pól `Python`, `Local`, `Gemini`, `Code` (przy API również `Model`). Przy problemie notebooka podaj nazwę wybranego kernela. **Nie wysyłaj klucza, strony z kluczami ani pełnej zawartości terminala.**

## Gotowość przed zajęciami

- [ ] Mam laptop i ładowarkę.
- [ ] Mam komplet plików tego repo.
- [ ] Test lokalny pokazał `Local: PASSED`.
- [ ] Notebook kontrolny pokazał `Notebook: PASSED`.
- [ ] Opcjonalnie: mam własny bezpłatny dostęp do Gemini API i wynik `Gemini: PASSED`.

Pliki `.venv`, `.env`, klucze i logi nie należą do repo. Przed udostępnieniem własnej kopii notebooka wyczyść wyniki komórek. `.gitignore` nie usuwa sekretów z plików już zapisanych w historii Gita.
