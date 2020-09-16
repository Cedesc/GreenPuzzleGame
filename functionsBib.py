from classes import Levelstruktur, Form, Rechteck, Kreis, Polygon, QColor, List
from random import randint
from PyQt5.QtGui import QPainter, QPen, QPolygon, QFont
from PyQt5.QtCore import Qt, QRect
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

def farbe_umkehren(self: Form) -> None:
    """ Feld korrekt faerben, falls es falsch gefaerbt ist und falsch faerben, falls es korrekt gefaerbt ist """
    self.umkehren()

# Level 3
def verbundeneAendern(self: Form) -> None:
    """ Alle verbundenen Formen umkehren """
    for verForm in self.verbundeneFormen:
        verForm.umkehren_ohneAufleuchten()

# Level 4
def funcL4(self: Form) -> None:
    """ Eine andere Form (einzig verbundene) wird korrekt gefaerbt,
    alle Formen bekommen die Funktion 'level_zuruecksetzen' ausser der gefaerbten """
    self.verbundeneFormen[0].richtig_faerben()
    self.zugehoerigesLevel.formFuncsAendern(level_zuruecksetzen)
    self.verbundeneFormen[0].func = funcL4

# Level 5
def funcL5(self: Form) -> None:
    """ Je nach Zustand des Levels wird ein anderes nebenstehendes Feld korrekt gefaerbt
    0: rechts, 1: unten, 2: links, 3: oben """
    levelZustand : int = self.zugehoerigesLevel.internerSpeicherL
    self.verbundeneFormen[levelZustand].umkehren()
    # Zustand zum naechsten aendern
    self.zugehoerigesLevel.internerSpeicherL = (levelZustand + 1) % 4

# Level 6
def funcL6(self: Form) -> None:
    """ Je nach Form (bzw internen Speicher) braucht es unterschiedlich viele Klicks, damit es korrekt gefaerbt wird
    Wird das kleinste mittlere Feld korrekt gefaerbt, so werden alle anderen auch korrekt gefaerbt """
    # Anzahl noetige Klicks um 1 verringern
    self.internerSpeicherF -= 1
    # pruefen ob keine Klicks mehr noetig
    if self.internerSpeicherF < 1:
        # falls keine klicks mehr noetig, verschwindet das Rechteck
        self.klickbar = False
        self.sichtbar = False
        # falls das kleinste mittlere Rechteck keine Klicks mehr benoetigt, werden alle Rechtecke korrekt gefaerbt
        if self.nummer == 6:
            self.zugehoerigesLevel.alleRichtigFaerben()

# Level 7
def funcL7(self: Form) -> None:
    """ Wenn geklickt wird, wird das zuvor geklickte korrekt gefaerbt """
    naechstZuFaerbendes : int = self.zugehoerigesLevel.internerSpeicherL
    # pruefen ob zuvor ein Feld geklickt wurde
    if naechstZuFaerbendes != -1:
        # falls ja, wird das zuvor geklickte korrekt gefaerbt
        self.zugehoerigesLevel.enthalteneFormen[naechstZuFaerbendes].umkehren()
    # momentan geklicktes Feld fuer naechsten Klick merken
    self.zugehoerigesLevel.internerSpeicherL = self.nummer

# Level 8
def funcL8_1(self: Form) -> None:
    """ Funktion fuer den ersten Knopf, der den Stempel bewegt """
    self.aufleuchten = True
    stempelPosition : int = self.zugehoerigesLevel.internerSpeicherL
    # Alte Position in falsche Farbe aendern
    if stempelPosition != -1:
        self.zugehoerigesLevel.enthalteneFormen[stempelPosition].falsch_faerben()
    # Eine Position weiter
    self.zugehoerigesLevel.internerSpeicherL = (stempelPosition + 1) % 5
    # Jetzige Position des Stempels korrekt faerben
    self.zugehoerigesLevel.enthalteneFormen[self.zugehoerigesLevel.internerSpeicherL].richtig_faerben()

def funcL8_2(self: Form) -> None:
    """ Funktion fuer den zweiten Knopf, der das momentane Feld korrekt gefaerbt laesst und den Stempel
    wieder nach oben bewegt """
    self.aufleuchten = True
    stempelPosition : int = self.zugehoerigesLevel.internerSpeicherL
    # pruefen ob der erste Knopf ueberhaupt schon gedrueckt wurde
    if stempelPosition != -1:
        # Stempel wird wieder nach oben gesetzt
        self.zugehoerigesLevel.internerSpeicherL = 0
        self.zugehoerigesLevel.enthalteneFormen[0].richtig_faerben()

# Level 9
def funcL9(self: Form) -> None:
    """ verbundene Formen eine nach der anderen abarbeiten """
    self.verbundeneFormen[self.internerSpeicherF].richtig_faerben()
    self.internerSpeicherF += 1

# Level 10
def funcL10(self: Form) -> None:
    """ Aeussere Felder steuern die inneren: Rechts nach rechts, unten nach unten, usw """
    position = self.zugehoerigesLevel.internerSpeicherL
    # nach rechts
    if self.internerSpeicherF == 0 and position[0] + 1 <= 2:
        position[0] += 1
    # nach unten
    elif self.internerSpeicherF == 1 and position[1] + 1 <= 2:
        position[1] += 1
    # nach links
    elif self.internerSpeicherF == 2 and 0 <= position[0] - 1:
        position[0] -= 1
    # nach oben
    elif self.internerSpeicherF == 3 and 0 <= position[1] - 1:
        position[1] -= 1
    # jetzige Position faerben
    self.zugehoerigesLevel.enthalteneFormen[position[0] + position[1] * 3].richtig_faerben()
    # falls alle in der Mitte korrekt gefaerbt wurden, werden die aussenstehenden auch korrekt gefaerbt
    for i in self.zugehoerigesLevel.enthalteneFormen[:9]:
        if i.farbe != QColor(0, 180, 0):
            return
    self.zugehoerigesLevel.alleRichtigFaerben()

# Level 11
def funcL11(self: Form) -> None:
    """ Verbundene Form umkehren """
    self.verbundeneFormen[0].umkehren()

