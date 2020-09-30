import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPolygon
from PyQt5.QtCore import Qt, QRect, QTimer
import functionsBib as fb
import settings
from classes import Levelstruktur, List
from sounddevice import play
from soundfile import read


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.wW : int = settings.BREITE                 # windowWidth ; Fenster ist immer quadratisch
        self.setGeometry(600, 150, self.wW, self.wW)
        self.setWindowTitle("Spaß mit grünem")
        self.originalLevels : List[Levelstruktur] = []  # Speicher fuer urspruengliche Level (relevant beim level reset)
        self.levels : List[Levelstruktur] = []          # Speicher fuer Level
        self.levelCounter : int = 1                     # Index des momentan zu bearbeitendem Level
        self.maxLevel : int = 0                         # den maximal zu erreichenden Index der level-Liste
        self.levelGewonnen : bool = False
        self.spielGewonnen : bool = False
        self.gewonneneLevel : List[bool] = [None]

        self.initalisierung()
        self.keyPressEvent = self.fn

        self.debugKoordinatenPrinten : bool = False

        if settings.MUSIK:
            self.musikAnmachen()

        self.show()


    def paintEvent(self, event) -> None:
        # Hintergrund zeichnen
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 180, 0), 1, Qt.SolidLine))
        painter.fillRect(0, 0, self.wW, self.wW, QColor(0, 160, 0))

        # Variable, damit der QTimer zeitlich vom aufleuchten und End-Screen getrennt ist.
        # Wenn es diese nicht gaebe, wuerde der End-Screen so lange wie das aufleuchten angezeigt werden
        warte : bool = False

        # Level zeichnen
        # sonstiges unter Formen zeichnen
        self.levels[self.levelCounter].weiteresZeichnenVorher(painter, self)
        # Rechtecke und Kreise einzeichnen
        painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))      # Umrandung der Kreise
        for form in self.levels[self.levelCounter].enthalteneFormen:
            if form.sichtbar:

                # Fuers rotieren
                painter.translate(form.mittelpunkt[0], form.mittelpunkt[1])
                painter.rotate(form.rotation)
                # Falls es aufleuchten soll, wird die Flaeche fuer eine gewisse Zeit weiss gefaerbt
                if form.aufleuchten:
                    painter.setBrush(settings.AUFLEUCHTFARBE)
                    QTimer.singleShot(settings.AUFLEUCHTZEIT, self.update)
                    form.aufleuchten = False
                    warte = True
                else:
                    painter.setBrush(form.farbe)
                # Falls Rechteck
                if form.welcheForm == 1:
                    painter.drawRect(form.xRelZuMitte, form.yRelZuMitte, form.weite, form.hoehe)
                # Falls Kreis
                elif form.welcheForm == 2:
                    painter.drawEllipse(form.xRelZuMitte, form.yRelZuMitte, form.weite, form.hoehe)
                # Falls Polygon
                elif form.welcheForm == 3:
                    painter.drawPolygon(QPolygon(list(form.eckpunkteRelZuMitte)))
                # Fuers rotieren
                painter.rotate(- form.rotation)
                painter.translate(- form.mittelpunkt[0], - form.mittelpunkt[1])
        # sonstiges ueber Formen zeichnen
        self.levels[self.levelCounter].weiteresZeichnenNachher(painter, self)

        # Nummer des derzeitigen Levels oben schreiben
        rect1 = QRect(0, int(self.wW / 100), self.wW, int(self.wW / 20))
        painter.setPen(QPen(QColor(0, 40, 0), 1, Qt.SolidLine))
        painter.setFont(QFont("Times", int(self.wW / 32)))
        if self.levelCounter == 0:
            painter.drawText(rect1, 4, "Interface")
        else:
            painter.drawText(rect1, 4, str(self.levelCounter))

        # Glueckwuensche, falls Level beendet wurde
        if not warte and self.levelGewonnen:
            # Kurzer Übergang zum nächsten Level, verschwindet nach paar Sekunden
            rect2 = QRect( 0, int(self.wW / 2.5), self.wW, int(self.wW / 2) )
            painter.setPen(QPen(QColor(0, 40, 0), 1, Qt.SolidLine))
            painter.setFont(QFont("Times", int(self.wW / 22)))
            painter.drawText(rect2, 4, "Glückwunsch,\n "
                                       "du hast Level " + str(self.levelCounter) + " geschafft")
            # pruefen ob es das letzte Level ist
            if self.levelCounter < self.maxLevel:
                QTimer.singleShot(settings.UEBERGANGSZEIT, self.update)
                self.levelGewonnen = False
                self.levelCounter += 1

            # Falls letztes Level und Endscreen noch nicht angezeigt wird, kommt noch einmal der Glueckwunsch-Screen
            elif not self.spielGewonnen:
                QTimer.singleShot(settings.UEBERGANGSZEIT, self.update)
                self.spielGewonnen = True
            # falls Spiel vorbei, eigener Gewinnscreen
            elif self.spielGewonnen:
                painter.fillRect(0, 0, self.wW, self.wW, QColor(0, 160, 0))
                rect3 = QRect(0, 0, self.wW, self.wW)
                painter.setFont(QFont("Times", int(self.wW / 22)))
                painter.drawText(rect3, 4, "Sehr gut!\n"
                                           "Du hast alle Level\n"
                                           "erfolgreich abgeschlossen\n\n")
                rect4 = QRect(0, int(self.wW / 3), self.wW, self.wW)
                painter.setFont(QFont("Times", int(self.wW / 55)))
                painter.drawText(rect4, 4,"Credits\n"
                                           "Creative Director:  Cedesc\n"
                                           "Production Director:  Cedesc\n"
                                           "Game Director:  Cedesc\n"
                                           "Technology Director:  Cedesc\n"
                                           "Art Director:  Cedesc\n"
                                           "Narrative Director:  Cedesc\n"
                                           "Story By:  Cedesc\n"
                                           "Lead Programmer:  Cedesc\n"
                                           "Technical Architect:  Cedesc\n"
                                           "Geiler Typ: Cedesc\n"
                                           "Camera Specialist:  Cedesc\n"
                                           "Lead Level Designer:  Cedesc\n"
                                           "Build Master:  Cedesc\n"
                                           "Music Composition:  Re_ii\n"
                                           "Lead Development Tester:  Cedesc\n"
                                           "Production Manager:  Cedesc\n"
                                           "Territory Manager:  Cedesc\n"
                                           "Production Support Coordinator:  Cedesc\n")

                print("Das Spiel wurde erfolgreich abgeschlossen.\n"
                      "Druecke Esc um das Fenster zu schliessen.")
            return


    def fn(self, e) -> None:

        # Im Endscreen sind Tastenbelegungen nicht vorgesehen, deshalb vorab dies zum Abfangen
        if self.spielGewonnen and e.key() != Qt.Key_Escape:
            print("Das Spiel ist zuende, Eingaben ausser Esc funktionieren hier nicht")
            return

        # Keybindings fuers Debuggen
        if e.key() == Qt.Key_1:
            print("- Debug-Hilfen :",
                  "\n    - 2 (Position printen) : Position des Klicks printen An",
                  "\n    - 3 (Drehen Links) : (Die erste) Form des Levels nach links drehen",
                  "\n    - 4 (Drehen Rechts) : (Die erste) Form des Levels nach rechts drehen",
                  "\n    - 5 (Alles faerben) : Alle Formen korrekt faerben",
                  "\n    - 8 : self.gewonnenenLevel anzeigen")
        if e.key() == Qt.Key_2:
            if not self.debugKoordinatenPrinten:
                print("Position des Klicks wird ab jetzt geprintet")
                self.debugKoordinatenPrinten = True
        if e.key() == Qt.Key_3:
            self.levels[self.levelCounter].enthalteneFormen[0].rotation -= 1
            self.update()
        if e.key() == Qt.Key_4:
            self.levels[self.levelCounter].enthalteneFormen[0].rotation += 1
            self.update()
        if e.key() == Qt.Key_5:
            self.levels[self.levelCounter].alleRichtigFaerben()
            self.update()
        if e.key() == Qt.Key_8:
            print(self.gewonneneLevel)


        if e.key() == Qt.Key_H:
            """ H druecken um Tastenbelegung anzuzeigen """
            print("- Steuerung :",
                  "\n    - H (Hilfe) : Steuerung anzeigen",
                  "\n    - Esc (Escape) : Fenster schliessen",
                  "\n    - R (Reset) : Momentanes Level neustarten",
                  "\n    - N (New) : Komplettes Spiel von neuem starten",
                  "\n    - J (Jump) : Zu gewuenschtem Level springen",
                  "\n    - Links : Zum vorigen Level springen",
                  "\n    - Rechts : Zum naechsten Level springen",
                  "\n    - Leertaste : Zum Interface springen")

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
            # Liste der gewonnenen Level zuruecksetzen
            self.gewonneneLevel = [None]
            for i in range(self.maxLevel - 1):
                self.gewonneneLevel.append(False)
            # Auf erstes Level zuruecksetzen
            self.levelCounter = 1
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
            if self.levelCounter == 1:
                print("Erstes Level wird bereits angezeigt")
            elif self.levelCounter == 0:
                print("Interface wird angezeigt, nicht moeglich zum vorigen Level zu springen")
            else:
                self.levelReset()   # momentanes Level zuruecksetzen
                self.levelCounter -= 1
                self.levelReset()   # voriges Level zuruecksetzen
                self.update()

        if e.key() == Qt.Key_Right:
            """ Pfeiltaste Rechts druecken um zum naechsten Level zu springen """
            if self.levelCounter == self.maxLevel:
                print("Letztes Level wird bereits angezeigt")
            elif self.levelCounter == 0:
                print("Interface wird angezeigt, nicht moeglich zum naechsten Level zu springen")
            else:
                self.levelReset()   # momentanes Level zuruecksetzen (unnoetig, aber "schoener")
                self.levelCounter += 1
                self.update()

        if e.key() == Qt.Key_Space:
            """ Leertaste druecken um zum Interface zu springen """
            self.levelReset()   # momentanes Level zuruecksetzen (unnoetig, aber "schoener")
            self.levelCounter = 0
            self.update()

        if e.key() == Qt.Key_Y:
            """ Fuer Steuerung im Level """
            momentanesLevel : Levelstruktur = self.levels[self.levelCounter]
            if momentanesLevel.tastenGesteuert:
                momentanesLevel.internerSpeicherL[0](momentanesLevel)
                self.update()

        if e.key() == Qt.Key_X:
            """ Fuer Steuerung im Level """
            momentanesLevel : Levelstruktur = self.levels[self.levelCounter]
            if momentanesLevel.tastenGesteuert:
                momentanesLevel.internerSpeicherL[1](momentanesLevel)
                self.update()


    def mousePressEvent(self, QMouseEvent) -> None:
        pos = QMouseEvent.pos()
        if self.debugKoordinatenPrinten:
            print("               ", pos.x(), pos.y())

        if self.levels[self.levelCounter].beruehrt(pos.x(), pos.y()):
            self.update()


    def musikAnmachen(self) -> None:
        data, fs = read(settings.MUSIKTRACK, dtype='float32')
        play(data, fs)

    def initalisierung(self) -> None:
        """ Anfaengliche Erstellung der Level """

        level00 : Levelstruktur = fb.level0Erstellen(self)
        level01 : Levelstruktur = fb.level1Erstellen(self)
        level02 : Levelstruktur = fb.level2Erstellen(self)
        level03 : Levelstruktur = fb.level3Erstellen(self)
        level04 : Levelstruktur = fb.level4Erstellen(self)
        level05 : Levelstruktur = fb.level5Erstellen(self)
        level06 : Levelstruktur = fb.level6Erstellen(self)
        level07 : Levelstruktur = fb.level7Erstellen(self)
        level08 : Levelstruktur = fb.level8Erstellen(self)
        level09 : Levelstruktur = fb.level9Erstellen(self)
        level10 : Levelstruktur = fb.level10Erstellen(self)
        level11 : Levelstruktur = fb.level11Erstellen(self)
        level12 : Levelstruktur = fb.level12Erstellen(self)
        level13 : Levelstruktur = fb.level13Erstellen(self)
        level14 : Levelstruktur = fb.level14Erstellen(self)
        level15 : Levelstruktur = fb.level15Erstellen(self)
        level16 : Levelstruktur = fb.level16Erstellen(self)
        level17 : Levelstruktur = fb.level17Erstellen(self)
        level18 : Levelstruktur = fb.level18Erstellen(self)
        level19 : Levelstruktur = fb.level19Erstellen(self)

        # alle Level separat in originalLevels abspeichern fuers zuruecksetzen
        self.originalLevels = [None   , level01, level02, level03, level04,
                               level05, level06, level07, level08, level09,
                               level10, level11, level12, level13, level14,
                               level15, level16, level17, level18, level19,
                               level00]

        # hoechstes Level festlegen
        self.maxLevel = len(self.originalLevels) - 1

        # Liste ob Level gewonnen wurden initialisieren
        for i in range(self.maxLevel):
            self.gewonneneLevel.append(False)
        print(len(self.gewonneneLevel))
        print(self.gewonneneLevel)

        # Interface spaeter hinzufuegen, da dort das maxLevel benoetigt wird
        interface : Levelstruktur = fb.interfaceErstellen(self)
        self.originalLevels[0] = interface

        # fuer jedes Level eine Kopie in self.levels erstellen, die letztlich die spielbaren Level sind
        for lev in self.originalLevels:
            self.levels.append(lev.kopieren())


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
        """ Alle Level zuruecksetzen """
        # levelReset auf jedes Level angewandt
        for i in range(self.maxLevel + 1):
            self.levelReset(i)





app = QApplication(sys.argv)
ex = Window()
sys.exit(app.exec_())
