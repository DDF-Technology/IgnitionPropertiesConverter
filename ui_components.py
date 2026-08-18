# Importa ttkbootstrap per uno stile moderno e temi per Tkinter
import ttkbootstrap as tb
# Importa i dialoghi nativi di Tkinter
from tkinter import filedialog, messagebox
# Importa funzioni di conversione personalizzate da modulo esterno
from converter import export_to_excel, import_from_excel
# Operazioni su file e percorsi
import os
import sys

def resource_path(relative_path):
    """Restituisce il percorso assoluto per risorse anche da .exe"""
    try:
        base_path = sys._MEIPASS  # Cartella temporanea creata da PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class PropertiesConverterApp:
    """Applicazione GUI per convertire file .properties in Excel e viceversa."""

    def __init__(self, master):
        self.master = master

        # Titolo della finestra principale
        master.title("Ignition Properties Converter")

        # Imposta icona personalizzata della finestra
        master.iconbitmap(resource_path("Icon.ico"))

        # Mantiene una composizione compatta e prevedibile per l'utility.
        master.resizable(False, False)

        # Dimensioni e centratura finestra sullo schermo
        master.update_idletasks()
        width, height = 560, 430
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry(f"{width}x{height}+{x}+{y}")

        master.style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        master.style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        master.style.configure("Large.TButton", font=("Segoe UI", 11, "bold"), padding=(16, 12))
        master.style.configure("Footer.TLabel", font=("Segoe UI", 9))

        container = tb.Frame(master, padding=(28, 22))
        container.pack(fill="both", expand=True)

        tb.Label(container,
                 text="Ignition Properties Converter",
                 style="Title.TLabel").pack(anchor="w")
        tb.Label(container,
                 text="Converte localizzazioni .properties in Excel e le rigenera dopo la revisione.",
                 style="Subtitle.TLabel",
                 bootstyle="secondary").pack(anchor="w", pady=(2, 20))

        # Pulsante per conversione da .properties a Excel
        self.to_excel_btn = tb.Button(container,
                                      text=".properties  →  Excel",
                                      command=self.convert_to_excel,
                                      bootstyle="primary",
                                      style='Large.TButton')
        self.to_excel_btn.pack(fill='x')
        tb.Label(container,
                 text="Unisce più lingue in un unico workbook modificabile.",
                 style="Subtitle.TLabel",
                 bootstyle="secondary").pack(anchor="w", pady=(5, 14))

        # Pulsante per conversione da Excel a .properties
        self.to_properties_btn = tb.Button(container,
                                           text="Excel  →  .properties",
                                           command=self.convert_to_properties,
                                           bootstyle="outline-primary",
                                           style='Large.TButton')
        self.to_properties_btn.pack(fill='x')
        tb.Label(container,
                 text="Crea un file UTF-8 per ogni colonna lingua.",
                 style="Subtitle.TLabel",
                 bootstyle="secondary").pack(anchor="w", pady=(5, 14))

        # Barra di progresso sempre visibile, inizialmente vuota e in modalità determinate
        self.progress = tb.Progressbar(container,
                                       mode="determinate",
                                       bootstyle="info-striped")
        self.progress.pack(fill='x')
        self.progress['value'] = 0  # barra vuota all’avvio

        # Separatore orizzontale tra pulsanti e label informativa
        separator = tb.Separator(container, orient='horizontal')
        separator.pack(fill='x', pady=(18, 10))

        # Etichetta con informazioni sull'autore e sito web
        self.label = tb.Label(container,
                              text="Fabio De Deo · DDF Technology · MIT License",
                              style="Footer.TLabel",
                              bootstyle="secondary")
        self.label.pack(anchor="center")

    def convert_to_excel(self):
        """Converti uno o più file .properties selezionati in un file Excel."""
        files = filedialog.askopenfilenames(filetypes=[("Properties files", "*.properties *.PROPERTIES")])
        if not files:
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                   filetypes=[("Excel files", "*.xlsx")])
        if not output_path:
            return

        try:
            # Attiva la barra di progresso in modalità indeterminata (animazione)
            self.progress['mode'] = 'indeterminate'
            self.progress.start(10)
            self.master.update_idletasks()

            # Chiamata alla funzione di conversione esterna
            export_to_excel(files, output_path)

            # Notifica di successo
            messagebox.showinfo("Successo", f"File Excel salvato in:\n{output_path}")

        except Exception as e:
            # Mostra messaggio di errore in caso di problemi
            messagebox.showerror("Errore", str(e))

        finally:
            # Ferma l’animazione e resetta la barra a vuota in modalità determinate
            self.progress.stop()
            self.progress['mode'] = 'determinate'
            self.progress['value'] = 0

    def convert_to_properties(self):
        """Converti un file Excel selezionato in file .properties in una cartella scelta."""
        file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file:
            return

        output_dir = filedialog.askdirectory()
        if not output_dir:
            return

        try:
            # Attiva animazione barra di progresso
            self.progress['mode'] = 'indeterminate'
            self.progress.start(10)
            self.master.update_idletasks()

            # Chiamata alla funzione di conversione esterna
            import_from_excel(file, output_dir)

            # Notifica di successo
            messagebox.showinfo("Successo", f"File .properties generati in:\n{output_dir}")

        except Exception as e:
            # Mostra errore in caso di eccezioni
            messagebox.showerror("Errore", str(e))

        finally:
            # Ferma animazione e resetta barra
            self.progress.stop()
            self.progress['mode'] = 'determinate'
            self.progress['value'] = 0