# Level 12
def funcL12_1(self: Form) -> None:
    """ Funktion fuer den ersten Knopf, der den unsichtbaren Stempel bewegt """
    self.aufleuchten = True
    # Eine Position weiter
    self.zugehoerigesLevel.internerSpeicherL += 1

def funcL12_2(self: Form) -> None:
    """ Funktion fuer den zweiten Knopf, der unterm Stempel umkehrt """
    self.aufleuchten = True
    stempelPosition : int = self.zugehoerigesLevel.internerSpeicherL
    # pruefen ob erster Knopf nicht oder ueber 3 mal gedrueckt wurde (also ob auf Feld oder ausserhalb)
    if stempelPosition != -1 and stempelPosition < 4:
        self.zugehoerigesLevel.enthalteneFormen[stempelPosition].umkehren()
    self.zugehoerigesLevel.internerSpeicherL = -1

# Level 13
def funcL13(self: Form) -> None:
    """ Wenn auf das richtige Feld geklickt wurde, wird zufaellig das naechste bestimmt und die Dreiecke
    entsprechend ausgerichtet """
    self.richtig_faerben()
    # erneutes klicken auf das (nun gefaerbtes) Feld waere ein Fehler
    self.func = level_zuruecksetzen
    # naechstes Feld zufaellig bestimmen
    naechstesFeld = randint(5, 8)
    # so lange das neu zufaellig ausgewaehlte Feld ein bereits gedruecktes ist, wird ein neues zufaelliges bestimmt
    while self.zugehoerigesLevel.enthalteneFormen[naechstesFeld].farbe == QColor(0, 180, 0):
        naechstesFeld = randint(5, 8)
        # sind jedoch alle Felder bereits richtig gefaerbt, wird das Level abgeschlossen (ineffizient, aber ok)
        anzahlRichtigeFelder = 0
        for i in range(4):
            if self.zugehoerigesLevel.enthalteneFormen[i + 5].farbe == QColor(0, 180, 0):
                anzahlRichtigeFelder += 1
        if anzahlRichtigeFelder == 4:
            self.zugehoerigesLevel.alleRichtigFaerben()
            return
    # wenn naechstes Feld gefunden wurde, wird diesem die Funktion neu zugeordnet und die Dreiecke werden ausgerichtet
    self.zugehoerigesLevel.enthalteneFormen[naechstesFeld].func = funcL13
    for dreieckIndex in range(5):
        self.zugehoerigesLevel.enthalteneFormen[dreieckIndex].rotation = \
            self.zugehoerigesLevel.internerSpeicherL[naechstesFeld - 5][dreieckIndex]

# Level 14
def funcL14_1(self: Form) -> None:
    """ Zustand zu 0, also 'links-und-mitte-drehen' aendern """
    self.aufleuchten = True
    self.zugehoerigesLevel.internerSpeicherL[2] = 0

def funcL14_2(self: Form) -> None:
    """ Zustand zu 1, also 'alle-drehen' aendern """
    self.aufleuchten = True
    self.zugehoerigesLevel.internerSpeicherL[2] = 1

def funcL14_3(self: Form) -> None:
    """ Zustand zu 2, also 'mitte-und-links-drehen' aendern """
    self.aufleuchten = True
    self.zugehoerigesLevel.internerSpeicherL[2] = 2

def funcL14_1Level(self: Levelstruktur) -> None:
    """ nach links drehen """
    # je nach Zustand werden andere Formen gedreht
    if self.internerSpeicherL[2] == 0:
        self.enthalteneFormen[6].rotation -= 3
        self.enthalteneFormen[7].rotation -= 3
    elif self.internerSpeicherL[2] == 1:
        self.enthalteneFormen[6].rotation -= 3
        self.enthalteneFormen[7].rotation -= 3
        self.enthalteneFormen[8].rotation -= 3
    elif self.internerSpeicherL[2] == 2:
        self.enthalteneFormen[7].rotation -= 3
        self.enthalteneFormen[8].rotation -= 3

    # pruefen ob alle richtig gedreht
    if self.enthalteneFormen[6].rotation % 360 == 45 \
            and self.enthalteneFormen[7].rotation % 360 == 180 \
            and self.enthalteneFormen[8].rotation % 360 == 315:
        self.alleRichtigFaerben()
        # manuell Level als gewonnen kennzeichnen ist noetig, da 'beruehrt' von 'Levelstruktur' nicht aufgerufen wird
        self.zugehoerigesFenster.levelGewonnen = True

def funcL14_2Level(self: Levelstruktur) -> None:
    """ nach rechts drehen """
    # je nach Zustand werden andere Formen gedreht
    if self.internerSpeicherL[2] == 0:
        self.enthalteneFormen[6].rotation += 3
        self.enthalteneFormen[7].rotation += 3
    elif self.internerSpeicherL[2] == 1:
        self.enthalteneFormen[6].rotation += 3
        self.enthalteneFormen[7].rotation += 3
        self.enthalteneFormen[8].rotation += 3
    elif self.internerSpeicherL[2] == 2:
        self.enthalteneFormen[7].rotation += 3
        self.enthalteneFormen[8].rotation += 3

    # pruefen ob alle richtig gedreht
    if self.enthalteneFormen[6].rotation % 360 == 45 \
            and self.enthalteneFormen[7].rotation % 360 == 180 \
            and self.enthalteneFormen[8].rotation % 360 == 315:
        self.alleRichtigFaerben()
        # manuell Level als gewonnen kennzeichnen ist noetig, da 'beruehrt' von 'Levelstruktur' nicht aufgerufen wird
        self.zugehoerigesFenster.levelGewonnen = True

