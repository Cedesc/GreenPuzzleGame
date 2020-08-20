import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen, QImage, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QEvent, QRect, QPointF, QPropertyAnimation, QTimer
import functionsBib
import settings



class Rechteck:

    def __init__(self, xKoordinate, yKoordinate, weite, hoehe, farbe):
        self.xKoordinate = xKoordinate
        self.yKoordinate = yKoordinate
        self.weite = weite
        self.hoehe = hoehe
        self.farbe = farbe
        self.zugehoerigesLevel = None
        self.func = functionsBib.heyho

    # grundlegende Funktionen
    def gruen_machen(self):
        self.farbe = QColor(0, 180, 0)

    def nothing(self, n1, n2, n3):
        pass

    def level_zuruecksetzen(self, n1, n2, n3):
        self.zugehoerigesLevel.zugehoerigesFenster.levelReset()


class Kreis:

    def __init__(self, xKoordinate, yKoordinate, weite, hoehe, farbe):
        self.xKoordinate = xKoordinate
        self.yKoordinate = yKoordinate
        self.weite = weite
        self.hoehe = hoehe
        self.farbe = farbe
        self.zugehoerigesLevel = None
        self.func = functionsBib.heyho2

    def gruen_machen(self):
        self.farbe = QColor(0, 180, 0)

    def nothing(self, n1, n2, n3):
        pass

    def level_zuruecksetzen(self, n1, n2, n3):
        self.zugehoerigesLevel.zugehoerigesFenster.levelReset()


class Levelstruktur:

    def __init__(self, zugehoerigesFenster):
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
                kreis.func(kreis, x, y)

                if self.gewinnbedingung():      # setzt ein, wenn man das Level gewonnen hat
                    self.zugehoerigesFenster.nextLevel()
                return True

        for rechteck in self.rechtecke:
            if (rechteck.xKoordinate <= x <= rechteck.xKoordinate + rechteck.weite) and (
                    rechteck.yKoordinate <= y <= rechteck.yKoordinate + rechteck.hoehe):
                rechteck.func(rechteck, x, y)

                if self.gewinnbedingung():      # setzt ein, wenn man das Level gewonnen hat
                    self.zugehoerigesFenster.nextLevel()
                return True
        return False

    def kopieren(self):     # kopiert die Levelstruktur, deepcopy hat nicht funktioniert
        neue = Levelstruktur(self.zugehoerigesFenster)
        for rec in self.rechtecke:
            neue.rechteck_hinzufuegen(Rechteck(rec.xKoordinate, rec.yKoordinate, rec.weite, rec.hoehe, rec.farbe))
        for kreis in self.kreise:
            neue.kreis_hinzufuegen(Kreis(kreis.xKoordinate, kreis.yKoordinate, kreis.weite, kreis.hoehe, kreis.farbe))
        return neue










