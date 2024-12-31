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

def add_item_und_button(liste, item, typ):
    frame = tk.Frame(liste, bg="#eeeeee", pady=10)
    frame.pack(fill="x", padx=20, pady=5)

    label = tk.Label(frame, text=item, font=("Helvetica", 14), fg="black", bg="#eeeeee", width=40, anchor="w")
    label.pack(side="left", padx=10)

    entfernen_button = tk.Button(frame, text="❌", command=lambda: entfernen_vokabel(item, typ, frame), 
                                 bg="#F44336", fg="white", font=("Arial", 12), relief="flat", activebackground="#E53935")
    entfernen_button.pack(side="right", padx=10)

def entfernen_vokabel(item, typ, frame):
    datei_name = "vokabeln.txt" if typ == "Vokabeln" else "lösungen.txt"
    with open(datei_name, "r") as f:
        lines = f.readlines()

    with open(datei_name, "w") as f:
        for line in lines:
            if line.strip() != item:
                f.write(line)

    frame.destroy()
    ausgabe_label.config(text=f"'{item}' wurde aus {typ} entfernt!", fg="#FF4C4C", font=("Arial", 14, "bold"))

def laden(typ):
    ziel_liste = vokabeln_liste if typ == "Vokabeln" else lösungen_liste
    datei_name = "vokabeln.txt" if typ == "Vokabeln" else "lösungen.txt"

    try:
        with open(datei_name, "r") as f:
            for line in f:
                add_item_und_button(ziel_liste, line.strip(), typ)
    except FileNotFoundError:
        ausgabe_label.config(text=f"Keine {typ} gefunden.", fg="#FF4C4C", font=("Arial", 12, "bold"))

def starten_test():
    root.withdraw()
    test_fenster = tk.Toplevel(root)
    test_fenster.title('Vokabel-Test')
    test_fenster.geometry('500x400')

    # Ändern des Designs für den Testmodus
    test_frame = tk.Frame(test_fenster, bg="#ffffff", pady=20)
    test_frame.pack(fill="both", expand=True)

    frage_label = tk.Label(test_frame, text="Test beginnt", font=("Arial", 18, "bold"), fg="#333", bg="#ffffff")
    frage_label.pack(pady=20)

    antwort_feld = tk.Entry(test_frame, font=("Arial", 16), width=25, fg="black", bg="#f0f0f0", insertbackground="black", relief="solid", bd=2)
    antwort_feld.pack(pady=10)

    # Antworten Button mit einem freundlicheren Design
    antwort_button = tk.Button(test_frame, text="Antwort prüfen", bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), relief="flat", activebackground="#45a049", height=2)
    antwort_button.pack(pady=10)

    fortschritt_label = tk.Label(test_frame, text="Fragen 0/0 | Punkte: 0", font=("Arial", 14), fg="black", bg="#ffffff")
    fortschritt_label.pack(pady=10)

    # Fragen und Lösungen laden
    vokabel_list = [vokabel_frame.winfo_children()[0].cget("text") for vokabel_frame in vokabeln_liste.winfo_children()]
    lösung_list = [lösung_frame.winfo_children()[0].cget("text") for lösung_frame in lösungen_liste.winfo_children()]

    gesamt_fragen = len(vokabel_list)
    punkte = 0

    fortschritt_label.config(text=f"Fragen 0/{gesamt_fragen} | Punkte: 0")

    def fragen_test():
        nonlocal punkte

        if not vokabel_list:
            frage_label.config(text="Test abgeschlossen!", fg="#4CAF50", font=("Arial", 18, "bold"))
            test_fenster.after(2000, test_fenster.destroy)
            root.deiconify()
            return

        vokabel = vokabel_list.pop(0)
        lösung = lösung_list.pop(0)

        frage_label.config(text=f"Was bedeutet '{vokabel}'?")
        antwort_feld.delete(0, tk.END)

        def check_answer(event=None):
            nonlocal punkte
            user_input = antwort_feld.get().strip()
            if user_input.lower() == lösung.lower():
                punkte += 1
                frage_label.config(text="Richtig!", fg="#4CAF50", font=("Arial", 16, "bold"))
            else:
                frage_label.config(text=f"Falsch! Richtig ist: '{lösung}'", fg="#FF4C4C", font=("Arial", 14, "bold"))

            fortschritt_label.config(text=f"Fragen {gesamt_fragen - len(vokabel_list)}/{gesamt_fragen} | Punkte: {punkte}")
            antwort_feld.delete(0, tk.END)
            test_fenster.after(1500, fragen_test)

        antwort_feld.bind('<Return>', check_answer)  # Enter-Taste zum Überprüfen der Antwort
        antwort_button.config(command=check_answer)

    fragen_test()