def funcL14WeiteresZeichnen(painterF: QPainter, win) -> None:
    # Steuerungshinweis im Level
    rect1 = QRect(0, int(win.wW * 8 / 10), win.wW, int(win.wW / 10))
    painterF.setPen(QPen(QColor(0, 40, 0), 1, Qt.SolidLine))
    painterF.setFont(QFont("Times", int(win.wW / 42)))
    painterF.drawText(rect1, 4, str("Y: nach links drehen\n   X: nach Rechts drehen"))

    # 'Hinweise' von Rechtecken zu Formen
    painterF.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
    painterF.drawLine(win.wW * 150 / 800, win.wW * 250 / 800, win.wW * 150 / 800, win.wW * 315 / 800)
    painterF.drawLine(win.wW * 150 / 800, win.wW * 250 / 800, win.wW * 200 / 800, win.wW * 300 / 800)
    painterF.drawLine(win.wW * 400 / 800, win.wW * 250 / 800, win.wW * 350 / 800, win.wW * 300 / 800)
    painterF.drawLine(win.wW * 400 / 800, win.wW * 250 / 800, win.wW * 400 / 800, win.wW * 315 / 800)
    painterF.drawLine(win.wW * 400 / 800, win.wW * 250 / 800, win.wW * 450 / 800, win.wW * 300 / 800)
    painterF.drawLine(win.wW * 650 / 800, win.wW * 250 / 800, win.wW * 600 / 800, win.wW * 300 / 800)
    painterF.drawLine(win.wW * 650 / 800, win.wW * 250 / 800, win.wW * 650 / 800, win.wW * 315 / 800)

# Level 15
def funcL15(self: Form, xKlick: int, yKlick: int) -> None:
    """ testet, je nach Zustand, ob der Klick rechts/links oder ueber/unter dem vorherigen Klick ist """
    momentanesLevel : Levelstruktur = self.zugehoerigesLevel
    # Wenn erster Klick ist relative Position nicht wichtig und wird nur fuer naechsten Klick gespeichert
    if self.internerSpeicherF == (-1, -1):
        self.internerSpeicherF = (xKlick, yKlick)
        self.richtig_faerben_ohneAufleuchten()
        return

    vorgabe : tuple = momentanesLevel.internerSpeicherL[0]
    zustand : int = momentanesLevel.internerSpeicherL[1]
    richtigGeklickt : bool = False

    # Soll rechts davon sein
    if vorgabe[zustand] == 0:
        if xKlick > self.internerSpeicherF[0]:
            richtigGeklickt = True
    # Soll drunter sein
    elif vorgabe[zustand] == 1:
        if yKlick > self.internerSpeicherF[1]:
            richtigGeklickt = True
    # Soll links davon sein
    elif vorgabe[zustand] == 2:
        if xKlick < self.internerSpeicherF[0]:
            richtigGeklickt = True
    # Soll drueber sein
    elif vorgabe[zustand] == 3:
        if yKlick < self.internerSpeicherF[1]:
            richtigGeklickt = True

    # wenn die relative Position richtig ist, wird der Klick gespeichert und der Zustand wechselt in den naechsten
    if richtigGeklickt:
        self.internerSpeicherF = (xKlick, yKlick)
        self.zugehoerigesLevel.internerSpeicherL[1] += 1
        self.zugehoerigesLevel.enthalteneFormen[self.zugehoerigesLevel.internerSpeicherL[1]].richtig_faerben()
        # abgeschlossen, wenn der vorgesehene Ablauf komplett durchgelaufen ist
        if momentanesLevel.internerSpeicherL[1] == 10:
            momentanesLevel.alleRichtigFaerben()
    # wenn nicht, wird das Level zurueckgesetzt
    else:
        self.zugehoerigesLevel.zugehoerigesFenster.levelReset()

# Level 16
def funcL16(self: Form) -> None:
    """ Verbundene Form umkehren """
    self.verbundeneFormen[0].umkehren()

# Level 17
def funcL17(self: Form) -> None:
    """ Eine andere Form (einzig verbundene) wird korrekt gefaerbt,
    alle Formen bekommen die Funktion 'level_zuruecksetzen' ausser der naechst-vorgesehenen """
    self.richtig_faerben()
    self.zugehoerigesLevel.formFuncsAendern(level_zuruecksetzen)
    self.verbundeneFormen[0].func = funcL17
    # Pruefen ob, bis auf die Polygone, alles korrekt gefaerbt ist
    formen : List[Form] = self.zugehoerigesLevel.enthalteneFormen
    for i in range(12):
        if formen[i].farbe != QColor(0, 180, 0):
            return
    self.zugehoerigesLevel.alleRichtigFaerben()

# Level 18
def funcL18(self: Form) -> None:
    """ je nach dem ob man den linken oder rechten Knopf drueckt, wird getestet, ob der richtige gedrueckt wurde """
    # level.internerSpeicherL = [(1, 0, 1, 1, 1, 0, 0), 0]
    vorgesehenerAblauf = self.zugehoerigesLevel.internerSpeicherL[0]
    zustandsPointer = self.zugehoerigesLevel.internerSpeicherL[1]
    # pruefen ob das korrekte geklickt wurde
    if vorgesehenerAblauf[zustandsPointer] == self.internerSpeicherF:
        pass
    # falls die falsche Seite geklickt wurde
    else:
        pass

def funcL18WeiteresZeichnen(painterF: QPainter, win) -> None:
    """ Form, die aus einer Linie besteht, zeichnen und Pfeil fuer den Anfang """
    # Fenstergroesse
    wW : int = win.wW
    # mittige Form
    painterF.setPen(QPen(QColor(0, 0, 0), wW / 80, Qt.SolidLine))
    painterF.drawPolyline(QPolygon([wW / 8, wW * 5 / 8, wW * 65 / 80, wW * 3 / 8,
                                    wW * 55 / 80, wW / 8, wW * 25 / 80, wW / 8,
                                    wW * 15 / 80, wW * 3 / 8, wW * 7 / 8, wW * 5 / 8]))
    # Anfangspfeil
    painterF.setPen(QPen(QColor(0, 0, 0), wW / 200, Qt.SolidLine))
    painterF.drawPolygon(QPolygon([wW * 7 / 80, wW * 57 / 80, wW / 8, wW * 52 / 80,
                                   wW * 13 / 80, wW * 57/ 80, wW * 11 / 80, wW * 57 / 80,
                                   wW * 11 / 80, wW * 59 / 80, wW * 9 / 80, wW * 59 / 80,
                                   wW * 9 / 80, wW * 57 / 80]))