class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.wW = settings.BREITE       # windowWidth ; Fenster ist immer quadratisch
        self.setGeometry(600, 150, self.wW, self.wW)
        self.setWindowTitle("Spaß mit grünem")
        self.originalLevels = []        # Speicher fuer die urspruenglichen Level (relevant beim level reset)
        self.levels = []                # Speicher fuer Level
        self.levelCounter = 0           # Index des momentan zu bearbeitendem Level
        self.maxLevel = 2               # den maximal zu erreichenden Index der level-liste, heißt Anzahl der Level
        self.levelGewonnen = False

        self.initalisierung()
        self.keyPressEvent = self.fn

        self.show()


    def paintEvent(self, event):
        # Hintergrund zeichnen
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 180, 0), 1, Qt.SolidLine))
        painter.fillRect(0, 0, self.wW, self.wW, QColor(0, 180, 0))
        rect1 = QRect(int(self.wW / 2), int(self.wW / 40), int(self.wW / 20), int(self.wW / 20))
        painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
        painter.drawText(rect1, 0, str(self.levelCounter))

        if self.levelGewonnen:
            if self.levelCounter > self.maxLevel:
                print("Glueckwunsch, du hast alle Level abgeschlossen")
                self.close()

            # Kurzer Übergang zum nächsten Level, verschwindet nach 3 Sekunden
            rect2 = QRect( int(self.wW / 2.5), int(self.wW / 2), int(self.wW / 2), int(self.wW / 2) )
            rect3 = QRect( int(self.wW / 1.75), int(self.wW / 2), int(self.wW / 2), int(self.wW / 2) )
            painter.drawText(rect2, 0, "Glückwunsch, du hast Level        geschafft")
            painter.drawText(rect3, 0, str(self.levelCounter-1))
            self.levelGewonnen = False
            QTimer.singleShot(1500, self.update)
            return

        # Level zeichnen
        for rechteck in self.levels[self.levelCounter].rechtecke:
            painter.fillRect(rechteck.xKoordinate, rechteck.yKoordinate,
                             rechteck.weite, rechteck.hoehe, rechteck.farbe)

        for kreis in self.levels[self.levelCounter].kreise:
            painter.setPen(QPen(kreis.farbe, 1, Qt.SolidLine))
            painter.setBrush(kreis.farbe)
            painter.drawEllipse(kreis.xKoordinate, kreis.yKoordinate,
                             kreis.weite, kreis.hoehe)

        self.levels[self.levelCounter].weiteresZeichnen(painter)


    def fn(self, e):

        if e.key() == Qt.Key_H:
            """ H druecken um Tastenbelegung anzuzeigen """
            print("- Steuerung :",
                  "\n    - H (Hilfe) : Steuerung anzeigen",
                  "\n    - Esc (Escape) : Fenster schliessen",
                  "\n    - R (Reset) : Momentanes Level neustarten",
                  "\n    - N (New) : Komplettest Spiel von neuem starten",
                  "\n    - J (Jump) : Zu gewuenschtem Level springen",
                  "\n    - Pfeiltaste Links : Zum vorigen Level springen",
                  "\n    - Pfeiltaste Rechts : Zum naechsten Level springen")

        if e.key() == Qt.Key_Escape:
            """ Esc druecken um Fenster zu schliessen """
            self.close()

        if e.key() == Qt.Key_R:
            """ R druecken um Level neuzustarten """
            self.levelReset()
            self.update()

        if e.key() == Qt.Key_N:
            """ N druecken um Spiel neuzustarten """
            self.gameReset()
            self.levelCounter = 0
            self.update()

        if e.key() == Qt.Key_J:
            """ J druecken um zu gewuenschtem Level zu springen """
            try:
                jumpTarget = int(input("Nummer des Levels: "))
                if 0 <= jumpTarget <= self.maxLevel:    # pruefen ob vorhandenes Level eingegeben wurde
                    self.gameReset()
                    self.levelCounter = jumpTarget
                else:
                    print("Fehler! Eingabe war kein Index eines bestenden Levels")
            except ValueError:      # Fehler abfangen, falls kein Int eingegeben wurde
                print("Fehler! Eingabe war nicht von Typ Int")

        if e.key() == Qt.Key_Left:
            """ Pfeiltaste Links druecken um ein Level zurueck zu springen """
            if self.levelCounter == 0:
                print("Fehler! Erstes Level wird bereits angezeigt")
            else:
                self.levelReset()   # momentanes Level zuruecksetzen
                self.levelCounter -= 1
                self.levelReset()   # voriges Level zuruecksetzen
                self.update()

        if e.key() == Qt.Key_Right:
            """ Pfeiltaste Rechts druecken um zum naechsten Level zu springen """
            if self.levelCounter == self.maxLevel:
                print("Fehler! Letztes Level wird bereits angezeigt")
            else:
                self.levelReset()   # momentanes Level zuruecksetzen (unnoetig, aber "schoener")
                self.levelCounter += 1
                self.update()



    def mousePressEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        #print("               ", pos.x(), pos.y())

        if self.levels[self.levelCounter].beruehrt(pos.x(), pos.y()):
            self.update()


    def initalisierung(self):
        """ Anfaengliche Erstellung der Level
        Koordinaten sollten bestenfalls keine genauen Zahlen sein, sondern immer in Abhaengigkeit der Fenstergroesse """

        level1 = Levelstruktur(self)
        for j in range(3):
            for i in range(2):
                level1.rechteck_hinzufuegen(Rechteck(self.wW / 16 + self.wW * (3 / 16) * i,
                                                     self.wW / 16 + self.wW * (3 / 16) * j,
                                                     self.wW / 8, self.wW / 8, QColor(0, 90, 0)))

        level2 = Levelstruktur(self)
        for j in range(3):
            for i in range(2):
                level2.kreis_hinzufuegen(Kreis(self.wW / 16 + self.wW * (3 / 16) * i,
                                                     self.wW / 16 + self.wW * (3 / 16) * j,
                                                     self.wW / 8, self.wW / 8, QColor(0, 90, 0)))

        level3 = Levelstruktur(self)
        for j in range(2):
            for i in range(1):
                level3.rechteck_hinzufuegen(Rechteck(self.wW / 16 + self.wW * (3 / 16) * (i + 2),
                                                     self.wW / 12 + self.wW * (3 / 16) * (j + 2),
                                                     self.wW / 8, self.wW / 8, QColor(0, 90, 0)))

        # alle Level separat in originalLevels abspeichern fuers zuruecksetzen
        self.originalLevels = [level1, level2, level3]
        self.levels = [level1.kopieren(), level2.kopieren(), level3.kopieren()]

    def levelReset(self, level: int = -1):
        """ Ein spezielles Level zuruecksetzen
        wird der Parameter frei gelassen, wird das momentane Level zurueckgesetzt """
        if level == -1:
            level = self.levelCounter
        if 0 <= level <= self.maxLevel:
            self.levels[level] = self.originalLevels[level].kopieren()
        else:
            pass

    def gameReset(self):
        """ Alle Level zuruecksetzen
        simple Implementation: levelReset auf jedes Level angewandt """
        for i in range(self.maxLevel):
            self.levelReset(i)

    def nextLevel(self):
        self.levelCounter += 1
        self.levelGewonnen = True




app = QApplication(sys.argv)
ex = Window()
sys.exit(app.exec_())
