from PyQt5.QtGui import QColor
from typing import List, Callable
from math import sqrt


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

    def richtig_faerben(self) -> None:
        """ Farbe wird zu richtig geaendert """
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


class Rechteck(Form):
    pass

class Kreis(Form):
    pass



class Levelstruktur:

    def __init__(self, zugehoerigesFenster):
        """ Eine Levelstruktur beinhaltet beliebig viele Rechtecke und Kreise
        und hat eine Referenz auf das Fenster, in welchem die Levelstruktur vorliegt """
        self.rechtecke : List[Rechteck] = []
        self.kreise : List[Kreis] = []
        self.zugehoerigesFenster = zugehoerigesFenster
        # interner Speicher jeder Form fuer etwaige Zustaende des Levels
        # zB: Position, die beim klicken betroffen ist, aendert sich jedes mal (bewegt sich im Kreis drum)
        self.internerSpeicherL = None

    def rechteck_hinzufuegen(self, rechteck: Rechteck) -> None:
        self.rechtecke.append(rechteck)
        rechteck.zugehoerigesLevel = self

    def kreis_hinzufuegen(self, kreis: Kreis) -> None:
        self.kreise.append(kreis)
        kreis.zugehoerigesLevel = self

    def weiteresZeichnen(self, painterF) -> None:
        """ Funktion, die Nicht-Rechtecke und Nicht-Kreise zeichnen soll """
        pass

    def gewinnbedingung(self) -> bool:
        """ Gewinnbedingung: Jedes Rechteck und jeder Kreis wird auf seine Farbe ueberprueft """

        for i in self.rechtecke:
            if i.farbe != QColor(0, 180, 0):
                return False
        for j in self.kreise:
            if j.farbe != QColor(0, 180, 0):
                return False
        return True

    def beruehrt(self, x: int, y: int) -> bool:
        """ Pruefen ob eine Form angeklickt wurde """

        # fuer jeden Kreis pruefen, ob der Mausklick in jeweiligem Rechteck drumrum ist
        for kreis in self.kreise:
            if (kreis.klickbar and
                kreis.xKoordinate <= x <= kreis.xKoordinate + kreis.weite) and (
                kreis.yKoordinate <= y <= kreis.yKoordinate + kreis.hoehe):
                # Satz des Pythagoras
                abstand = sqrt((kreis.xKoordinate + kreis.weite / 2 - x)**2 +
                               (kreis.yKoordinate + kreis.hoehe / 2 - y)**2)
                # Maximalen Radius nutzen ist gut fuer Ovale, da sonst teils gefaerbte Flaeche nicht klickbar ist
                radius = max(kreis.weite / 2, kreis.hoehe / 2)
                # Abstand zwischen Mausklick und Kreismittelpunkt berechnen: perfekt bei Kreis, gut bei Oval
                if abstand <= radius:
                    # falls Kreis getroffen, wird seine Funktion ausgefuehrt
                    kreis.func(kreis)
                    # pruefen ob Level gewonnen
                    if self.gewinnbedingung():
                        self.zugehoerigesFenster.levelGewonnen = True
                    return True

        # fuer jedes Rechteck pruefen, ob der Mausklick in jeweiligem ist
        for rechteck in self.rechtecke:
            if (rechteck.klickbar and
                rechteck.xKoordinate <= x <= rechteck.xKoordinate + rechteck.weite) and (
                rechteck.yKoordinate <= y <= rechteck.yKoordinate + rechteck.hoehe):
                # falls Rechteck getroffen, wird seine Funktion ausgefuehrt
                rechteck.func(rechteck)
                # pruefen ob Level gewonnen
                if self.gewinnbedingung():
                    self.zugehoerigesFenster.levelGewonnen = True
                return True

        return False

    def kopieren(self):
        """ Kopiert die Levelstruktur
        deepcopy hat nicht funktioniert """

        neue = Levelstruktur(self.zugehoerigesFenster)

        """ internen Speicher vom alten Level uebernehmen """
        neue.internerSpeicherL = self.internerSpeicherL

        """ neue Rechtecke und Kreise erstellen und dann den internen Speicher beim gerade erstellten uebernehmen"""
        for rec in self.rechtecke:
            neue.rechteck_hinzufuegen(Rechteck(rec.nummer, rec.xKoordinate, rec.yKoordinate,
                                               rec.weite, rec.hoehe, rec.farbe, rec.func))
            neue.rechtecke[-1].internerSpeicherF = rec.internerSpeicherF
            neue.rechtecke[-1].klickbar = rec.klickbar
            neue.rechtecke[-1].sichtbar = rec.sichtbar
        for kreis in self.kreise:
            neue.kreis_hinzufuegen(Kreis(kreis.nummer, kreis.xKoordinate, kreis.yKoordinate,
                                         kreis.weite, kreis.hoehe, kreis.farbe, kreis.func))
            neue.kreise[-1].internerSpeicherF = kreis.internerSpeicherF
            neue.kreise[-1].klickbar = kreis.klickbar
            neue.kreise[-1].sichtbar = kreis.sichtbar

        """ verbundene Formen zuweisen 
        ist so kompliziert noetig, da sonst 'verbundeneFormen' auf die nicht kopierten Formen referenziert """
        # pro originales Rechteck, welches verbundene Formen besitzt, werden diese dort
        # referenzierten-originalen-Rechtecke ('recAltRefRec') durchgegangen
        for recAlt in self.rechtecke:
            for recAltRefRec in recAlt.verbundeneFormen:
                # Kopien nach uebereinstimmendem Rechteck (gleiche Nummer) durchsuchen
                for recNeu in neue.rechtecke:
                    if recAltRefRec.nummer == recNeu.nummer:
                        # bei Uebereinstimmung die richtige Zuweisung zu 'verbundeneFormen' der Kopie hinzufuegen
                        neue.rechtecke[recAlt.nummer].verbundeneFormen.append(recNeu)
        # pro originalem Kreis, welcher verbundene Formen besitzt, werden diese dort
        # referenzierten-originalen-Kreise ('kreisAltRefKreis') durchgegangen
        for kreisAlt in self.kreise:
            for kreisAltRefKreis in kreisAlt.verbundeneFormen:
                # Kopien nach uebereinstimmendem Kreis (gleiche Nummer) durchsuchen
                for kreisNeu in neue.kreise:
                    if kreisAltRefKreis.nummer == kreisNeu.nummer:
                        # bei Uebereinstimmung die richtige Zuweisung zu 'verbundeFormen' der Kopie hinzufuegen
                        neue.kreise[kreisAlt.nummer].verbundeneFormen.append(kreisNeu)
        return neue

    def recReferenzenHinzufuegen(self, anzahlRecs: int, recRefsNummern: List[List[int]]) -> None:
        """ Schnell mehrere Referenzen auf mehrere Rechtecke hinzufuegen
        'anzahlRecs' ist die Anzahl an Rechtecken (also letzter Index + 1)
        'recRefs' ist Liste von Listen mit den jeweilig zuzuweisenden Referenzen
        Wichtig ist, dass die Indizes uebereinstimmen, heisst:
        0. Rechteck bekommt recRefs[0] zugewiesen, 1. Rechteck bekommt recRefs[1] zugewiesen, etc. """
        for clickedRecNummer in range(anzahlRecs):
            for bindRecNummer in recRefsNummern[clickedRecNummer]:
                self.rechtecke[clickedRecNummer].verbundeneFormen.append(self.rechtecke[bindRecNummer])

    def recFuncsAendern(self, zielFunc: Callable[[Form], None], zuAenderndeFormen: List[int] = 'Alle Rechtecke'):
        """ Bestimmten Rechtecken neue Funktion zuweisen
        Wird keine Liste an Rechteck-Indizes angegeben, so werden allen die Funktion zugeordnet """
        if zuAenderndeFormen == 'Alle Rechtecke':
            zuAenderndeFormen = [i for i in range(len(self.rechtecke))]
        for i in zuAenderndeFormen:
            self.rechtecke[i].func = zielFunc

    def recInternerSpeicherAendern(self, zielSpeicher, zuAenderndeFormen: List[int] = 'Alle Rechtecke'):
        """ Den internen Speicher von bestimmten Rechtecken aendern
        Wird keine Liste an Rechteck-Indizes angegeben, so wird jeder interne Speicher betroffen """
        if zuAenderndeFormen == 'Alle Rechtecke':
            zuAenderndeFormen = [i for i in range(len(self.rechtecke))]
        for i in zuAenderndeFormen:
            self.rechtecke[i].internerSpeicherF = zielSpeicher

    def recInternerSpeicherAddieren(self, summand: int, zuAenderndeFormen: List[int] = 'Alle Rechtecke'):
        """ Einen Wert auf den internen Speicher bestimmter Rechtecke hinzuaddieren
        Wird keine Liste an Rechteck-Indizes angegeben, so wird jeder interne Speicher betroffen """
        if zuAenderndeFormen == 'Alle Rechtecke':
            zuAenderndeFormen = [i for i in range(len(self.rechtecke))]
        for i in zuAenderndeFormen:
            self.rechtecke[i].internerSpeicherF += summand

