# Projekt: P016-wedos-online
# Zadání: Monitorování služeb přes WEDOS OnLine přes terminál
# Verze 1.0
# Celkem čas 2:20h

# importy
import json
import requests
import os
import time
from colorama import init, Fore

init(convert=True)

def hezka_tabulka(string, znaku):
    string = str(string)
    delka_string = len(string)
    if delka_string >= znaku:
        mezer = 0
    else:
        mezer = znaku - delka_string
    string = string + ' ' * mezer
    return string

# ----- config -------
from config import wedos_api_klic, wedos_api_email # API key a e-mail
wedos_api_url   = 'https://api.wedos.online/mon/'
# --------------------

# Vyčistíme obrazovku
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
    time.sleep(2)
# ---------------


while True:
    os.system('cls')
    dotaz = wedos_api_url + 'checks'
    odpoved = requests.request(method='GET', url=dotaz, headers=headers)
    json_data = json.loads(odpoved.text)
    #print (json_data)
    aktualni_cas = time.strftime("%H:%M:%S", time.localtime())
    print (f'Čas požadavku: {aktualni_cas}')
    print ('┌────────────────────────────────┬──────────────────────────────────────────────────────────────┬──────────────────┬────┬────────┬───────┐')
    print ('│ Název kontroly                 │ Cíl kontroly                                                 │ Stav             │Varo│Dostupno│Vteřin │')
    print ('├────────────────────────────────┼──────────────────────────────────────────────────────────────┼──────────────────┼────┼────────┼───────┤')
    for kontroly in json_data['results']:
        # statusStamp 
        radek  = '│ '
        nazev_vystup = kontroly["name"] + ' [' + kontroly["type"] + ']'
        radek += hezka_tabulka(nazev_vystup, 30)
        radek += ' │ '
        radek += hezka_tabulka(kontroly["fullTarget"], 60)
        radek += ' │ '
        if kontroly["status"] == 'ok':
            radek += Fore.GREEN + hezka_tabulka(kontroly["status"], 16) + Fore.RESET
        else: 
            radek += hezka_tabulka(kontroly["status"], 16)
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
        if kontroly["errorSeconds_1d"] > 0:
            radek += Fore.RED + hezka_tabulka(kontroly["errorSeconds_1d"], 5) + Fore.RESET
        else:
            radek += Fore.GREEN + hezka_tabulka(kontroly["errorSeconds_1d"], 5) + Fore.RESET
        radek += ' │'

        print (radek)

    print ('└────────────────────────────────┴──────────────────────────────────────────────────────────────┴──────────────────┴────┴────────┴───────┘')

    #print(odpoved.status_code)
    #print(odpoved.text)

    for i in range(30):
        time.sleep(1)
        print(f"Aktualizace za: {30-i} ", end="\r")
