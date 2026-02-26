# LED from a Web Page

Progetto scolastico sviluppato per i corsi di **Sistemi e Reti** e **TPSIT** (Tecnologie e Progettazione di Sistemi Informatici e di Telecomunicazioni).

L'obiettivo è controllare un LED fisico collegato a un **Raspberry Pi** tramite una pagina web, usando un database MySQL come livello di comunicazione tra il frontend e lo script Python in esecuzione sulla scheda.

---

## 🏗️ Architettura

```
Browser  ──── index.php / script.js ──┐
         ◄─── get_state.php (500 ms) ──┤  HTTP (GET)
                                       ▼
                           setUpdate.php  ──►  MySQL DB (ledtable)
                           get_state.php  ◄──  MySQL DB (ledtable)
                                                    ▲
                                                    │  polling ogni 200 ms
                                              script.py (Raspberry Pi)
                                                    │
                                          GPIO BOARD pin 7
                                                    │
                                                  💡 LED
```

1. L'utente clicca il pulsante **On/Off** sulla pagina web.
2. `script.js` invia una richiesta GET a `setUpdate.php`, che imposta `toChange = 1` nel database.
3. `script.py`, in esecuzione sul Raspberry Pi, controlla continuamente il DB (ogni 200 ms): quando trova `toChange = 1` inverte lo stato del LED fisico e resetta il flag a `0`.
4. `get_state.php` viene interrogato ogni 500 ms dal browser per aggiornare l'etichetta **LED Acceso / LED Spento** sulla pagina.

---

## 📁 Struttura del progetto

| File | Descrizione |
|------|-------------|
| `index.php` | Pagina web principale con il pulsante di controllo |
| `script.js` | Logica client-side: toggle e polling dello stato |
| `setUpdate.php` | Imposta `toChange = 1` nel DB per segnalare un cambio di stato |
| `get_state.php` | Restituisce lo stato corrente del LED come JSON |
| `conn.db.php` | Parametri di connessione al database |
| `script.py` | Script Python sul Raspberry Pi: legge il DB e pilota il GPIO |
| `ledtable.sql` | Schema e dati iniziali della tabella MySQL |

---

## 🔧 Requisiti

### Server web (es. Raspberry Pi o altro host)
- PHP 7.x o superiore con l'estensione `mysqli`
- Web server (Apache, Nginx, …)
- MySQL / MariaDB

### Raspberry Pi (per il controllo fisico del LED)
- Python 3
- Librerie Python:
  - `mysql-connector-python`
  - `RPi.GPIO`
- LED collegato al **pin fisico 7** (numerazione BOARD, corrisponde a GPIO 4 in modalità BCM)

---

## 🚀 Setup

### 1. Database

Importare lo schema nel database MySQL:

```bash
mysql -u root -p < ledtable.sql
```

Il comando crea il database `led` con la tabella `ledtable` contenente una riga con `toChange = 0` e `ledState = 0`.

### 2. Configurazione della connessione

Modificare `conn.db.php` con le proprie credenziali MySQL:

```php
$host = 'localhost';
$user = 'utente';
$pass = 'password';
$db   = 'led';
```

Aggiornare anche i parametri di connessione all'interno di `script.py`:

```python
mydb = mysql.connector.connect(
    host   = "localhost",
    user   = "utente",
    passwd = "password",
    database = "led"
)
```

### 3. Web server

Copiare i file PHP nella root del web server (es. `/var/www/html/`) e avviarlo.

### 4. Script Python

Installare le dipendenze:

```bash
pip install mysql-connector-python RPi.GPIO
```

Impostare le variabili all'inizio di `script.py`:

```python
ledPin         = 7     # pin fisico BOARD (= GPIO 4 in BCM); lo script usa GPIO.BOARD
iAmOnRaspberry = True  # True se si esegue su Raspberry Pi
debug          = False # True per log su console
```

Avviare lo script:

```bash
python script.py
```

---

## 🖥️ Utilizzo

1. Aprire nel browser l'indirizzo del server (es. `http://<ip-raspberry>/`).
2. La pagina mostra lo stato attuale del LED (**LED Acceso** / **LED Spento**).
3. Premere il pulsante **On/Off led** per cambiare lo stato.

---

## 🛠️ Tecnologie utilizzate

- **PHP** – backend web e accesso al database
- **JavaScript** (Fetch API) – comunicazione asincrona con il server
- **Bootstrap 5** – interfaccia grafica responsive
- **MySQL / MariaDB** – strato di comunicazione tra web server e Raspberry Pi
- **Python 3** – controllo del GPIO sul Raspberry Pi
- **RPi.GPIO** – libreria per la gestione dei pin GPIO

