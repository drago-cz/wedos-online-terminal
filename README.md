 ## WEDOS OnLine Terminal

 *WEDOS OnLine Terminal* je skript v Python, který se připojí přes API na službu WEDOS OnLine a v terminálu zobrazí aktuální stav kontrol za posledních 24 hodin. Následně se každých 30 vteřin aktualizuje.

![WEDOS OnLine Terminal](https://github.com/drago-cz/wedos-online-terminal/blob/master/screenshot.png)

### Požadavky
 
 WEDOS OnLine terminál vyžaduje následující Python moduly:
 * colorama
 * requests

 Dále budete potřebovat **API klíč** z WEDOS OnLine. Ten získáte v administraci (https://cp.wedos.online/user/api)
 * Pro spojení se serverem je nutný API klíč a uživatelské jméno (aktuálně e-mail)
 * API klíč se po vygenerování ve WEDOS OnLine neukládá v čitelné podobě. Pokud si jej neuložíte je nutné vygenerovat nový.
 * E-mail a API klíč vložte do souboru `config.py`

### Verze 1.1.1 (aktuální)
- Fix: Handle NoneType in "errorSeconds_1d" comparison

### Verze 1.1
- [x] ošetření stavu kontrol
- [x] dát volbu filtrace kontrol při spuštění skriptu
- [x] ošetřit maximální velikost názvů přímo v hezka_tabulka()
- [x] přidání logování

### Verze 1.0
 První pracovní verze, která zobrazuje všechny kontroly a jejich aktuální stav. Refresh je na 30 vteřin. 