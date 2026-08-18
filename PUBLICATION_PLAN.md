# Piano di pubblicazione completa

## Obiettivo

Offrire gratuitamente alla comunità degli sviluppatori SCADA Ignition il converter completo,
senza limitazioni funzionali, sia come sorgente sia come eseguibile Windows verificabile.

## Contenuti pubblici previsti

- sorgenti Python completi;
- test automatici e script riproducibile di packaging;
- dipendenze runtime e di sviluppo dichiarate;
- eseguibile Windows e checksum SHA-256;
- esempi sintetici di file `.properties` e workbook, privi di dati cliente;
- guida d'uso, limiti del formato e procedura per segnalare problemi.

Non sono previste versioni demo, limiti sul numero di chiavi o lingue, timeout o funzioni bloccate.

## Licenza

Il codice originale è distribuito sotto licenza MIT. Le dipendenze e gli strumenti di packaging
mantengono le licenze dei rispettivi titolari e sono elencati in `THIRD_PARTY_NOTICES.md`.

## Checklist prima della pubblicazione

1. aggiungere esempi sintetici e una prova end-to-end dell'eseguibile;
2. generare il pacchetto con `scripts/Build-Release.ps1`;
3. verificare apertura della GUI e conversione in entrambe le direzioni;
4. controllare dipendenze, segreti, dati cliente e file generati;
5. includere licenze di terze parti, note di versione e checksum;
6. pubblicare soltanto dopo approvazione esplicita del proprietario, ricevuta il 2026-08-18.
