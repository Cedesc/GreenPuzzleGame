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
    self.richtig_faerben()
    self.func = nothing

def richtig_fehlererkennung(self: Form) -> None:
    """ Feld korrekt faerben und level zuruecksetzen, falls Feld nochmal geklickt wird"""
    self.richtig_faerben()
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
    self.verbundeneFormen[0].richtig_faerben()
    self.zugehoerigesLevel.recFuncsAendern(level_zuruecksetzen)
    self.verbundeneFormen[0].func = funcL4

# Level 5
def funcL5(self: Form) -> None:
    """ Je nach Zustand des Levels wird ein anderes nebenstehendes Feld korrekt gefaerbt
    0: rechts, 1: unten, 2: links, 3: oben """
    levelZustand : int = self.zugehoerigesLevel.internerSpeicherL
    self.verbundeneFormen[levelZustand].umkehren()
    self.zugehoerigesLevel.internerSpeicherL = (levelZustand + 1) % 4

# Level 6
def funcL6(self: Form) -> None:
    """ Je nach Form (bzw internen Speicher) braucht es unterschiedlich viele Klicks, damit es korrekt gefaerbt wird
    Wird das mittlere Feld korrekt, so werden alle anderen auch korrekt gefaerbt """
    self.internerSpeicherF -= 1
    if self.internerSpeicherF < 1:
        self.richtig_faerben()
        self.klickbar = False
        self.sichtbar = False
        if self.nummer == 6:
            for rec in self.zugehoerigesLevel.rechtecke:
                rec.richtig_faerben()

# Level 7
def funcL7(self: Form) -> None:
    """ Faerben ist immer ein Klick verzoegert """
    naechstZuFaerbendes : int = self.zugehoerigesLevel.internerSpeicherL
    if naechstZuFaerbendes != -1:
        self.zugehoerigesLevel.rechtecke[naechstZuFaerbendes].umkehren()
    self.zugehoerigesLevel.internerSpeicherL = self.nummer

# Level 8
def funcL8_1(self: Form) -> None:
    """ Funktion fuer den ersten Knopf, der den Stempel bewegt """
    stempelPosition : int = self.zugehoerigesLevel.internerSpeicherL
    # Alte Position in falsche Farbe aendern, falls nicht gestempelt (anderer Knopf gedrueckt) wurde
    self.zugehoerigesLevel.rechtecke[stempelPosition].falsch_faerben()
    # Eine Position weiter
    self.zugehoerigesLevel.internerSpeicherL = (stempelPosition + 1) % 5
    # Jetzige Position des Stempels korrekt faerben
    self.zugehoerigesLevel.rechtecke[self.zugehoerigesLevel.internerSpeicherL].richtig_faerben()

def funcL8_2(self: Form) -> None:
    """ Funktion fuer den zweiten Knopf, der stempelt """
    stempelPosition : int = self.zugehoerigesLevel.internerSpeicherL
    if stempelPosition != -1:
        self.zugehoerigesLevel.rechtecke[stempelPosition].richtig_faerben()
        self.zugehoerigesLevel.internerSpeicherL = 0
        self.zugehoerigesLevel.rechtecke[0].richtig_faerben()

# Level 9
def funcL9(self: Form) -> None:
    """ verbundene Formen eine nach der anderen abarbeiten """
    self.verbundeneFormen[self.internerSpeicherF].richtig_faerben()
    self.internerSpeicherF += 1



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
    """ Beim anklicken eines Rechtecks wird ein anderes Rechteck korrekt gefaerbt. Wird dieses gefaerbte dann geklickt,
    wird ein anderes korrekt gefaerbt usw. Bei anklicken eines anderen Felds, wird das Level zurueckgesetzt """
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

def level5Erstellen(self) -> Levelstruktur:
    """ Je nach Zustand des Levels wird ein anderes nebenstehendes Feld korrekt gefaerbt
    in der Reihenfolge rechts, unten, links, oben """
    level = Levelstruktur(self)
    for y in range(5):
        for x in range(5):
            level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                self.wW / 16 + self.wW * (3 / 16) * x,
                                                self.wW / 16 + self.wW * (3 / 16) * y,
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL5))
    # verbundene Rechtecke zuweisen
    zuweisungsListe = [ [1, 5, 4, 20] , [2, 6, 0, 21] , [3, 7, 1, 22] , [4, 8, 2, 23] , [0, 9, 3, 24] ,
                        [6, 10, 9, 0] , [7, 11, 5, 1] , [8, 12, 6, 2] , [9, 13, 7, 3] , [5, 14, 8, 4] ,
                        [11, 15, 14, 5] , [12, 16, 10, 6] , [13, 17, 11, 7] , [14, 18, 12, 8] , [10, 19, 13, 9] ,
                        [16, 20, 19, 10] , [17, 21, 15, 11] , [18, 22, 16, 12] , [19, 23, 17, 13] , [15, 24, 18, 14] ,
                        [21, 0, 24, 15] , [22, 1, 20, 16] , [23, 2, 21, 17] , [24, 3, 22, 18] , [20, 4, 23, 19] ]
    level.recReferenzenHinzufuegen(25, zuweisungsListe)
    # internen Speicher des Levels festlegen
    level.internerSpeicherL = 0
    return level

