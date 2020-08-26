import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen, QImage, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QEvent, QRect, QPointF, QPropertyAnimation, QTimer
import functionsBib as fb
import settings
from classes import Rechteck, Kreis, Levelstruktur, List


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.wW : int = settings.BREITE                 # windowWidth ; Fenster ist immer quadratisch
        self.setGeometry(600, 150, self.wW, self.wW)
        self.setWindowTitle("Spaß mit grünem")
        self.originalLevels : List[Levelstruktur] = []  # Speicher fuer urspruengliche Level (relevant beim level reset)
        self.levels : List[Levelstruktur] = []          # Speicher fuer Level
        self.levelCounter : int = 0                     # Index des momentan zu bearbeitendem Level
        self.maxLevel : int = settings.ANZAHLLEVEL      # den maximal zu erreichenden Index der level-Liste
        self.levelGewonnen : bool = False

        self.initalisierung()
        self.keyPressEvent = self.fn

        self.show()


    def paintEvent(self, event) -> None:
        # Hintergrund zeichnen
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 180, 0), 1, Qt.SolidLine))
        painter.fillRect(0, 0, self.wW, self.wW, QColor(0, 160, 0))

        # Nummer des derzeitigen Levels oben schreiben
        rect1 = QRect(int(self.wW / 2), int(self.wW / 100), int(self.wW / 20), int(self.wW / 20))
        painter.setPen(QPen(QColor(0, 40, 0), 1, Qt.SolidLine))
        painter.setFont(QFont("Times", int(self.wW / 32)))
        painter.drawText(rect1, 0, str(self.levelCounter))

        if self.levelGewonnen:
            if self.levelCounter > self.maxLevel:
                print("Glueckwunsch, du hast alle Level abgeschlossen")
                self.close()

            # Kurzer Übergang zum nächsten Level, verschwindet nach 3 Sekunden
            rect2 = QRect( 0, int(self.wW / 2.5), self.wW, int(self.wW / 2) )
            painter.setPen(QPen(QColor(0, 40, 0), 1, Qt.SolidLine))
            painter.setFont(QFont("Times", int(self.wW / 22)))
            painter.drawText(rect2, 4, "Glückwunsch,\n "
                                       "du hast Level " + str(self.levelCounter - 1) + " geschafft")
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


    def fn(self, e) -> None:

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


    def mousePressEvent(self, QMouseEvent) -> None:
        pos = QMouseEvent.pos()
        #print("               ", pos.x(), pos.y())

        if self.levels[self.levelCounter].beruehrt(pos.x(), pos.y()):
            self.update()


    def initalisierung(self) -> None:
        """ Anfaengliche Erstellung der Level """

        level0 : Levelstruktur = fb.level0Erstellen(self)
        level1 : Levelstruktur = fb.level1Erstellen(self)
        level2 : Levelstruktur = fb.level2Erstellen(self)
        level3 : Levelstruktur = fb.level3Erstellen(self)

        # alle Level separat in originalLevels abspeichern fuers zuruecksetzen
        self.originalLevels = [level0, level1, level2, level3]
        self.levels = [level0.kopieren(), level1.kopieren(), level2.kopieren(), level3.kopieren()]

    def levelReset(self, levelNummer: int = -1) -> None:
        """ Ein spezielles Level zuruecksetzen
        wird der Parameter frei gelassen, wird das momentane Level zurueckgesetzt """
        if levelNummer == -1:
            levelNummer = self.levelCounter
        if 0 <= levelNummer <= self.maxLevel:
            self.levels[levelNummer] = self.originalLevels[levelNummer].kopieren()
        else:
            print("Die Eingabe ist Schwachsinn")

    def gameReset(self) -> None:
        """ Alle Level zuruecksetzen
        simple Implementation: levelReset auf jedes Level angewandt """
        for i in range(self.maxLevel + 1):
            self.levelReset(i)

    def nextLevel(self) -> None:
        self.levelCounter += 1
        self.levelGewonnen = True




app = QApplication(sys.argv)
ex = Window()
sys.exit(app.exec_())
