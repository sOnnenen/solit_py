# solit_py

# Bestärkendes Lernen am Beispiel von (Peg)Solitär 

Diese README Datei soll eine Übersicht über den im Rahmen des Projekts geschriebenen Code geben, 
damit dieser einfach verwendet, geändert und/oder darauf aufgebaut werden kann.

Zunächst empfiehlt es sich mit Solitär vertraut zu machen.

# Wie wird Solitär gespielt

Gespielt wird auf einem Spielbrett, auf dem Spielfiguren oder Steine nebeneinander verteilt sind. Vor dem Start wird ein Stein entfernt. Aufgabe ist es durch Sprünge am Ende so wenig Steine wie möglich zu hinterlassen, idealerweise nur noch ein Stein in der Mitte des Spielbretts. Es darf immer nur über einen Stein gesprungen werden und der übersprungene Stein entfernt werden. Mögliche Zugrichtungen hängen von der Variante des Spielbretts ab. Beim klassischen Solitär (Englisches Brett), darf horizontal und vertikal gezogen werden. Es gibt zahlreiche Varianten (http://www.onlinesologames.com/peg-solitaire), wobei sich in diesem Projekt auf das Englische Brett, Dreieck und Raute beschränkt wurde.

# Wichtige Files

***SimWorld.py:***

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

***Q_Agent.py:***

Diese File beinhaltet die Klasse *QLearner(alpha,gamma,epsilon,epsilon_decay,alpha_decay,name)*. Sie stellt den Agenten auf Basis des Q-Learning Algorithmuses dar. *alpha* ist die Learning Rate, *gamma* der Discount und *epsilon* die Exploration Rate. *epsiolon_decy* und *alpha_decay* geben an wie schnell *epsilon* bzw. *alpha* absinken und sind optional. Soll *epsilon* oder *alpha* nicht kleiner werden, dann muss der jeweilige Decay Null sein. *name* gibt den Namen der Q-Table File an. Nachfolgend werden die wichtigste Methoden für den Agenten aufgelistet.

-*update_epsilon()*: Aktualisiert den Wert von *epsilon*, falls *epsilon_decay* ungleich Null.

-*update_alpha()*: Aktualisiert den Wert von *alpha*, falls *alpha_decay* ungleich Null.

-*get_next_action(state,actions)*: Gibt die nächste Aktion zurück. Diese wird abhängig von *epsilon* entweder zufällig oder optimiert gewählt.

-*train_agent(sate,actions,chosen_action,prev_state,game_over)*: Aktualisiert die Q-Table.

So wird der Agent erzeugt:
```bash
import Q_Agent

Agent=Q_Agent.QLearner(0.5,0.5,0.01,0.01,'Table')
```
So würde ein Spielzug mit Aktualisierung der Q-Table aussehen:
```bash
Aktion=Agent.get_next_action(Brett.get_board_view(),Brett.get_actions())
Brett.take_action(Aktion)
Agent.train_agent(Brett.get_board_view(),Brett.get_actions(),Aktion,Brett.get_previous_state(),Brett.in_final_state())
Agent.update_epsilon()
Agent.update_alpha()
```

Die Reward Function, die festlegt wie die Züge belohnt werden, kann in der File über *ACTIVE_FUNCTION* gändert werden zwischen *'normalized_reward'*, *'strict_reward'* und *'tactical_reward'*.

***display.py:***

Diese File lernt einen Agent für ein Spielbrett. Die File erstellt dann zwei Plots. Der erste Plot zeigt die Anzahl der verbleibenden Pins über die Episoden und der zweite Plot den erhaltenen Reward über die Episoden. Die Anzahl der Episoden kann über *EPISODES* geändert werden. *SHOW_EVERY* gibt an nach welcher Anzahl an Episoden die grafische Darstellung erfolgen soll. Dazu muss *show_games* noch auf Eins gesetzt werden. Über *AVERAGE* kann angegeben werden über wie viele Episoden immer gemittelt wird.

# Ein neues Solitär Brett Klasse implementieren (Beispiel Pinguin Brett)

#### Zunächst wird die Klasse mit init Funktion erstellt: 
Das Pinguin Brett ist wird mit analog zum englischen Brett und zum Dreieck Brett erstellt. Die Größe ist auf 5 festgelegt und als shape wird "Triangular" verwendet.
#### Danach muss noch das Spielbrett bevölkert werden:
Dazu verwendet man die modifizierte Version der populate_board() Funktion des Englischen Bretts.
Jede Zelle bekommt dabei Koordinaten entsprechen des transformierten Pinguin Bretts. Siehe nachstehende Grafik.

![Pinguin](/images/Pinguin.png)

#### Anschließend muss noch die set_neighbor_pairs Funktion des Dreieck Bretts übernommen werden und fertig ist die Pinguin Klasse: 

Um diese zu testen muss man lediglich, in der display.py Funktion das Pinguin Brett verwenden.
```bash
NAME = "Pinguin_test"
# weiterer Code
Brett = SimWorld.py.Penguin()
Brett.populate_board()
Brett.board_array[2][1].set_value(0)
```


