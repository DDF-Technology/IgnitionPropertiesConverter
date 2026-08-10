# Importa moduli standard
import os  # Operazioni su file e percorsi
import pandas as pd  # Gestione di dati tabellari e file Excel

def read_properties_file(filepath):
    """
    Legge un file .properties e restituisce un dizionario con le coppie chiave=valore.

    Args:
        filepath (str): Percorso del file .properties da leggere.

    Returns:
        dict: Dizionario contenente le coppie chiave=valore.
    """
    data = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Ignora righe vuote o commentate
            if line and not line.startswith("#"):
                if "=" in line:
                    key, value = line.split("=", 1)  # Divide solo alla prima '='
                    data[key.strip()] = value.strip()
    return data

def export_to_excel(properties_files, output_path):
    """
    Converte una lista di file .properties in un unico file Excel.

    Ogni lingua diventa una colonna, e ogni chiave è una riga.

    Args:
        properties_files (list[str]): Elenco di file .properties da unire.
        output_path (str): Percorso del file Excel da creare.
    """
    all_data = {}

    for file in properties_files:
        # Estrae il codice lingua dal nome file (es: Language_it.properties -> 'it')
        lang_code = os.path.splitext(os.path.basename(file))[0].split("_")[-1]
        props = read_properties_file(file)

        for key, value in props.items():
            if key not in all_data:
                all_data[key] = {}
            all_data[key][lang_code] = value

    # Conversione in DataFrame: righe = chiavi, colonne = codici lingua
    df = pd.DataFrame.from_dict(all_data, orient="index").reset_index()
    df = df.rename(columns={"index": "key"})
    df = df.sort_values(by="key")

    # Esporta il DataFrame in un file Excel
    df.to_excel(output_path, index=False)

def import_from_excel(excel_file, output_dir):
    """
    Converte un file Excel in più file .properties, uno per ciascuna lingua.

    Args:
        excel_file (str): Percorso del file Excel da leggere.
        output_dir (str): Cartella dove salvare i file .properties generati.
    """
    df = pd.read_excel(excel_file)

    for col in df.columns:
        if col.lower() == "key":
            continue  # Salta la colonna delle chiavi

        # Crea il percorso del file .properties per ogni lingua
        filepath = os.path.join(output_dir, f"Language_{col}.PROPERTIES")

        with open(filepath, "w", encoding="utf-8") as f:
            for _, row in df.iterrows():
                if pd.notna(row[col]):
                    f.write(f"{row['key']}={row[col]}\n")