# Funktionen für die Levelerstellung
# Koordinaten sollten keine genauen Zahlen sein, sondern immer in Abhaengigkeit der Fenstergroesse

def level0Erstellen(self) -> Levelstruktur:
    """ Testlevel """
    level = Levelstruktur(self)
    for y in range(2):
        for x in range(3):
            level.form_hinzufuegen(Rechteck(self.wW / 16 + self.wW * (3 / 16) * x,
                                            self.wW / 16 + self.wW * (3 / 16) * y,
                                            self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fertig))
    return level

def level1Erstellen(self) -> Levelstruktur:
    """ Testlevel """
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(1):
            level.form_hinzufuegen(Kreis(self.wW / 16 + self.wW * (3 / 16) * x,
                                         self.wW / 16 + self.wW * (3 / 16) * y,
                                         self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fehlererkennung))
    return level

def level2Erstellen(self) -> Levelstruktur:
    """ Testlevel """
    level = Levelstruktur(self)
    for y in range(2):
        for x in range(1):
            level.form_hinzufuegen(Rechteck(self.wW / 16 + self.wW * (3 / 16) * (x + 2),
                                            self.wW / 12 + self.wW * (3 / 16) * (y + 2),
                                            self.wW / 8, self.wW / 8, QColor(0, 90, 0), richtig_fehlererkennung))
    return level

def level3Erstellen(self) -> Levelstruktur:
    """ Bei anklicken eines Rechtecks werden alle umliegenden Rechtecke geaendert """
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(4):
            level.form_hinzufuegen(Rechteck(self.wW / 6.4 + self.wW * (3 / 16) * x,
                                            self.wW / 5 + self.wW * (3 / 16) * y,
                                            self.wW / 8, self.wW / 8, QColor(0, 90, 0), verbundeneAendern))
    # verbundene Rechtecke zuweisen (je alle drumherum)
    zuweisungsListe = [ [1, 4, 5] , [0, 2, 4, 5, 6] , [1, 3, 5, 6, 7] , [2, 6, 7] ,
              [0, 1, 5, 8, 9] , [0, 1, 2, 4, 6, 8, 9, 10] , [1, 2, 3, 5, 7, 9, 10, 11] , [2, 3, 6, 10, 11] ,
              [4, 5, 9] , [4, 5, 6, 8, 10] , [5, 6, 7, 9, 11] , [6, 7, 10] ]
    level.formReferenzenHinzufuegen(zuweisungsListe)
    return level

def level4Erstellen(self) -> Levelstruktur:
    """ Beim anklicken eines Rechtecks wird ein anderes Rechteck korrekt gefaerbt. Wird dieses gefaerbte dann geklickt,
    wird ein anderes korrekt gefaerbt usw. Bei anklicken eines anderen Felds, wird das Level zurueckgesetzt. """
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(3):
            level.form_hinzufuegen(Rechteck(self.wW / 8 + self.wW * (5 / 16) * x,
                                            self.wW / 8 + self.wW * (5 / 16) * y,
                                            self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL4))
    # verbundene Rechtecke zuweisen (soll letztlich ein Durchlauf am Stueck sein)
    level.formReferenzenHinzufuegen([ [4], [6], [3], [7], [5], [8], [0], [1], [2] ])
    return level

def level5Erstellen(self) -> Levelstruktur:
    """ Je nach Zustand des Levels wird ein anderes nebenstehendes Feld korrekt gefaerbt
    in der Reihenfolge rechts, unten, links, oben und dann wieder von vorn """
    level = Levelstruktur(self)
    for y in range(5):
        for x in range(5):
            level.form_hinzufuegen(Rechteck(self.wW / 16 + self.wW * (3 / 16) * x,
                                            self.wW / 16 + self.wW * (3 / 16) * y,
                                            self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL5))
    # verbundene Rechtecke zuweisen (je rechts, unten, links, oben)
    zuweisungsListe = [ [1 , 5 , 4 , 20] , [2 , 6 , 0 , 21] , [3 , 7 , 1 , 22] , [4 , 8 , 2 , 23] , [0 , 9 , 3 , 24],
                        [6 , 10, 9 , 0 ] , [7 , 11, 5 , 1 ] , [8 , 12, 6 , 2 ] , [9 , 13, 7 , 3 ] , [5 , 14, 8 , 4 ],
                        [11, 15, 14, 5 ] , [12, 16, 10, 6 ] , [13, 17, 11, 7 ] , [14, 18, 12, 8 ] , [10, 19, 13, 9 ],
                        [16, 20, 19, 10] , [17, 21, 15, 11] , [18, 22, 16, 12] , [19, 23, 17, 13] , [15, 24, 18, 14],
                        [21, 0 , 24, 15] , [22, 1 , 20, 16] , [23, 2 , 21, 17] , [24, 3 , 22, 18] , [20, 4 , 23, 19] ]
    level.formReferenzenHinzufuegen(zuweisungsListe)
    # internen Speicher des Levels festlegen
    level.internerSpeicherL = 0
    return level

def level6Erstellen(self) -> Levelstruktur:
    """ Je nach Feld, muss es unterschiedlich oft geklickt werden bis es korrekt gefaerbt wird
    Wird das letzte mittlere Feld korrekt gefaerbt, so werden alle anderen Felder auch gefaerbt
    Umliegende Felder sind nur zur Verwirrung da """
    level = Levelstruktur(self)
    # von grossem zu kleinem Feld, welche unterschiedlich oft geklickt werden muessen
    for i in range(1, 8):
        level.form_hinzufuegen(Rechteck(self.wW / 16 * i, self.wW / 16 * i,
                                        self.wW - self.wW / 8 * i, self.wW - self.wW / 8 * i,
                                        QColor(0, 90, 0), funcL6))
        # Anzahl an noetigen Klicks auf eine Form festlegen (je kleiner / spaeter, desto mehr)
        level.enthalteneFormen[-1].internerSpeicherF = int(i * 3 / 4)
    # umliegende Felder zur Verwirrung
    for y in range(5):
        for x in range(5):
            if not ((x, y) in [(1, 0), (3, 0), (0, 1), (0, 3), (4, 1), (4, 3), (1, 4), (3, 4)]):
                level.form_hinzufuegen(Rechteck(self.wW / 16 + self.wW * (3 / 16) * x,
                                                self.wW / 16 + self.wW * (3 / 16) * y,
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), farbe_umkehren))
    return level

