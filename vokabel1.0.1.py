import tkinter as tk
from tkinter import simpledialog
import random

# Funktion zum Hinzufügen von Vokabeln oder Lösungen
def hinzufügen(typ):
    eingabe = eingabe_feld.get().strip()  # Leerzeichen entfernen
    if not eingabe:
        ausgabe_label.config(text="Eingabe darf nicht leer sein!", fg="#FF4C4C", font=("Arial", 12, "bold"))
        return

    ziel_liste = vokabeln_liste if typ == "Vokabeln" else lösungen_liste
    # Prüfen, ob die Eingabe bereits vorhanden ist
    if any(
        isinstance(child, tk.Label) and child.cget("text") == eingabe
        for child in ziel_liste.winfo_children()
    ):
        ausgabe_label.config(text=f"'{eingabe}' ist bereits in {typ} vorhanden!", fg="#FF4C4C", font=("Arial", 12, "bold"))
        return

    datei_name = "vokabeln.txt" if typ == "Vokabeln" else "lösungen.txt"
    with open(datei_name, "a") as f:
        f.write(eingabe + "\n")
    
    add_item_und_button(ziel_liste, eingabe, typ)
    ausgabe_label.config(text=f"'{eingabe}' wurde zu {typ} hinzugefügt!", fg="#4CAF50", font=("Arial", 14, "bold"))
    eingabe_feld.delete(0, tk.END)

# Funktion um ein Element und einen Entfernen-Button hinzuzufügen
def add_item_und_button(liste, item, typ):
    frame = tk.Frame(liste, bg="#eeeeee", pady=10)
    frame.pack(fill="x", padx=20, pady=5)

    label = tk.Label(frame, text=item, font=("Helvetica", 14), fg="black", bg="#eeeeee", width=40, anchor="w")
    label.pack(side="left", padx=10)

    entfernen_button = tk.Button(frame, text="❌", command=lambda: entfernen_vokabel(item, typ, frame), 
                                 bg="#F44336", fg="white", font=("Arial", 12), relief="flat", activebackground="#E53935")
    entfernen_button.pack(side="right", padx=10)

# Funktion um Vokabel oder Lösung zu entfernen
def entfernen_vokabel(item, typ, frame):
    if typ == "Vokabeln":
        datei_name = "vokabeln.txt"
    else:
        datei_name = "lösungen.txt"
    
    # Datei lesen und alle Zeilen außer der zu löschenden behalten
    with open(datei_name, "r") as f:
        lines = f.readlines()

    with open(datei_name, "w") as f:
        for line in lines:
            if line.strip() != item:
                f.write(line)

    frame.destroy()  # Entfernt das Frame, das das Label und den Button enthält
    ausgabe_label.config(text=f"'{item}' wurde aus {typ} entfernt!", fg="#FF4C4C", font=("Arial", 14, "bold"))

# Funktion zum Laden der Vokabeln und Lösungen aus den Dateien
def laden(typ):
    ziel_liste = vokabeln_liste if typ == "Vokabeln" else lösungen_liste
    datei_name = "vokabeln.txt" if typ == "Vokabeln" else "lösungen.txt"

    try:
        with open(datei_name, "r") as f:
            for line in f:
                add_item_und_button(ziel_liste, line.strip(), typ)
    except FileNotFoundError:
        ausgabe_label.config(text=f"Keine {typ} gefunden.", fg="#FF4C4C", font=("Arial", 12, "bold"))

# Funktion zum Test starten
def starten_test():
    # Hauptfenster unsichtbar machen
    root.withdraw()

    # Neues Fenster für den Test
    test_fenster = tk.Toplevel(root)
    test_fenster.title('Vokabel-Test')
    test_fenster.geometry('400x400')

    # Frame für Testinhalt
    test_frame = tk.Frame(test_fenster, bg="#f4f4f4")
    test_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Frage-Label für den Test
    frage_label = tk.Label(test_frame, text="Test beginnt", font=("Helvetica", 16), fg="black", bg="#f4f4f4")
    frage_label.pack(pady=10)

    # Eingabefeld für Antwort
    antwort_feld = tk.Entry(test_frame, font=("Helvetica", 14), width=30, relief="solid", bd=2, fg="black", bg="#ffffff", insertbackground="black")
    antwort_feld.pack(pady=10)

    # Antwort-Button
    antwort_button = tk.Button(test_frame, text="Antwort prüfen", bg="#FF9800", fg="white", font=("Helvetica", 12), relief="flat", activebackground="#FB8C00", height=2)
    antwort_button.pack(pady=10)

    # Fortschrittsanzeige
    fortschritt_label = tk.Label(test_frame, text="Fragen 0/0", font=("Helvetica", 12), fg="black", bg="#f4f4f4")
    fortschritt_label.pack(pady=5)

    # Liste der Vokabeln und Lösungen
    vokabel_list = [vokabel_frame.winfo_children()[0].cget("text") for vokabel_frame in vokabeln_liste.winfo_children()]
    lösung_list = [lösung_frame.winfo_children()[0].cget("text") for lösung_frame in lösungen_liste.winfo_children()]

    # Gesamtzahl der Fragen
    gesamt_fragen = len(vokabel_list)

    # Die Gesamtzahl der Fragen anzeigen
    fortschritt_label.config(text=f"Fragen 0/{gesamt_fragen}")

    # Funktionen für den Test
    def fragen_test():
        if not vokabel_list:
            frage_label.config(text="Test abgeschlossen!", fg="#4CAF50", font=("Arial", 14, "bold"))
            test_fenster.after(2000, test_fenster.destroy)  # Fenster nach 2 Sekunden schließen
            # Hauptfenster wieder sichtbar machen
            root.deiconify()
            return

        vokabel = vokabel_list.pop(0)  # Erste Vokabel holen
        lösung = lösung_list.pop(0)  # Entsprechende Lösung holen

        frage_label.config(text=f"Was bedeutet '{vokabel}'?")
        antwort_feld.delete(0, tk.END)

        # Antwort prüfen
        def check_answer():
            user_input = antwort_feld.get().strip()  # Benutzerantwort auslesen
            if user_input.lower() == lösung.lower():
                frage_label.config(text="Gut gemacht!", fg="#4CAF50", font=("Arial", 16, "bold"))
            else:
                frage_label.config(text=f"Leider falsch. Die richtige Antwort ist '{lösung}'", fg="#FF4C4C", font=("Arial", 14, "bold"))

            antwort_feld.delete(0, tk.END)  # Eingabefeld nach der Antwort zurücksetzen
            # Fortschritt aktualisieren
            fortschritt_label.config(text=f"Fragen {gesamt_fragen - len(vokabel_list)}/{gesamt_fragen}")
            # Nächste Frage stellen
            test_fenster.after(1500, fragen_test)  # 1.5 Sekunden warten und zur nächsten Frage übergehen

        antwort_button.config(command=check_answer)

    # Test starten
    fragen_test()

