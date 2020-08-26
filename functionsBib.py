from classes import Levelstruktur, Form, Rechteck, Kreis, QColor, List, Callable
""" Bibliothek fuer Funktionen der Formen und Levelerstellung """


# Funktionen fuer Rechtecke und Kreise
                # Aufpassen, wenn man nach der Zeile "level_zuruecksetzen(self)" noch was schreiben will.
                # Wird im allgemeinen nicht funktionieren, da dadurch ein komplett neues Level erstellt wird und
                # die Referenzen dann veraltet sind

def nothing(self) -> None:
    """ Wenn draufgeklickt wird, soll nichts ausgefuehrt werden """
    return

def level_zuruecksetzen(self) -> None:
    """ Falls zB ein Fehler gemacht wurde, wird das Level zurueckgesetzt """
    self.zugehoerigesLevel.zugehoerigesFenster.levelReset()

def richtig_fertig(self) -> None:
    """ Feld korrekt faerben und keine weitere eingabe darauf ermoeglichen """
    self.gruen_machen()
    self.func = nothing

def richtig_fehlererkennung(self) -> None:
    """ Feld korrekt faerben und level zuruecksetzen, falls Feld nochmal geklickt wird"""
    self.gruen_machen()
    self.func = level_zuruecksetzen

def anderesRichtigUndAendern(self: Form) -> None:
    for verForm in self.verbundeneFormen:
        verForm.umkehren()



# Funktionen für die Levelerstellung
# Koordinaten sollten keine genauen Zahlen sein, sondern immer in Abhaengigkeit der Fenstergroesse

def level0Erstellen(self) -> Levelstruktur:
    level = Levelstruktur(self)
    for x in range(2):
        for y in range(3):
            level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                self.wW / 16 + self.wW * (3 / 16) * x,
                                                self.wW / 16 + self.wW * (3 / 16) * y,
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fertig))
    return level

def level1Erstellen(self) -> Levelstruktur:
    level = Levelstruktur(self)
    for x in range(3):
        for y in range(1):
            level.kreis_hinzufuegen(Kreis(len(level.kreise),  # spiegelt Index in der Liste wieder
                                          self.wW / 16 + self.wW * (3 / 16) * x,
                                          self.wW / 16 + self.wW * (3 / 16) * y,
                                          self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fehlererkennung))
    return level

def level2Erstellen(self) -> Levelstruktur:
    level = Levelstruktur(self)
    for x in range(2):
        for y in range(1):
            level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                self.wW / 16 + self.wW * (3 / 16) * (x + 2),
                                                self.wW / 12 + self.wW * (3 / 16) * (y + 2),
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fehlererkennung))
    return level

def level3Erstellen(self) -> Levelstruktur:
    level = Levelstruktur(self)
    for x in range(3):
        for y in range(4):
            level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                self.wW / 16 + self.wW * (3 / 16) * x,
                                                self.wW / 16 + self.wW * (3 / 16) * y,
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), anderesRichtigUndAendern))

    level.rechtecke[0].verbundeneFormen.append(level.rechtecke[1])
    level.rechtecke[0].verbundeneFormen.append(level.rechtecke[2])

    level.rechtecke[1].verbundeneFormen.append(level.rechtecke[2])
    level.rechtecke[2].verbundeneFormen.append(level.rechtecke[3])
    level.rechtecke[3].verbundeneFormen.append(level.rechtecke[4])
    level.rechtecke[4].verbundeneFormen.append(level.rechtecke[5])
    level.rechtecke[5].verbundeneFormen.append(level.rechtecke[6])
    level.rechtecke[6].verbundeneFormen.append(level.rechtecke[7])
    level.rechtecke[7].verbundeneFormen.append(level.rechtecke[8])
    level.rechtecke[8].verbundeneFormen.append(level.rechtecke[9])
    level.rechtecke[9].verbundeneFormen.append(level.rechtecke[10])
    level.rechtecke[10].verbundeneFormen.append(level.rechtecke[11])
    level.rechtecke[11].verbundeneFormen.append(level.rechtecke[0])
    return level

