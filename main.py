# Projekt: P016-wedos-online
# Zadání: Monitorování služeb přes WEDOS OnLine přes terminál
# Verze 1.1
# Celkem čas 3:05h

# importy
import json
import requests
import os
import time
from colorama import init, Fore

init(convert=True)

# Vyčistíme debugovací soubor
open('debug.txt', 'w').close()

# Funkce start
def hezka_tabulka(string, znaku):
    string = str(string)
    delka_string = len(string)
    if delka_string == znaku:
        mezer = 0
    elif delka_string > znaku:
        string = string[0:(znaku-3)] + '...'
        mezer = 0
    else:
        mezer = znaku - delka_string
    string = string + ' ' * mezer
    return string

def nazev_stavu(string):
    if string == 'unknown':
        return Fore.WHITE + hezka_tabulka('Čeká na test', 16) + Fore.RESET
    elif string == 'ok':
        return Fore.GREEN + hezka_tabulka('V pořádku', 16) + Fore.RESET
    elif string == 'slow':
        return Fore.YELLOW + hezka_tabulka('Pomalý', 16) + Fore.RESET
    elif string == 'response_timeout':
        return Fore.RED + hezka_tabulka('Timeout odpovědi', 16) + Fore.RESET
    elif string == 'down':
        return Fore.RED + hezka_tabulka('Bez odpovědi', 16) + Fore.RESET
    elif string == 'response_error':
        return Fore.RED + hezka_tabulka('Chybná odpověď', 16) + Fore.RESET
    elif string == 'maintenance':
        return Fore.CYAN + hezka_tabulka('Údržba', 16) + Fore.RESET
    elif string == 'paused':
        return Fore.WHITE + hezka_tabulka('Zastaveno', 16) + Fore.RESET
    elif string == 'disabled':
        return Fore.RED + hezka_tabulka('Kontr. zrušena', 16) + Fore.RESET
    elif string == 'denied':
        return Fore.RED + hezka_tabulka('Kontr. odmítnuta', 16) + Fore.RESET
    elif string == 'unverified':
        return Fore.RED + hezka_tabulka('Čelá na ověření', 16) + Fore.RESET
    elif string == 'invalidStatus':
        return Fore.RED + hezka_tabulka('Jiný problém', 16) + Fore.RESET
    else:
        return Fore.RED + hezka_tabulka(string, 16) + Fore.RESET

def debug_log(string):
    aktualni_cas = time.strftime("%H:%M:%S", time.localtime())
    log = str(aktualni_cas) + ': ' + str(string) + '\n'
    with open('debug.txt', 'a', encoding='utf8') as debug_soubor:
        debug_soubor.write(log)

# Funkce end

# ----- config -------
from config import wedos_api_klic, wedos_api_email # API key a e-mail
wedos_api_url   = 'https://api.wedos.online/mon/'
# --------------------

debug_log('Skript spuštěn...')

# Vyčistíme okno a zvětříme jej
os.system('cls')
os.system('mode con: cols=140 lines=52')
#140x52


# sestavíme header dotazu
headers = {
    'Accept': 'application/json',
    'X-Auth-User' : wedos_api_email,
    'X-Auth-Key': wedos_api_klic
}

# Pošleme PING na API abychom se ujistili, že vše funguje
print(f'Pokus o navzázaní spojení...')

dotaz = wedos_api_url + 'ping'
odpoved = requests.request(method='GET', url=dotaz, headers=headers)

if odpoved.status_code == 403:
    print(f'Stavový kód {Fore.RED}403{Fore.RESET} Přístup zamítnut.')
    json_data = json.loads(odpoved.text)
    chyba_text = json_data['error']['error']
    if json_data['error']['code'] == 'C505':
        print(f'Chyba {Fore.RED}{chyba_text}{Fore.RESET} - hlavička dotazu neobsahuje kompletní informace pro přihlášení.')
    elif  json_data['error']['code'] == 'C507':
        print(f'Chyba {Fore.RED}{chyba_text}{Fore.RESET} - Chyba přihlášení - zřejmě neplatý klíč anebo uživatel.')
    else:
        print(f'Chyba {Fore.RED}{chyba_text}{Fore.RESET} - ?.')
    quit()