def level7Erstellen(self) -> Levelstruktur:
    """ Das faerben ist immer um einen Klick verzoegert """
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(3):
            level.form_hinzufuegen(Kreis(self.wW / 4 + self.wW * (3 / 16) * x,
                                            self.wW / 4.5 + self.wW * (3 / 16) * y,
                                            self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL7))
    # internen Speicher des Levels mit einem Platzhalter fuellen
    level.internerSpeicherL = -1
    return level

def level8Erstellen(self) -> Levelstruktur:
    """ 2 Knoepfe, der 1. ist dafuer da, den Stempel zu bewegen, der 2. zum stempeln. Bewegt sich der Stempel
    ueber ein schon gefaerbtes Feld hinweg, so wird dieses wieder falsch gefaerbt """
    level = Levelstruktur(self)
    for y in range(5):
        level.form_hinzufuegen(Rechteck(0, self.wW / 5 * y, self.wW, self.wW / 5, QColor(0, 90, 0), nothing))
        # gerade hinzugefuegtes Rechteck nicht-klickbar machen
        level.enthalteneFormen[-1].klickbar = False
    # Knoepfe hinzufuegen
    level.form_hinzufuegen(Kreis(self.wW / 10,
                                 self.wW * 4 / 25,
                                 self.wW / 8, self.wW / 8, QColor(0, 180, 0), funcL8_1))
    level.form_hinzufuegen(Kreis(self.wW / 10,
                                 self.wW * 1 / 3,
                                 self.wW / 8, self.wW / 8, QColor(0, 180, 0), funcL8_2))
    # internen Speicher des Levels mit Platzhalter fuellen
    level.internerSpeicherL = -1
    return level

def level9Erstellen(self) -> Levelstruktur:
    """ Nur ein Feld ist relevant. Klickt man mehrmals darauf wird das Level Feld fuer Feld richtig gefaerbt """
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(4):
            verschiebungNachOben : int = 0
            # zweite und vierte Spalte leicht nach oben verschieben
            if x % 2 == 0:
                verschiebungNachOben = self.wW / 12
            level.form_hinzufuegen(Kreis(self.wW / 16 + self.wW / 4 * x,
                                         self.wW / 8 + verschiebungNachOben + self.wW / 4 * y,
                                         self.wW / 8, self.wW / 8, QColor(0, 90, 0), level_zuruecksetzen))
    # bei einem (willkuerlich gewaehltem, aber nicht zufaelligem) Kreis die Funktion einbauen
    level.enthalteneFormen[9].func = funcL9
    # bei gleichem Kreis jedes andere Feld zuordnen
    kreise: List[Form] = level.enthalteneFormen
    level.enthalteneFormen[9].verbundeneFormen = [ kreise[3], kreise[8], kreise[5], kreise[6], kreise[11], kreise[0],
                                                   kreise[1], kreise[4], kreise[10], kreise[2], kreise[7], kreise[9]]
    # Speicher soll als Index auf den jetzt naechst relevanten Kreis dienen
    level.enthalteneFormen[9].internerSpeicherF = 0
    return level

def level10Erstellen(self) -> Levelstruktur:
    """ Nebenstehende Felder vorhanden, womit man das innere steuern kann """
    level = Levelstruktur(self)
    # innere Rechtecke
    for y in range(3):
        for x in range(3):
            level.form_hinzufuegen(Rechteck(self.wW / 4 + self.wW * (3 / 16) * x,
                                            self.wW / 4 + self.wW * (3 / 16) * y,
                                            self.wW / 8, self.wW / 8, QColor(0, 90, 0), nothing))
    # die vier aeusseren Rechtecke zum steuern
    level.form_hinzufuegen(Rechteck(self.wW / 4 + self.wW * (3 / 16) * 3,
                                    self.wW / 4 + self.wW * (3 / 16),
                                    self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL10))
    level.form_hinzufuegen(Rechteck(self.wW / 4 + self.wW * (3 / 16),
                                    self.wW / 4 + self.wW * (3 / 16) * 3,
                                    self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL10))
    level.form_hinzufuegen(Rechteck(self.wW / 4 - self.wW * (3 / 16),
                                    self.wW / 4 + self.wW * (3 / 16),
                                    self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL10))
    level.form_hinzufuegen(Rechteck(self.wW / 4 + self.wW * (3 / 16),
                                    self.wW / 4 - self.wW * (3 / 16),
                                    self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL10))
    # aeusseren Rechtecken Zahlen zuordnen um in funcL10 zwischen den Funktionsweisen unterscheiden zu koennen
    level.enthalteneFormen[9].internerSpeicherF = 0
    level.enthalteneFormen[10].internerSpeicherF = 1
    level.enthalteneFormen[11].internerSpeicherF = 2
    level.enthalteneFormen[12].internerSpeicherF = 3
    # interner Speicher beschreibt die Position im 2-Dimensionalem
    level.internerSpeicherL = [1, 1]
    # mittleres Feld richtig faerben, da das 'zu bewegende Rechteck' dort beginnt
    level.enthalteneFormen[4].richtig_faerben()
    return level

def level11Erstellen(self) -> Levelstruktur:
    """ Eine Form hat immer genau ein Gegenstueck, welche gegenseitig die Farbe umkehren """
    level = Levelstruktur(self)
    for y in range(4):
        for x in range(4):
            # jede 1. Form wird ein Rechteck, jede zweite ein Kreis
            if (x + y) % 2 == 0:
                level.form_hinzufuegen(Rechteck(self.wW / 6.4 + self.wW * (3 / 16) * x,
                                                self.wW / 6.4 + self.wW * (3 / 16) * y,
                                                self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL11))
            else:
                level.form_hinzufuegen(Kreis(self.wW / 6.4 + self.wW * (3 / 16) * x,
                                             self.wW / 6.4 + self.wW * (3 / 16) * y,
                                             self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL11))
    # jeweilige Gegenstuecke zuordnen
    level.formReferenzenHinzufuegen([ [3], [2], [1], [0], [7], [6], [5], [4],
                                      [11], [10], [9], [8], [15], [14], [13], [12] ])
    return level