def level6Erstellen(self) -> Levelstruktur:
    """ Je nach Feld, muss es unterschiedlich oft geklickt werden bis es korrekt gefaerbt wird
    Wird das letzte mittlere Feld korrekt gefaerbt, so werden alle anderen Felder auch gefaerbt
    Umliegende Felder sind nur zur Verwirrung da """
    level = Levelstruktur(self)
    for i in range(1, 8):
        level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),
                                            self.wW / 16 * i, self.wW / 16 * i,
                                            self.wW - self.wW / 8 * i, self.wW - self.wW / 8 * i,
                                            QColor(0, 90, 0), funcL6))
        level.rechtecke[-1].internerSpeicherF = int(i * 3/4)
    for y in range(5):
        for x in range(5):
            if not ((x, y) in [(1, 0), (3, 0), (0, 1), (0, 3), (4, 1), (4, 3), (1, 4), (3, 4)]):
                level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                    self.wW / 16 + self.wW * (3 / 16) * x,
                                                    self.wW / 16 + self.wW * (3 / 16) * y,
                                                    self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fertig))
    return level

def level7Erstellen(self) -> Levelstruktur:
    """ Das faerben ist immer um einen Klick verzoegert """
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(3):
            level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                                self.wW / 4 + self.wW * (3 / 16) * x,
                                                self.wW / 4.5 + self.wW * (3 / 16) * y,
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL7))
    # internen Speicher des Levels festlegen
    level.internerSpeicherL = -1
    return level

def level8Erstellen(self) -> Levelstruktur:
    """ 2 Knoepfe, der 1. ist dafuer da, den Stempel zu bewegen, der 2. zum stempeln. Bewegt sich der Stempel
    ueber ein schon gefaerbtes Feld hinweg, so wird das wieder falsch gefaerbt """
    level = Levelstruktur(self)
    for y in range(5):
        level.rechteck_hinzufuegen(Rechteck(len(level.rechtecke),  # spiegelt Index in der Liste wieder
                                            0,
                                            self.wW / 5 * y,
                                            self.wW, self.wW / 5, QColor(0, 90, 0), nothing))
    level.kreis_hinzufuegen(Kreis(len(level.kreise),
                                  self.wW / 10,
                                  self.wW / 5,
                                  self.wW / 8, self.wW / 8, QColor(0, 180, 0), funcL8_1))
    level.kreis_hinzufuegen(Kreis(len(level.kreise),
                                  self.wW / 10,
                                  self.wW * 3 / 8,
                                  self.wW / 8, self.wW / 8, QColor(0, 180, 0), funcL8_2))
    level.internerSpeicherL = -1
    return level

def level9Erstellen(self) -> Levelstruktur:
    """ Nur ein Feld ist relevant. Klickt man mehrmals darauf wird das Level Stueck fuer Stueck richtig gefaerbt """
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(4):
            verschiebungNachOben : int = 0
            if x % 2 == 0:
                verschiebungNachOben = self.wW / 12
            level.kreis_hinzufuegen(Kreis(len(level.kreise),  # spiegelt Index in der Liste wieder
                                          self.wW / 16 + self.wW / 4 * x,
                                          self.wW / 8 + verschiebungNachOben + self.wW / 4 * y,
                                          self.wW / 8, self.wW / 8, QColor(0, 90, 0), level_zuruecksetzen))
    # Bei einem (willkuerlich gewaehltem) Kreis die Funktion einbauen
    level.kreise[9].func = funcL9
    level.kreise[9].verbundeneFormen = [level.kreise[3], level.kreise[8], level.kreise[5], level.kreise[6],
                                        level.kreise[11], level.kreise[0], level.kreise[1], level.kreise[4],
                                        level.kreise[10], level.kreise[2], level.kreise[7], level.kreise[9]]
    level.kreise[9].internerSpeicherF = 0
    return level