if (odpoved.status_code == 200):
    print(f'Stavový kód {Fore.GREEN}200{Fore.RESET} - Úspěšně jsme se spojili se serverem WEDOS OnLine')
    time.sleep(1)
# ---------------

# volba
print('Jaké kontroly chceš zobrazit?')
print(f'{Fore.YELLOW}[1]{Fore.RESET} - Všechny {Fore.YELLOW}[2]{Fore.RESET} - Jen výpadky')
volba = input()
debug_log(f'Volba {volba}')
try:
    volba = int(volba)
except:
    volba = 1

while True:
    # mazání obrazovaky
    if(os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')

    # všechny 
    if volba == 1:
        dotaz           = wedos_api_url + 'checks'
        co_kontrolujeme = 'Všechny kontroly'
    # výpadky (down)
    elif volba == 2:
        dotaz = wedos_api_url + 'checks' + '?status=down'
        co_kontrolujeme = 'Pouze výpadky'
    # ostatní
    else:
        dotaz = wedos_api_url + 'checks'
        co_kontrolujeme = 'Všechny kontroly'

    debug_log(str(dotaz) + ' ' + str(odpoved.status_code))
    odpoved = requests.request(method='GET', url=dotaz, headers=headers)
    json_data = json.loads(odpoved.text)
    debug_log(json_data)
    
    aktualni_cas = time.strftime("%H:%M:%S", time.localtime())
    print (f'Čas požadavku: {aktualni_cas} ({co_kontrolujeme})')
    print ('┌────────────────────────────────┬──────────────────────────────────────────────────────────────┬──────────────────┬────┬────────┬───────┐')
    print ('│ Název kontroly                 │ Cíl kontroly                                                 │ Stav             │Varo│Dostupno│Vteřin │')
    print ('├────────────────────────────────┼──────────────────────────────────────────────────────────────┼──────────────────┼────┼────────┼───────┤')
    for kontroly in json_data['results']:
        # statusStamp 
        radek  = '│ '
        nazev_vystup = '[' + kontroly["type"] + '] ' +kontroly["name"]
        radek += hezka_tabulka(nazev_vystup, 30)
        radek += ' │ '
        radek += hezka_tabulka(kontroly["fullTarget"], 60)
        radek += ' │ '
        radek += nazev_stavu(kontroly["status"])
        radek += ' │ '
        radek += hezka_tabulka(kontroly["warningsCount"], 2)
        radek += ' │ '
        if kontroly["uptime_1d"] == 100:
            radek += Fore.GREEN + hezka_tabulka(kontroly["uptime_1d"], 6) + Fore.RESET
        elif kontroly["uptime_1d"] >= 99:
            radek += Fore.YELLOW + hezka_tabulka(kontroly["uptime_1d"], 6) + Fore.RESET
        else:
            radek += Fore.RED + hezka_tabulka(kontroly["uptime_1d"], 6) + Fore.RESET
        radek += ' │ '
        if kontroly["errorSeconds_1d"] is not None and kontroly["errorSeconds_1d"] > 0:
            radek += Fore.RED + hezka_tabulka(kontroly["errorSeconds_1d"], 5) + Fore.RESET
        else:
            radek += Fore.GREEN + hezka_tabulka(kontroly["errorSeconds_1d"] or 0, 5) + Fore.RESET
        radek += ' │'

        print (radek)

    print ('└────────────────────────────────┴──────────────────────────────────────────────────────────────┴──────────────────┴────┴────────┴───────┘')

    #print(odpoved.status_code)
    #print(odpoved.text)

    for i in range(30):
        time.sleep(1)
        print(f"Aktualizace za: {30-i} ", end="\r")