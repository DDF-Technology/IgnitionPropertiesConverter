# IgnitionPropertiesConverter

Utility desktop per gestire file di localizzazione Java/Ignition. Converte uno o più file
`.properties` in un foglio Excel modificabile e ricrea i file di lingua dalle colonne del workbook.

## Flusso operativo

- conversione properties → Excel per confrontare chiavi e traduzioni in forma tabellare;
- modifica o revisione delle traduzioni nel workbook;
- conversione Excel → properties per rigenerare i file destinati al progetto Ignition.

Conservare una copia degli originali e controllare l'output prima dell'importazione: escaping,
duplicati, righe commentate e codifica possono avere significati specifici nel sistema sorgente.

## Requisiti e avvio

- Python 3.10 o successivo;
- Tkinter;
- `pandas`, `openpyxl` e `ttkbootstrap`.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python main.py
```

## Struttura

- `main.py`: creazione della finestra e avvio dell'applicazione;
- `ui_components.py`: interfaccia e flussi di conversione;
- `converter.py`: lettura, trasformazione e scrittura dei formati;
- `main.spec`: configurazione storica PyInstaller.

L'eseguibile storico in `dist` è conservato localmente ma escluso dal repository.

## Proprietà e licenza

Copyright © 2026 Fabio De Deo — [www.ddf.technology](https://www.ddf.technology/). Tutti i
diritti riservati. Consultare [LICENSE](LICENSE).
