# solit_py

# Bestärkendes Lernen am Beispiel von (Peg)Solitär 

Diese README Datei soll eine Übersicht über den im Rahmen des Projekts geschriebenen Code geben, 
damit dieser einfach verwendet, geändert und/oder darauf aufgebaut werden kann.

Zunächst empfiehlt es sich mit Solitär vertraut zu machen.

# Wie wird Solitär gespielt

Gespielt wird auf einem Spielbrett, auf dem Spielfiguren oder Steine nebeneinander verteilt sind. Vor dem Start wird ein Stein entfernt. Aufgabe ist es durch Sprünge am Ende so wenig Steine wie möglich zu hinterlassen, idealerweise nur noch ein Stein in der Mitte des Spielbretts. Es darf immer nur über einen Stein gesprungen werden und der übersprungene Stein entfernt werden. Mögliche Zugrichtungen hängen von der Variante des Spielbretts ab. Beim klassischen Solitär (Englisches Brett), darf horizontal und vertikal gezogen werden. Es gibt zahlreiche Varianten (http://www.onlinesologames.com/peg-solitaire), wobei sich in diesem Projekt auf das Englische Brett, Dreieck und Raute beschränkt wurde.

# Wichtige Files

*SimWorld.py*:
Diese File stellt die Spielbretter und die Spielfiguren bereit, in den Klassen *English()*, *Triangular(n)*, *Diamond(n)*. n steht für die Größe der Kantenlänge der beiden Spielbretter Dreieck und Raute. Das Englische Spielbrett hat eine feste Größe, die nicht geändert werden kann. Für die Spielfiguren bzw. den Zellen auf dem Spielbrett steht die Klasse *Cell(value,row,column)* bereit, wobei *value=1* bedeutet, dass auf Zelle (*row,column*) eine Spielfigur steht. *value=0* bedeutet, dass hier keine Spielfigur steht. Nachfolgend werden die wichtigsten Methoden für die Spielbretter aufgelistet.

-*populate_board()*: Setzt Zellen (Spielsteine) auf das Spielbrett und muss vor dem Spielen aufgerufen werden.

-*set_neighbor_pairs()*: Erstellt Liste von benachbarten Zellen zu den einzelnen Steinen und dient zur späteren Berechnung der möglichen Züge (Aktionen) und muss vor dem Spielen aufgerufen werden.

-*get_actions()*: Liefert eine Liste an möglichen Aktionen zurück.

-*in_final_state()*: Prüft, ob keine Aktionen mehr möglich sind.

-*get_sample_action()*: Gibt eine zufällige, mögliche Aktion zurück.

-*take_action(action)*: Macht den Zug, der in *action* steht.

-*get_board_view()*: Gibt das momentane Spielbrett als 2D-Array zurück und dient als Zustand für späteres lernen.

-*get_previous_state()*: Gibt den letzten Zustand des Spielbretts zurück.

Ein Beispiel für das erzeugen eines Spielbretts:
```bash
import SimWorld

Brett=SimWorld.English()
Brett.populate_board()
Brett.set_neighbor_pairs()
```
So würde man einen zufälligen Zug machen:
```bash
Aktion=Brett.get_sample_action()
Brett.take_action(Aktion)
```
So einen aus der Liste der möglichen Züge:
```bash
Zug_Liste=Brett.get_actions()
Brett.take_action(Zug_Liste[3])
```
