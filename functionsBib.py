from classes import Levelstruktur, Form, Rechteck, Kreis, QColor, List
""" Bibliothek fuer Funktionen der Formen und Levelerstellung """


# Funktionen fuer Rechtecke und Kreise
                # Aufpassen, wenn man nach der Zeile "level_zuruecksetzen(self)" noch was schreiben will.
                # Wird im allgemeinen nicht funktionieren, da dadurch ein komplett neues Level erstellt wird und
                # die Referenzen dann veraltet sind

def nothing(self: Form) -> None:
    """ Wenn draufgeklickt wird, soll nichts ausgefuehrt werden """
    return

def level_zuruecksetzen(self: Form) -> None:
    """ Falls zB ein Fehler gemacht wurde, wird das Level zurueckgesetzt """
    self.zugehoerigesLevel.zugehoerigesFenster.levelReset()

def richtig_fertig(self: Form) -> None:
    """ Feld korrekt faerben und keine weitere eingabe darauf ermoeglichen """
    self.gruen_machen()
    self.func = nothing

def richtig_fehlererkennung(self: Form) -> None:
    """ Feld korrekt faerben und level zuruecksetzen, falls Feld nochmal geklickt wird"""
    self.gruen_machen()
    self.func = level_zuruecksetzen

# Level 3
def verbundeneAendern(self: Form) -> None:
    """ Alle verbundenen Formen umkehren """
    for verForm in self.verbundeneFormen:
        verForm.umkehren()

# Level 4
def funcL4(self: Form) -> None:
    """ Eine andere Form (einzig verbundene) wird korrekt gefaerbt,
    alle Formen bekommen die Funktion 'level_zuruecksetzen' ausser der gefaerbten """
    self.verbundeneFormen[0].gruen_machen()
    self.zugehoerigesLevel.recFuncsAendern(level_zuruecksetzen)
    self.verbundeneFormen[0].func = funcL4


# Funktionen für die Levelerstellung
# Koordinaten sollten keine genauen Zahlen sein, sondern immer in Abhaengigkeit der Fenstergroesse

def level0Erstellen(self) -> Levelstruktur:
    level = Levelstruktur(self)
    for y in range(2):
        for x in range(3):
            level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                self.wW / 16 + self.wW * (3 / 16) * x,
                                                self.wW / 16 + self.wW * (3 / 16) * y,
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fertig))
    return level

def level1Erstellen(self) -> Levelstruktur:
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(1):
            level.kreis_hinzufuegen(Kreis(len(level.kreise),  # spiegelt Index in der Liste wieder
                                          self.wW / 16 + self.wW * (3 / 16) * x,
                                          self.wW / 16 + self.wW * (3 / 16) * y,
                                          self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fehlererkennung))
    return level

def level2Erstellen(self) -> Levelstruktur:
    level = Levelstruktur(self)
    for y in range(2):
        for x in range(1):
            level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                self.wW / 16 + self.wW * (3 / 16) * (x + 2),
                                                self.wW / 12 + self.wW * (3 / 16) * (y + 2),
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fehlererkennung))
    return level

def level3Erstellen(self) -> Levelstruktur:
    """ Bei anklicken eines Rechtecks werden alle umliegenden Rechtecke geaendert """
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(4):
            level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                self.wW / 6.4 + self.wW * (3 / 16) * x,
                                                self.wW / 5 + self.wW * (3 / 16) * y,
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), verbundeneAendern))
    # verbundene Rechtecke zuweisen
    zuweisungsListe = [ [1, 4, 5] , [0, 2, 4, 5, 6] , [1, 3, 5, 6, 7] , [2, 6, 7] ,
              [0, 1, 5, 8, 9] , [0, 1, 2, 4, 6, 8, 9, 10] , [1, 2, 3, 5, 7, 9, 10, 11] , [2, 3, 6, 10, 11] ,
              [4, 5, 9] , [4, 5, 6, 8, 10] , [5, 6, 7, 9, 11] , [6, 7, 10] ]
    level.recReferenzenHinzufuegen(12, zuweisungsListe)
    return level

def level4Erstellen(self) -> Levelstruktur:
    """ """
    level = Levelstruktur(self)
    for y in range(4):
        for x in range(4):
            level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                self.wW / 6.4 + self.wW * (3 / 16) * x,
                                                self.wW / 6.4 + self.wW * (3 / 16) * y,
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL4))
    # verbundene Rechtecke zuweisen
    zuweisungsListe = [ [15], [14], [3], [12], [13], [8], [11], [9],
                        [2],  [1],  [0], [10], [7],  [5], [6],  [4] ]
    level.recReferenzenHinzufuegen(16, zuweisungsListe)
    return level

