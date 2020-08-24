from PyQt5.QtGui import QColor


class Form:

    def __init__(self, xKoordinate, yKoordinate, weite, hoehe, farbe, func):
        self.xKoordinate = xKoordinate
        self.yKoordinate = yKoordinate
        self.weite = weite
        self.hoehe = hoehe
        self.farbe = farbe
        self.func = func
        self.zugehoerigesLevel = None

    def gruen_machen(self):
        self.farbe = QColor(0, 180, 0)

    # grundlegende zuweisbare Funktionen

    def nothing(self, self2):
        """ Wenn draufgeklickt wird, soll nichts ausgefuehrt werden """
        return 0
    def level_zuruecksetzen(self, self2):
        """ Falls zB ein Fehler gemacht wurde, wird das Level zurueckgesetzt """
        self.zugehoerigesLevel.zugehoerigesFenster.levelReset()

class Rechteck(Form):
    pass

class Kreis(Form):
    pass


class Levelstruktur:

    def __init__(self, zugehoerigesFenster):
        """ Eine Levelstruktur beinhaltet beliebig viele Rechtecke und Kreise
        und hat eine Referenz auf das Fenster, in welchem die Levelstruktur vorliegt """
        self.rechtecke = []
        self.kreise = []
        self.zugehoerigesFenster = zugehoerigesFenster

    def rechteck_hinzufuegen(self, rechteck):
        self.rechtecke.append(rechteck)
        rechteck.zugehoerigesLevel = self

    def kreis_hinzufuegen(self, kreis):
        self.kreise.append(kreis)
        kreis.zugehoerigesLevel = self

    def weiteresZeichnen(self, painterF):
        """ Funktion, die Nicht-Rechtecke und Nicht-Kreise zeichnen soll """
        pass

    def gewinnbedingung(self):
        """ Gewinnbedingung: Jedes Rechteck und jeder Kreis wird auf seine Farbe ueberprueft """
        for i in self.rechtecke:
            if i.farbe != QColor(0, 180, 0):
                return False
        for j in self.kreise:
            if j.farbe != QColor(0, 180, 0):
                return False
        return True

    def beruehrt(self, x, y):

        for kreis in self.kreise:
            if (kreis.xKoordinate <= x <= kreis.xKoordinate + kreis.weite) and (
                    kreis.yKoordinate <= y <= kreis.yKoordinate + kreis.hoehe):
                kreis.func(kreis)

                if self.gewinnbedingung():      # setzt ein, wenn man das Level gewonnen hat
                    self.zugehoerigesFenster.nextLevel()
                return True

        for rechteck in self.rechtecke:
            if (rechteck.xKoordinate <= x <= rechteck.xKoordinate + rechteck.weite) and (
                    rechteck.yKoordinate <= y <= rechteck.yKoordinate + rechteck.hoehe):
                rechteck.func(rechteck)

                if self.gewinnbedingung():      # setzt ein, wenn man das Level gewonnen hat
                    self.zugehoerigesFenster.nextLevel()
                return True
        return False

    def kopieren(self):
        """ Kopiert die Levelstruktur, deepcopy hat nicht funktioniert """
        neue = Levelstruktur(self.zugehoerigesFenster)
        for rec in self.rechtecke:
            neue.rechteck_hinzufuegen(Rechteck(rec.xKoordinate, rec.yKoordinate,
                                               rec.weite, rec.hoehe, rec.farbe, rec.func))
        for kreis in self.kreise:
            neue.kreis_hinzufuegen(Kreis(kreis.xKoordinate, kreis.yKoordinate,
                                         kreis.weite, kreis.hoehe, kreis.farbe, kreis.func))
        return neue