from PyQt5.QtGui import QColor


class Form:

    def __init__(self, nummer, xKoordinate, yKoordinate, weite, hoehe, farbe, func):
        # 'nummer' soll gleich des Index sein, welchen die Form in der Levelstruktur hat.
        self.nummer = nummer
        self.xKoordinate = xKoordinate
        self.yKoordinate = yKoordinate
        self.weite = weite
        self.hoehe = hoehe
        self.farbe = farbe
        self.func = func
        self.zugehoerigesLevel = None
        # Referenz auf andere Form, damit beim anklicken auch Aenderungen an dieser getaetigt werden koennen
        self.verbundeneFormen = []

    def gruen_machen(self):
        self.farbe = QColor(0, 180, 0)


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
        """ Pruefen ob eine Form angeklickt wurde """

        # fuer jeden Kreis pruefen, ob der Mausklick in jeweiligem ist (nicht gut implementiert, da rechteckig!)
        for kreis in self.kreise:
            if (kreis.xKoordinate <= x <= kreis.xKoordinate + kreis.weite) and (
                    kreis.yKoordinate <= y <= kreis.yKoordinate + kreis.hoehe):
                # falls Kreis getroffen, wird seine Funktion ausgefuehrt
                kreis.func(kreis)
                # pruefen ob Level gewonnen
                if self.gewinnbedingung():
                    self.zugehoerigesFenster.nextLevel()
                return True

        # fuer jedes Rechteck pruefen, ob der Mausklick in jeweiligem ist
        for rechteck in self.rechtecke:
            if (rechteck.xKoordinate <= x <= rechteck.xKoordinate + rechteck.weite) and (
                    rechteck.yKoordinate <= y <= rechteck.yKoordinate + rechteck.hoehe):
                # falls Rechteck getroffen, wird seine Funktion ausgefuehrt
                rechteck.func(rechteck)
                # pruefen ob Level gewonnen
                if self.gewinnbedingung():
                    self.zugehoerigesFenster.nextLevel()
                return True

        return False

    def kopieren(self):
        """ Kopiert die Levelstruktur
        deepcopy hat nicht funktioniert """

        neue = Levelstruktur(self.zugehoerigesFenster)

        """ neue Rechtecke und Kreise erstellen """
        for rec in self.rechtecke:
            neue.rechteck_hinzufuegen(Rechteck(rec.nummer, rec.xKoordinate, rec.yKoordinate,
                                               rec.weite, rec.hoehe, rec.farbe, rec.func))
        for kreis in self.kreise:
            neue.kreis_hinzufuegen(Kreis(kreis.nummer, kreis.xKoordinate, kreis.yKoordinate,
                                         kreis.weite, kreis.hoehe, kreis.farbe, kreis.func))

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
                        neue.rechtecke[kreisAlt.nummer].verbundeneFormen.append(kreisNeu)
        return neue

