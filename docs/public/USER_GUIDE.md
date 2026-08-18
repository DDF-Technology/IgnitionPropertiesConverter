# Guida rapida

## Da `.properties` a Excel

1. Avviare `IgnitionPropertiesConverter.exe`.
2. Selezionare **Da .properties a Excel**.
3. Scegliere uno o più file con nomi distinti per lingua, ad esempio `Language_it.properties` e `Language_en.properties`.
4. Indicare il file `.xlsx` di destinazione.
5. Modificare le traduzioni senza rinominare la colonna `key` e senza inserire formule.

## Da Excel a `.properties`

1. Selezionare **Da Excel a .properties**.
2. Scegliere il workbook modificato.
3. Selezionare una cartella di destinazione.
4. Verificare i file `Language_<lingua>.properties` prodotti prima di importarli nel progetto.

## Regole e limiti

- I file `.properties` sono letti e scritti in UTF-8.
- Commenti e formattazione originale non vengono conservati nel passaggio attraverso Excel.
- Chiavi duplicate, lingue duplicate, celle chiave vuote e formule Excel vengono rifiutate.
- Escape Java comuni, Unicode `\uXXXX` e continuazioni di riga sono gestiti.
- Conservare sempre una copia degli originali e controllare l'output prima dell'importazione.