def level12Erstellen(self) -> Levelstruktur:
    """ 2 Knoepfe, der 1. ist dafuer da, den Stempel zu bewegen, der 2. zum stempeln. Der Stempel selbst ist unsichtbar
    und er kehrt um statt korrekt zu faerben. """
    level = Levelstruktur(self)
    for y in range(4):
        level.form_hinzufuegen(Rechteck(0, self.wW / 4 * y, self.wW, self.wW / 4, QColor(0, 90, 0), nothing))
        # gerade hinzugefuegtes Rechteck nicht-klickbar machen
        level.enthalteneFormen[-1].klickbar = False
    # Knoepfe hinzufuegen
    level.form_hinzufuegen(Kreis(self.wW / 10,
                                 self.wW * 4 / 25,
                                 self.wW / 8, self.wW / 8, QColor(0, 180, 0), funcL12_1))
    level.form_hinzufuegen(Kreis(self.wW / 10,
                                 self.wW * 1 / 3,
                                 self.wW / 8, self.wW / 8, QColor(0, 180, 0), funcL12_2))
    # internen Speicher des Levels mit Platzhalter fuellen
    level.internerSpeicherL = -1
    return level

def level13Erstellen(self) -> Levelstruktur:
    """ Dreiecke zeigen auf den Kreis, den man als naechstes druecken muss. Dabei wird das naechst zu drueckende
    Dreieck zufaellig bestimmt. """
    level = Levelstruktur(self)
    # nicht klickbare Dreiecke erstellen
    for xDreieck in range(5):
        level.form_hinzufuegen(Polygon((self.wW / 8 + self.wW * 3 / 16 * xDreieck, self.wW / 10 + self.wW / 12,
                                        self.wW / 16 + self.wW * 3 / 16 * xDreieck, self.wW / 4  + self.wW / 12,
                                        self.wW * 3 / 16 +  self.wW * 3 / 16 * xDreieck, self.wW / 4 + self.wW / 12),
                                       QColor(0, 90, 0), nothing))
    # Kreise erstellen
    for xKreis in range(4):
        level.form_hinzufuegen(Kreis(self.wW * 5 / 32 + self.wW * 3 / 16 * xKreis, self.wW / 2,
                                     self.wW / 8, self.wW / 8,
                                     QColor(0, 90, 0), level_zuruecksetzen))
    # Rotationen der Dreiecke, die sie annehmen, je nach dem welcher Kreis als naechster ist, vorab speichern
    level.internerSpeicherL = ( (162, 199, 225, 240, 247) , (135, 162, 199, 225, 240) ,
                                (120, 135, 162, 199, 225) , (113, 120, 135, 162, 199) )
    # erste Form zufaellig bestimmen, der die richtige Funktion zugewiesen wird
    ersteForm : int = randint(5, 8)
    level.enthalteneFormen[ersteForm].func = funcL13
    # Dreiecke auf ersten Kreis ausrichten
    for dreieckIndex in range(5):
        level.enthalteneFormen[dreieckIndex].rotation = level.internerSpeicherL[ersteForm - 5][dreieckIndex]
    return level

def level14Erstellen(self) -> Levelstruktur:
    """ 3 Formen zum drehen mit X und Y vorhanden """
    level = Levelstruktur(self)
    # obere Knoepfe hinzufuegen
    for xRechteck in range(3):
        level.form_hinzufuegen(Rechteck(self.wW / 8 + self.wW * (5 / 16) * xRechteck,
                                        self.wW / 5,
                                        self.wW / 8, self.wW / 8, QColor(0, 90, 0), nothing))
    # jeweilige Funktionen zuordnen
    level.enthalteneFormen[0].func = funcL14_1
    level.enthalteneFormen[1].func = funcL14_2
    level.enthalteneFormen[2].func = funcL14_3

    # schwarze bereits korrekt gedrehte Polygone hinter den drehbaren zur Orientierung zuerst hinzufuegen ...
    for xPolygon in range(3):
        level.form_hinzufuegen(Polygon((self.wW / 8 + self.wW * (5 / 16) * xPolygon, self.wW * 11 / 16,
                                        self.wW / 8 + self.wW * (5 / 16) * xPolygon, self.wW / 2,
                                        self.wW / 4 + self.wW * (5 / 16) * xPolygon, self.wW / 2,
                                        self.wW / 4 + self.wW * (5 / 16) * xPolygon, self.wW * 11 / 16,
                                        self.wW * 3 / 16 + self.wW * (5 / 16) * xPolygon, self.wW * 9 / 16),
                                       QColor(0, 0, 0), nothing))
    # ... dann drehen
    level.enthalteneFormen[3].rotation = 45
    level.enthalteneFormen[4].rotation = 180
    level.enthalteneFormen[5].rotation = 315

    # drehbare Polygone
    for xPolygon in range(3):
        level.form_hinzufuegen(Polygon((self.wW / 8 + self.wW * (5 / 16) * xPolygon, self.wW * 11 / 16,
                                        self.wW / 8 + self.wW * (5 / 16) * xPolygon, self.wW / 2,
                                        self.wW / 4 + self.wW * (5 / 16) * xPolygon, self.wW / 2,
                                        self.wW / 4 + self.wW * (5 / 16) * xPolygon, self.wW * 11 / 16,
                                        self.wW * 3 / 16 + self.wW * (5 / 16) * xPolygon, self.wW * 9 / 16),
                                       QColor(0, 90, 0), nothing))

    level.tastenGesteuert = True
    # [0] und [1] sind die Levelfunktionen, damit diese von den Tasten ausgefuehrt werden koennen
    # [2] ist Zustand des Levels:   0: links und mitte bewegen, 1: alle bewegen, 2: mitte und rechts bewegen
    level.internerSpeicherL = [funcL14_1Level, funcL14_2Level, 1]
    # Hinweislinien an den Knoepfen zeichnen und Steuerungshinweis drunter schreiben
    level.weiteresZeichnen = funcL14WeiteresZeichnen
    return level