# Funktion zum Leeren der Listen und Dateien
def listen_leeren():
    # Vokabeln und Lösungen aus den Frames entfernen
    for frame in vokabeln_liste.winfo_children():
        frame.destroy()
    for frame in lösungen_liste.winfo_children():
        frame.destroy()

    # Dateien leeren
    with open("vokabeln.txt", "w") as f:
        f.truncate(0)
    with open("lösungen.txt", "w") as f:
        f.truncate(0)

    ausgabe_label.config(text="Listen wurden geleert!", fg="#FF4C4C", font=("Arial", 14, "bold"))

# Fenster erstellen
root = tk.Tk()
root.title('Vokabel-Trainer')
root.minsize(800, 600)
root.config(bg="#f4f4f4")

# Haupt-Container für Layout
main_frame = tk.Frame(root, bg="#f4f4f4")
main_frame.pack(pady=30, padx=30, fill="both", expand=True)

# Titel hinzufügen
label = tk.Label(main_frame, text="Willkommen zum Vokabel-Trainer", font=("Helvetica", 26, "bold"), fg="#2196F3", bg="#f4f4f4")
label.pack(pady=20)

# Eingabefeld für Vokabeln/Lösungen
eingabe_feld = tk.Entry(main_frame, font=("Helvetica", 14), width=30, relief="solid", bd=2, fg="black", bg="#ffffff", insertbackground="black")
eingabe_feld.pack(pady=10)

# Ausgabe-Label für Statusmeldungen
ausgabe_label = tk.Label(main_frame, text="", font=("Helvetica", 14), fg="black", bg="#f4f4f4")
ausgabe_label.pack(pady=10)

# Listen-Container für Vokabeln
vokabeln_liste = tk.Frame(main_frame, bg="#f4f4f4")
vokabeln_liste.pack(pady=10, fill="both", expand=True)

# Listen-Container für Lösungen
lösungen_liste = tk.Frame(main_frame, bg="#f4f4f4")
lösungen_liste.pack(pady=10, fill="both", expand=True)

# Buttons
button_vokabeln = tk.Button(main_frame, text="Vokabeln hinzufügen", command=lambda: hinzufügen("Vokabeln"), bg="#2196F3", fg="white", font=("Helvetica", 12), relief="flat", activebackground="#1e88e5")
button_vokabeln.pack(pady=10, fill="x", padx=50)

button_lösungen = tk.Button(main_frame, text="Lösungen hinzufügen", command=lambda: hinzufügen("Lösungen"), bg="#2196F3", fg="white", font=("Helvetica", 12), relief="flat", activebackground="#1e88e5")
button_lösungen.pack(pady=10, fill="x", padx=50)

button_test = tk.Button(main_frame, text="Test starten", command=starten_test, bg="#FF9800", fg="white", font=("Helvetica", 12), relief="flat", activebackground="#FB8C00", height=2)
button_test.pack(pady=20, fill="x", padx=50)

button_leeren = tk.Button(main_frame, text="Listen leeren", command=listen_leeren, bg="#F44336", fg="white", font=("Helvetica", 12), relief="flat", activebackground="#D32F2F", height=2)
button_leeren.pack(pady=10, fill="x", padx=50)

# Vokabeln und Lösungen laden
laden("Vokabeln")
laden("Lösungen")

# Label für "by: Ben" hinzufügen und unten rechts positionieren
by_label = tk.Label(root, text="by: Ben", font=("Helvetica", 10), fg="gray", bg="#f4f4f4")
by_label.pack(side="bottom", anchor="se", padx=20, pady=10)

# Hauptschleife starten
root.mainloop()
