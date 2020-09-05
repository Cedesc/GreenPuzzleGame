from PyQt5.QtGui import QColor
from typing import List, Callable
from math import sqrt
from copy import copy


class Form:

    def __init__(self, nummer: float, xKoordinate: float, yKoordinate: float, weite: float, hoehe: float,
                 farbe: QColor, func):
        # 'nummer' soll gleich des Index sein, welchen die Form in der Levelstruktur hat.
        self.nummer : int = int(nummer)
        self.xKoordinate : int = int(xKoordinate)
        self.yKoordinate : int = int(yKoordinate)
        self.weite : int = int(weite)
        self.hoehe : int = int(hoehe)
        self.farbe : QColor = farbe
        self.func : Callable[[Form], None] = func
        self.zugehoerigesLevel : Levelstruktur = None
        # Referenz auf andere Form, damit beim anklicken auch Aenderungen an dieser getaetigt werden koennen
        self.verbundeneFormen : List[Form] = []
        # interner Speicher jeder Form fuer etwaige Zustaende der Form
        # zB: muss 3 mal geklickt werden, bis es korrekt gefaerbt wird
        self.internerSpeicherF = None
        self.klickbar : bool = True
        self.sichtbar : bool = True
        self.aufleuchten : bool = False
        self.welcheForm : int = 0           # 0: Platzhalter , 1: Rechteck , 2: Kreis , 3: Polygon
        self.eckpunkte : tuple = tuple()
        self.rotation : int = 0

        # Berechnung bei Erstellung
        self.mittelpunkt : (int, int) = (int(self.xKoordinate + weite // 2), int(self.yKoordinate + hoehe // 2))
        self.xRelZuMitte : int = self.xKoordinate - self.mittelpunkt[0]
        self.yRelZuMitte : int = self.yKoordinate - self.mittelpunkt[1]
        self.eckpunkteRelZuMitte : tuple = tuple()

    def richtig_faerben(self) -> None:
        """ Farbe wird zu richtig geaendert """
        self.farbe = QColor(0, 180, 0)
        self.aufleuchten = True

    def richtig_faerben_ohneAufleuchten(self) -> None:
        """ Farbe wird zu richtig geaendert
        Aufleuchten deaktiviert """
        self.farbe = QColor(0, 180, 0)

    def falsch_faerben(self) -> None:
        """ Farbe wird zu falsch geaendert """
        self.farbe = QColor(0, 90, 0)

    def richtig_faerben_verschwinden(self) -> None:
        """ Farbe wird korrekt gefaerbt, angezeigt wird jedoch der Hintergrund """
        self.farbe = QColor(0, 180, 0)
        self.sichtbar = False

    def umkehren(self) -> None:
        """ Farbe wird umgekehrt: Falls richtig wird es zu falsch, falls falsch wird es zu richtig """
        if self.farbe == QColor(0, 180, 0):
            self.farbe = QColor(0, 90, 0)
        elif self.farbe == QColor(0, 90, 0):
            self.farbe = QColor(0, 180, 0)
        self.aufleuchten = True

    def umkehren_ohneAufleuchten(self) -> None:
        """ Farbe wird umgekehrt: Falls richtig wird es zu falsch, falls falsch wird es zu richtig
        Aufleuchten deaktiviert """
        if self.farbe == QColor(0, 180, 0):
            self.farbe = QColor(0, 90, 0)
        elif self.farbe == QColor(0, 90, 0):
            self.farbe = QColor(0, 180, 0)

class Rechteck(Form):

    def __init__(self, nummer: float, xKoordinate: float, yKoordinate: float, weite: float, hoehe: float, farbe: QColor, func):
        super().__init__(nummer, xKoordinate, yKoordinate, weite, hoehe, farbe, func)
        self.welcheForm = 1
        self.eckpunkte = ((self.xKoordinate, self.yKoordinate),
                          (self.xKoordinate + self.weite, self.yKoordinate),
                          (self.xKoordinate, self.yKoordinate + self.hoehe),
                          (self.xKoordinate + self.weite, self.yKoordinate + self.hoehe))

class Kreis(Form):

    def __init__(self, nummer: float, xKoordinate: float, yKoordinate: float, weite: float, hoehe: float, farbe: QColor, func):
        super().__init__(nummer, xKoordinate, yKoordinate, weite, hoehe, farbe, func)
        self.welcheForm = 2

class Polygon(Form):

    def __init__(self, nummer: float, eckpunktKoordinaten: tuple,farbe: QColor, func):
        super().__init__(nummer, min(eckpunktKoordinaten[0::2]),
                         min(eckpunktKoordinaten[1::2]),
                         max(eckpunktKoordinaten[0::2]) - min(eckpunktKoordinaten[0::2]),
                         max(eckpunktKoordinaten[1::2]) - min(eckpunktKoordinaten[1::2]),
                         farbe, func)
        if len(eckpunktKoordinaten) % 2 == 1:
            print("Fehlende yKoordinate in eckpunktKoordinaten!")
        self.welcheForm = 3
        self.klickbar = False
        self.eckpunkte = eckpunktKoordinaten
        self.mittelpunkt = (sum(self.eckpunkte[0::2]) // len(self.eckpunkte) * 2,
                            sum(self.eckpunkte[1::2]) // len(self.eckpunkte) * 2)
        self.xRelZuMitte = self.xKoordinate - self.mittelpunkt[0]
        self.yRelZuMitte = self.yKoordinate - self.mittelpunkt[1]

        hilfsListe = []
        for index in range(len(self.eckpunkte)):
            if index % 2 == 0:
                hilfsListe.append(self.eckpunkte[index] - self.mittelpunkt[0])
            else:
                hilfsListe.append(self.eckpunkte[index] - self.mittelpunkt[1])
        self.eckpunkteRelZuMitte = tuple(hilfsListe)


class Levelstruktur:

    def __init__(self, zugehoerigesFenster):
        """ Eine Levelstruktur beinhaltet beliebig viele Rechtecke und Kreise
        und hat eine Referenz auf das Fenster, in welchem die Levelstruktur vorliegt """
        self.enthalteneFormen : List[Form] = []
        self.zugehoerigesFenster = zugehoerigesFenster
        # interner Speicher jeder Form fuer etwaige Zustaende des Levels
        # zB: Position, die beim klicken betroffen ist, aendert sich jedes mal (bewegt sich im Kreis drum)
        self.internerSpeicherL = None

    def form_hinzufuegen(self, form: Form) -> None:
        self.enthalteneFormen.append(form)
        form.zugehoerigesLevel = self

    def weiteresZeichnen(self, painterF) -> None:
        """ Funktion, die Nicht-Rechtecke und Nicht-Kreise zeichnen soll """
        pass

    def gewinnbedingung(self) -> bool:
        """ Gewinnbedingung: Jedes Rechteck und jeder Kreis wird auf seine Farbe ueberprueft """

        for i in self.enthalteneFormen:
            if i.farbe != QColor(0, 180, 0):
                return False
        return True

    def beruehrt(self, x: int, y: int) -> bool:
        """ Pruefen ob eine Form angeklickt wurde. Bei einem Rechteck leicht festzustellen. Bei einem Kreis
        wird noch der Abstand zum Mittelpunkt des Kreises berechnet um sicherzustellen, dass im Kreis geklickt wurde.
        Bei Ovalen kann nur eine (gute) Annaeherung sichergestellt werden """

        # fuer jede Form pruefen, ob der Mausklick in jeweiliger ist und ob die Form ueberhaupt klickbar ist
        for form in self.enthalteneFormen:
            if (form.klickbar and
                form.xKoordinate <= x <= form.xKoordinate + form.weite) and (
                form.yKoordinate <= y <= form.yKoordinate + form.hoehe):
                # pruefen welche Art von Form getroffen wurde
                if form.welcheForm == 1:
                    # falls Rechteck getroffen wurde, wird seine Funktion ausgefuehrt
                    form.func(form)
                elif form.welcheForm == 2:
                    # Satz des Pythagoras
                    abstand = sqrt((form.mittelpunkt[0] - x) ** 2 + (form.mittelpunkt[1] - y) ** 2)
                    # Maximalen Radius nutzen ist gut fuer Ovale, da sonst teils gefaerbte Flaeche nicht klickbar ist
                    radius = max(form.weite / 2, form.hoehe / 2)
                    # Abstand zwischen Mausklick und Kreismittelpunkt berechnen: perfekt bei Kreis, gut bei Oval
                    if abstand <= radius:
                        # falls Kreis getroffen wurde, wird seine Funktion ausgefuehrt
                        form.func(form)

                # pruefen ob Level gewonnen, da hier auf jeden Fall eine Form getroffen wurde
                if self.gewinnbedingung():
                    self.zugehoerigesFenster.levelGewonnen = True
                return True

        return False

    def kopieren(self):
        """ Kopiert die Levelstruktur
        deepcopy hat nicht funktioniert """

        # self.eckpunkte: tuple = tuple()
        # self.rotation: int = 0
        # self.mittelpunkt: (int, int) = (int(self.xKoordinate + weite // 2), int(self.yKoordinate + hoehe // 2))
        # self.xRelZuMitte: int = self.xKoordinate - self.mittelpunkt[0]
        # self.yRelZuMitte: int = self.yKoordinate - self.mittelpunkt[1]

        neue = Levelstruktur(self.zugehoerigesFenster)

        """ internen Speicher vom alten Level uebernehmen """
        neue.internerSpeicherL = copy(self.internerSpeicherL)

        """ neue Rechtecke und Kreise erstellen und dann den internen Speicher beim gerade erstellten uebernehmen"""
        for form in self.enthalteneFormen:
            # Falls Original Rechteck ist: Rechteck hinzufuegen
            if form.welcheForm == 1:
                neue.form_hinzufuegen(Rechteck(form.nummer, form.xKoordinate, form.yKoordinate,
                                               form.weite, form.hoehe, form.farbe, form.func))
            # Falls Original Kreis ist: Kreis hinzufuegen
            if form.welcheForm == 2:
                neue.form_hinzufuegen(Kreis(form.nummer, form.xKoordinate, form.yKoordinate,
                                            form.weite, form.hoehe, form.farbe, form.func))
            # Falls Original Polygon ist: Polygon hinzufuegen
            if form.welcheForm == 3:
                neue.form_hinzufuegen(Polygon(form.nummer, form.eckpunkte, form.farbe, form.func))
            neue.enthalteneFormen[-1].internerSpeicherF = copy(form.internerSpeicherF)
            neue.enthalteneFormen[-1].klickbar = form.klickbar
            neue.enthalteneFormen[-1].sichtbar = form.sichtbar
            neue.enthalteneFormen[-1].aufleuchten = form.aufleuchten
            neue.enthalteneFormen[-1].eckpunkte = form.eckpunkte
            neue.enthalteneFormen[-1].rotation = form.rotation
            neue.enthalteneFormen[-1].eckpunkteRelZuMitte = form.eckpunkteRelZuMitte

        """ verbundene Formen zuweisen 
        ist so kompliziert noetig, da sonst 'verbundeneFormen' auf die nicht kopierten Formen referenziert """
        # pro originaler Form, welches verbundene Formen besitzt, werden diese dort
        # referenzierten-originalen-Formen ('formAltRefForm') durchgegangen
        for formAlt in self.enthalteneFormen:
            for formAltRefForm in formAlt.verbundeneFormen:
                # Kopien nach uebereinstimmendem Rechteck (gleiche Nummer) durchsuchen
                for formNeu in neue.enthalteneFormen:
                    if formAltRefForm.nummer == formNeu.nummer:
                        # bei Uebereinstimmung die richtige Zuweisung zu 'verbundeneFormen' der Kopie hinzufuegen
                        neue.enthalteneFormen[formAlt.nummer].verbundeneFormen.append(formNeu)
        return neue

    def formReferenzenHinzufuegen(self, anzahlFormen: int, formRefsNummern: List[List[int]]) -> None:
        """ Schnell mehrere Referenzen auf mehrere Formen hinzufuegen
        'anzahlFormen' ist die Anzahl an Formen (also letzter Index + 1)
        'formRefsNummern' ist Liste von Listen mit den jeweilig zuzuweisenden Referenzen
        Wichtig ist, dass die Indizes uebereinstimmen, heisst:
        0. Form bekommt formRefsNummern[0] zugewiesen, 1. Form bekommt formRefsNummern[1] zugewiesen, etc. """
        for clickedFormNummer in range(anzahlFormen):
            for bindFormNummer in formRefsNummern[clickedFormNummer]:
                self.enthalteneFormen[clickedFormNummer].verbundeneFormen.append(self.enthalteneFormen[bindFormNummer])

    def formFuncsAendern(self, zielFunc: Callable[[Form], None], zuAenderndeFormen: List[int] = 'Alle Formen'):
        """ Bestimmten Formen neue Funktion zuweisen
        Wird keine Liste an Form-Indizes angegeben, so werden allen die Funktion zugeordnet """
        if zuAenderndeFormen == 'Alle Formen':
            zuAenderndeFormen = [i for i in range(len(self.enthalteneFormen))]
        for i in zuAenderndeFormen:
            self.enthalteneFormen[i].func = zielFunc

    def formInternerSpeicherAendern(self, zielSpeicher, zuAenderndeFormen: List[int] = 'Alle Formen'):
        """ Den internen Speicher von bestimmten Formen aendern
        Wird keine Liste an Form-Indizes angegeben, so wird jeder interne Speicher betroffen """
        if zuAenderndeFormen == 'Alle Formen':
            zuAenderndeFormen = [i for i in range(len(self.enthalteneFormen))]
        for i in zuAenderndeFormen:
            self.enthalteneFormen[i].internerSpeicherF = zielSpeicher

    def formInternerSpeicherAddieren(self, summand: int, zuAenderndeFormen: List[int] = 'Alle Formen'):
        """ Einen Wert auf den internen Speicher bestimmter Formen hinzuaddieren
        Wird keine Liste an Form-Indizes angegeben, so wird jeder interne Speicher betroffen """
        if zuAenderndeFormen == 'Alle Formen':
            zuAenderndeFormen = [i for i in range(len(self.enthalteneFormen))]
        for i in zuAenderndeFormen:
            self.enthalteneFormen[i].internerSpeicherF += summand

