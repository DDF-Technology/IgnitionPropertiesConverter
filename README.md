# IgnitionPropertiesConverter

Utility desktop per gestire file di localizzazione Java/Ignition. Converte uno o più file
`.properties` in un foglio Excel modificabile e ricrea i file di lingua dalle colonne del workbook.

## Flusso operativo

- conversione properties → Excel per confrontare chiavi e traduzioni in forma tabellare;
- modifica o revisione delle traduzioni nel workbook;
- conversione Excel → properties per rigenerare i file destinati al progetto Ignition.

Conservare una copia degli originali e controllare l'output prima dell'importazione: escaping,
duplicati, righe commentate e codifica possono avere significati specifici nel sistema sorgente.
I commenti e la formattazione originale non vengono conservati. Le formule Excel vengono rifiutate,
mentre i valori `.properties` che iniziano con `=` rimangono testo letterale.

## Download

La pre-release Windows portable è disponibile nella pagina
[v1.0.0-rc2](https://github.com/DDF-Technology/IgnitionPropertiesConverter/releases/tag/v1.0.0-rc2).
Il pacchetto non è firmato: verificare il file `.sha256` pubblicato insieme allo ZIP prima dell'avvio.

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

## Test e pacchetto Windows

Le dipendenze di sviluppo sono separate da quelle runtime. Per il pacchetto Windows verificato usare Python 3.14 con il componente Tcl/Tk installato:

```powershell
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
.\.venv\Scripts\python -m unittest discover -s tests -v
powershell -ExecutionPolicy Bypass -File .\scripts\Build-Release.ps1
```

Lo script esegue i test prima di creare un candidato locale in `artifacts\release`, completo di
eseguibile, esempi, documentazione, licenze, inventario e checksum SHA-256. Gli artefatti generati
restano locali ed esclusi dal repository sorgente.

La guida per l'utente è disponibile in [docs/public/USER_GUIDE.md](docs/public/USER_GUIDE.md) e lo
stato dei gate precedenti alla pubblicazione in [docs/RELEASE_READINESS.md](docs/RELEASE_READINESS.md).

## Proprietà e licenza

Il progetto è distribuito gratuitamente e integralmente sotto [licenza MIT](LICENSE) alla comunità
degli sviluppatori SCADA Ignition. Le dipendenze mantengono le licenze dei rispettivi titolari,
riepilogate in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Vedere anche
[PUBLICATION_PLAN.md](PUBLICATION_PLAN.md).

Ignition è un marchio di Inductive Automation. Questo progetto indipendente non è affiliato,
approvato o sponsorizzato da Inductive Automation.
