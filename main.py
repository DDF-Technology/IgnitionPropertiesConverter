# Importa ttkbootstrap per una GUI moderna basata su Tkinter
import ttkbootstrap as tb

# Importa la classe dell'interfaccia utente dal modulo ui_components
from ui_components import PropertiesConverterApp

# Punto di ingresso principale dell'applicazione
if __name__ == "__main__":
    # Crea la finestra principale con un tema scuro
    app = tb.Window(themename="darkly")

    # Inizializza l'applicazione con l'interfaccia definita
    PropertiesConverterApp(app)

    # Avvia il loop principale dell'interfaccia grafica
    app.mainloop()