def listen_leeren():
    for frame in vokabeln_liste.winfo_children():
        frame.destroy()
    for frame in lösungen_liste.winfo_children():
        frame.destroy()

    with open("vokabeln.txt", "w") as f:
        f.truncate(0)
    with open("lösungen.txt", "w") as f:
        f.truncate(0)

    ausgabe_label.config(text="Listen wurden geleert!", fg="#FF4C4C", font=("Arial", 14, "bold"))

def erstellen_button(root, text, command, **kwargs):
    """Hilfsfunktion zum Erstellen von abgerundeten Buttons."""
    button = tk.Button(root, text=text, command=command, 
                       bg=kwargs.get('bg', '#2196F3'), fg=kwargs.get('fg', 'white'),
                       font=("Helvetica", 12), relief="flat", width=20, height=2, borderwidth=1, padx=10, pady=5)
    button.config(borderwidth=3, relief="solid")  # Abgerundete Ecken durch Solid Border
    return button

root = tk.Tk()
root.title('Vokabel-Trainer')
root.minsize(800, 600)
root.config(bg="#f4f4f4")

# Haupt-Frame
main_frame = tk.Frame(root, bg="#f4f4f4")
main_frame.pack(pady=30, padx=30, fill="both", expand=True)

# Überschrift
label = tk.Label(main_frame, text="Willkommen zum Vokabel-Trainer", font=("Helvetica", 26, "bold"), fg="#2196F3", bg="#f4f4f4")
label.pack(pady=20)

# Eingabefeld für neue Vokabeln
eingabe_feld = tk.Entry(main_frame, font=("Helvetica", 14), width=30, relief="solid", bd=2, fg="black", bg="#ffffff", insertbackground="black")
eingabe_feld.pack(pady=10)

# Ausgabe-Label
ausgabe_label = tk.Label(main_frame, text="", font=("Helvetica", 14), fg="black", bg="#f4f4f4")
ausgabe_label.pack(pady=10)

# Listen für Vokabeln und Lösungen
vokabeln_liste = tk.Frame(main_frame, bg="#f4f4f4")
vokabeln_liste.pack(pady=10, fill="both", expand=True)

lösungen_liste = tk.Frame(main_frame, bg="#f4f4f4")
lösungen_liste.pack(pady=10, fill="both", expand=True)

# Buttons
button_vokabeln = erstellen_button(main_frame, "Vokabeln hinzufügen", lambda: hinzufügen("Vokabeln"))
button_vokabeln.pack(pady=5)

button_lösungen = erstellen_button(main_frame, "Lösungen hinzufügen", lambda: hinzufügen("Lösungen"))
button_lösungen.pack(pady=5)

button_test = erstellen_button(main_frame, "Test starten", starten_test)
button_test.pack(pady=5)

button_leeren = erstellen_button(main_frame, "Listen leeren", listen_leeren)
button_leeren.pack(pady=5)

# Laden der gespeicherten Vokabeln und Lösungen
laden("Vokabeln")
laden("Lösungen")

# Footer
by_label = tk.Label(root, text="by: Ben", font=("Helvetica", 10), fg="gray", bg="#f4f4f4")
by_label.pack(side="bottom", anchor="se", padx=20, pady=10)

root.mainloop()