def level15Erstellen(self) -> Levelstruktur:
    """ Nur interessant wo relativ zum vorherigen Klick geklickt wurde """
    level = Levelstruktur(self)
    # als Hintergrund einen fenstergrossen Kreis hinzufuegen, auf dem geklickt werden kann
    level.form_hinzufuegen(Kreis(0, 0, self.wW, self.wW, QColor(0, 90, 0), funcL15))
    # alle Pfeile (nach oben gerichtet) hinzufuegen
    for i in range(10):
        level.form_hinzufuegen(Polygon((self.wW / 800 * 38 + self.wW / 800 * 75 * i, self.wW / 800 * 400,
                                        self.wW / 800 * 63 + self.wW / 800 * 75 * i, self.wW / 800 * 350,
                                        self.wW / 800 * 88 + self.wW / 800 * 75 * i, self.wW / 800 * 400,
                                        self.wW / 800 * 75 + self.wW / 800 * 75 * i, self.wW / 800 * 400,
                                        self.wW / 800 * 75 + self.wW / 800 * 75 * i, self.wW / 800 * 412,
                                        self.wW / 800 * 50 + self.wW / 800 * 75 * i, self.wW / 800 * 412,
                                        self.wW / 800 * 50 + self.wW / 800 * 75 * i, self.wW / 800 * 400),
                                       QColor(0, 0, 0), nothing))
        # Bestimmte Pfeile drehen, damit die Hinweise Sinn ergeben
        letzteForm : Form = level.enthalteneFormen[-1]
        # nach rechts
        if i == 4 or i == 9:
            letzteForm.rotation = 90
        # nach unten
        elif i == 2 or i == 7:
            letzteForm.rotation = 180
        # nach links
        elif i == 3 or i == 5 or i == 6:
            letzteForm.rotation = 270
    # als ersten Klickpunkt wird (-1, -1) als Platzhalter gespeicht, da dies gar nicht hier angeklickt werden kann
    level.enthalteneFormen[0].internerSpeicherF = (-1, -1)
    # [0] ist der vorgesehene Ablauf  ,  [1] ist der Index, also der Zeiger, in welchem Zustand man nun ist
    level.internerSpeicherL = [ (3, 3, 1, 2, 0, 2, 2, 1, 3, 0), 0]
    level.enthalteneFormen[0].klickKoordinatenMerken = True
    return level

def level16Erstellen(self) -> Levelstruktur:
    """ Jede Form hat eine andere zugewiesene Form. Einige Formen sind bereits gefaerbt, andere nicht, sodass man
    sich letztlich etwas verliert, wenn man sich nicht die anfangs gefaerbten gemerkt hat """
    level = Levelstruktur(self)
    for y in range(3):
        for x in range(4):
            # bestimmte Felder werden bereits richtig gefaerbt
            genutzteFarbe : QColor = QColor(0, 90, 0)
            if (x,y) in [ (0,3), (1,0), (1,2), (1,3), (2,1), (2,2), (3,0), (3,1) ]:
                genutzteFarbe = QColor(0, 180, 0)
            level.form_hinzufuegen(Rechteck(self.wW / 6.4 + self.wW * (3 / 16) * x,
                                            self.wW / 5 + self.wW * (3 / 16) * y,
                                            self.wW / 8, self.wW / 8, genutzteFarbe, funcL16))
    # je verbundenes Rechteck zuweisen
    level.formReferenzenHinzufuegen([ [2], [4], [5], [0], [10], [1], [6], [3], [9], [11], [7], [8] ])
    return level

