# LedFromAWebPage

Progetto scolastico realizzato per i corsi di **Sistemi e Reti** e **TPSIT** (Tecnologie e Progettazione di Sistemi Informatici e di Telecomunicazioni).

L'obiettivo è controllare un LED collegato a un **Raspberry Pi** tramite una pagina web, sfruttando un database MySQL come livello di comunicazione tra il browser e l'hardware.

---

## Architettura

```
Browser (index.php + script.js)
        |
        | HTTP (Fetch API)
        v
   Server PHP (setUpdate.php / get_state.php)
        |
        | MySQL
        v
   Database MariaDB (tabella ledtable)
        ^
        | polling ogni 200 ms
        |
   script.py (Raspberry Pi)
        |
        | RPi.GPIO
        v
      LED (GPIO pin 7)
```

**Flusso di funzionamento:**

1. L'utente preme il pulsante "On/Off led" sulla pagina web.
2. `script.js` esegue una chiamata a `setUpdate.php`, che imposta `toChange = 1` nel database.
3. `script.py`, in esecuzione sul Raspberry Pi, interroga il database ogni 200 ms.
4. Quando rileva `toChange = 1`, inverte lo stato del LED tramite GPIO e resetta il flag a `toChange = 0`.
5. `script.js` aggiorna l'indicatore di stato (LED Acceso / LED Spento) interrogando `get_state.php` ogni 500 ms.

---

## Tecnologie utilizzate

| Componente     | Tecnologia                         |
|----------------|------------------------------------|
| Frontend       | PHP, HTML, Bootstrap 5, JavaScript |
| Backend API    | PHP, MySQLi                        |
| Database       | MariaDB / MySQL                    |
| Hardware       | Raspberry Pi + RPi.GPIO (Python 3) |

---

## Requisiti

### Server web
- PHP 7.3+
- MariaDB / MySQL
- Apache o Nginx (con mod_php)

### Raspberry Pi
- Python 3
- Librerie Python: `mysql-connector-python`, `RPi.GPIO`

```bash
pip install mysql-connector-python RPi.GPIO
```

---

## Installazione e configurazione

### 1. Database

Importare lo schema SQL nel database MySQL/MariaDB:

```bash
mysql -u root -p < ledtable.sql
```

Questo creerà il database `led` con la tabella `ledtable` e inserirà il record iniziale.

### 2. Configurazione connessione database

Modificare `conn.db.php` con le credenziali del proprio database:

```php
$host = 'localhost';
$user = 'nome_utente';
$pass = 'password';
$db   = 'led';
```

Le stesse credenziali vanno aggiornate nella funzione `connect()` di `script.py`.

### 3. Server web

Copiare i file PHP (`index.php`, `conn.db.php`, `get_state.php`, `setUpdate.php`) e `script.js` nella directory pubblica del server web (es. `/var/www/html/led/`).

> **⚠️ Sicurezza:** `conn.db.php` contiene le credenziali del database. In un ambiente di produzione è consigliabile spostarlo al di fuori della document root e includerlo tramite percorso assoluto, oppure configurare il server web per bloccare l'accesso diretto ai file di configurazione PHP.

### 4. Script Raspberry Pi

Sul Raspberry Pi, aprire `script.py` e impostare:

```python
ledPin = 7          # pin 7 (numerazione BOARD) = GPIO 4 (numerazione BCM)
iAmOnRaspberry = True
```

Avviare lo script:

```bash
python3 script.py
```

> **Nota:** il Raspberry Pi e il server web devono poter accedere allo stesso database MySQL.

---

## Struttura del progetto

```
led-from-webpage/
├── index.php        # Pagina web principale con il pulsante On/Off
├── script.js        # Logica frontend: invio comandi e aggiornamento stato
├── script.py        # Script Python per il controllo del LED sul Raspberry Pi
├── conn.db.php      # Configurazione connessione al database
├── get_state.php    # API: restituisce lo stato attuale del LED (JSON)
├── setUpdate.php    # API: imposta il flag di cambio stato nel database
└── ledtable.sql     # Schema SQL della tabella del database
```

---

## Schema del database

**Tabella `ledtable`** (database `led`):

| Colonna    | Tipo         | Descrizione                                       |
|------------|--------------|---------------------------------------------------|
| `toChange` | tinyint(1)   | Flag: `1` = richiesta di cambio stato pendente    |
| `ledState` | tinyint(1)   | Stato attuale del LED: `0` = spento, `1` = acceso |

