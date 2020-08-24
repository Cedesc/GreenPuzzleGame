from classes import Levelstruktur, Rechteck, Kreis, QColor
""" Bibliothek fuer Funktionen der Formen und Levelerstellung """


# Funktionen fuer Rechtecke und Kreise

def heyho(self):
    self.gruen_machen()
    self.func = self.level_zuruecksetzen
    self.func = self.nothing
    return

def heyho2(self):
    self.gruen_machen()
    self.func = self.level_zuruecksetzen
    return




# Funktionen für die Levelerstellung
# Koordinaten sollten keine genauen Zahlen sein, sondern immer in Abhaengigkeit der Fenstergroesse

def level0Erstellen(self):
    level = Levelstruktur(self)
    for j in range(2):
        for i in range(3):
            level.rechteck_hinzufuegen(Rechteck(self.wW / 16 + self.wW * (3 / 16) * i,
                                                 self.wW / 16 + self.wW * (3 / 16) * j,
                                                 self.wW / 8, self.wW / 8, QColor(0, 90, 0), heyho))
    return level

def level1Erstellen(self):
    level = Levelstruktur(self)
    for j in range(3):
        for i in range(1):
            level.kreis_hinzufuegen(Kreis(self.wW / 16 + self.wW * (3 / 16) * i,
                                           self.wW / 16 + self.wW * (3 / 16) * j,
                                           self.wW / 8, self.wW / 8, QColor(0, 90, 0), heyho2))
    return level

def level2Erstellen(self):
    level = Levelstruktur(self)
    for j in range(2):
        for i in range(1):
            level.rechteck_hinzufuegen(Rechteck(self.wW / 16 + self.wW * (3 / 16) * (i + 2),
                                                 self.wW / 12 + self.wW * (3 / 16) * (j + 2),
                                                 self.wW / 8, self.wW / 8, QColor(0, 90, 0), heyho2))
    return level