def level17Erstellen(self) -> Levelstruktur:
    """ jeweils kleiner Hinweis auf dem Feld, welches als naechstes kommt """
    level = Levelstruktur(self)
    # klickbare Rechtecke hinzufuegen
    for y in range(4):
        for x in range(3):
            level.form_hinzufuegen(Rechteck(self.wW / 4 + self.wW * (3 / 16) * x,
                                            self.wW / 6 + self.wW * (3 / 16) * y,
                                            self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL17))
    # zu jeder Form eine verbundene hinzufuegen
    level.formReferenzenHinzufuegen([ [1], [10], [8], [6], [5], [3], [0], [4], [7], [11], [9], [2] ])
    # schwarze Dreiecke als Hinweise auf den Rechtecken hinzufuegen
    for y in range(4):
        for x in range(3):
            level.form_hinzufuegen(Polygon((self.wW / 800 * 250 + self.wW * (3 / 16) * x,
                                            self.wW / 800 * 155 + self.wW * (3 / 16) * y,
                                            self.wW / 800 * 225 + self.wW * (3 / 16) * x,
                                            self.wW / 800 * 205 + self.wW * (3 / 16) * y,
                                            self.wW / 800 * 275 + self.wW * (3 / 16) * x,
                                            self.wW / 800 * 205 + self.wW * (3 / 16) * y ),
                                            QColor(0, 0, 0), nothing))
            # korrekt drehen
            letzteForm : Form = level.enthalteneFormen[-1]
            # nach rechts
            if (x,y) in [(0,0), (0,3), (1,1)]:
                letzteForm.rotation = 90
            # nach unten
            elif (x, y) in [(0, 1), (1, 0), (2, 0)]:
                letzteForm.rotation = 180
            # nach links
            elif (x, y) in [(1, 3), (2, 1), (2, 2)]:
                letzteForm.rotation = 270

    # weitere Dreiecke fuer die doppelten und dreifachen hinzufuegen
    level.form_hinzufuegen(
        Polygon((self.wW / 800 * 250 + self.wW * (3 / 16) * 0, self.wW / 800 * 165 + self.wW * (3 / 16) * 2,
                 self.wW / 800 * 225 + self.wW * (3 / 16) * 0, self.wW / 800 * 215 + self.wW * (3 / 16) * 2,
                 self.wW / 800 * 275 + self.wW * (3 / 16) * 0, self.wW / 800 * 215 + self.wW * (3 / 16) * 2),
                QColor(0, 0, 0), nothing))
    level.form_hinzufuegen(
        Polygon((self.wW / 800 * 240 + self.wW * (3 / 16) * 0, self.wW / 800 * 155 + self.wW * (3 / 16) * 3,
                 self.wW / 800 * 215 + self.wW * (3 / 16) * 0, self.wW / 800 * 205 + self.wW * (3 / 16) * 3,
                 self.wW / 800 * 265 + self.wW * (3 / 16) * 0, self.wW / 800 * 205 + self.wW * (3 / 16) * 3),
                QColor(0, 0, 0), nothing))
    level.enthalteneFormen[-1].rotation = 90
    level.form_hinzufuegen(
        Polygon((self.wW / 800 * 250 + self.wW * (3 / 16) * 1, self.wW / 800 * 145 + self.wW * (3 / 16) * 0,
                 self.wW / 800 * 225 + self.wW * (3 / 16) * 1, self.wW / 800 * 195 + self.wW * (3 / 16) * 0,
                 self.wW / 800 * 275 + self.wW * (3 / 16) * 1, self.wW / 800 * 195 + self.wW * (3 / 16) * 0),
                QColor(0, 0, 0), nothing))
    level.enthalteneFormen[-1].rotation = 180
    level.form_hinzufuegen(
        Polygon((self.wW / 800 * 250 + self.wW * (3 / 16) * 1, self.wW / 800 * 135 + self.wW * (3 / 16) * 0,
                 self.wW / 800 * 225 + self.wW * (3 / 16) * 1, self.wW / 800 * 185 + self.wW * (3 / 16) * 0,
                 self.wW / 800 * 275 + self.wW * (3 / 16) * 1, self.wW / 800 * 185 + self.wW * (3 / 16) * 0),
                QColor(0, 0, 0), nothing))
    level.enthalteneFormen[-1].rotation = 180
    level.form_hinzufuegen(
        Polygon((self.wW / 800 * 250 + self.wW * (3 / 16) * 2, self.wW / 800 * 145 + self.wW * (3 / 16) * 0,
                 self.wW / 800 * 225 + self.wW * (3 / 16) * 2, self.wW / 800 * 195 + self.wW * (3 / 16) * 0,
                 self.wW / 800 * 275 + self.wW * (3 / 16) * 2, self.wW / 800 * 195 + self.wW * (3 / 16) * 0),
                QColor(0, 0, 0), nothing))
    level.enthalteneFormen[-1].rotation = 180
    level.form_hinzufuegen(
        Polygon((self.wW / 800 * 250 + self.wW * (3 / 16) * 2, self.wW / 800 * 165 + self.wW * (3 / 16) * 3,
                 self.wW / 800 * 225 + self.wW * (3 / 16) * 2, self.wW / 800 * 215 + self.wW * (3 / 16) * 3,
                 self.wW / 800 * 275 + self.wW * (3 / 16) * 2, self.wW / 800 * 215 + self.wW * (3 / 16) * 3),
                QColor(0, 0, 0), nothing))
    level.form_hinzufuegen(
        Polygon((self.wW / 800 * 250 + self.wW * (3 / 16) * 2, self.wW / 800 * 175 + self.wW * (3 / 16) * 3,
                 self.wW / 800 * 225 + self.wW * (3 / 16) * 2, self.wW / 800 * 225 + self.wW * (3 / 16) * 3,
                 self.wW / 800 * 275 + self.wW * (3 / 16) * 2, self.wW / 800 * 225 + self.wW * (3 / 16) * 3),
                QColor(0, 0, 0), nothing))
    return level

def level18Erstellen(self) -> Levelstruktur:
    """ Form, die aus einer Linie besteht, abgebildet, an der links und rechts von der Linie unregelmaessig Kreise sind.
    diese sind Hinweise, ob man nun den linken oder rechten Knopf druecken muss. """
    level = Levelstruktur(self)

    # Kreise, welche die Hinweise darstellen, hinzufuegen
    level.form_hinzufuegen(Kreis(self.wW / 4, self.wW * 46 / 80,
                                 self.wW / 16, self.wW / 16, QColor(0, 90, 0), nothing))
    level.form_hinzufuegen(Kreis(self.wW * 5 / 8, self.wW * 29 / 80,
                                 self.wW / 16, self.wW / 16, QColor(0, 90, 0), nothing))
    level.form_hinzufuegen(Kreis(self.wW * 535 / 800, self.wW * 16 / 80,
                                 self.wW / 16, self.wW / 16, QColor(0, 90, 0), nothing))
    level.form_hinzufuegen(Kreis(self.wW * 375 / 800, self.wW * 103 / 800,
                                 self.wW / 16, self.wW / 16, QColor(0, 90, 0), nothing))
    level.form_hinzufuegen(Kreis(self.wW * 15 / 80, self.wW * 16 / 80,
                                 self.wW / 16, self.wW / 16, QColor(0, 90, 0), nothing))
    level.form_hinzufuegen(Kreis(self.wW * 25 / 80 , self.wW * 29 / 80,
                                 self.wW / 16, self.wW / 16, QColor(0, 90, 0), nothing))
    level.form_hinzufuegen(Kreis(self.wW * 55 / 80, self.wW * 4 / 8,
                                 self.wW / 16, self.wW / 16, QColor(0, 90, 0), nothing))

    # zwei untere Knoepfe erstellen
    for x in range(2):
        level.form_hinzufuegen(Kreis(self.wW * 11 / 32 + self.wW * 3 / 16 * x,
                                     self.wW * 3 / 4,
                                     self.wW / 8, self.wW / 8, QColor(0, 90, 0), funcL18))
    # internen Speicher der Knoepfe zur Unterscheidung in funcL18 fuellen (0: links, 1: rechts)
    level.enthalteneFormen[-2].internerSpeicherF = 0
    level.enthalteneFormen[-1].internerSpeicherF = 1

    # Form, die an den Hinweisen liegt, und Anfangspfeil hinzufuegen
    level.weiteresZeichnen = funcL18WeiteresZeichnen

    # [0] ist der festgelegte Ablauf, [1] ist der Pointer, welcher Zustand nun dran ist
    level.internerSpeicherL = [(1, 0, 1, 1, 1, 0, 0), 0]
    return level