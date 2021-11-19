from direction import *

class Way:
    """Objekter av klassen definerer en strekning og en himmelretning"""

    def __init__(self, cardinal, length: int):
        self._direction = cardinal
        self._length = length

    def get_direction(self):
        return self._direction

    def get_length(self):
        return self._length

    def add(self, distance: int):
        """Legger en strekning distance til lengden på self.
        Negative strekninger kan legges til. Om den totale lengden blir negativ endres himmelretningen."""
        self._length += distance
        if self._length < 0:
            self._length *= -1
            self._direction = Cardinal.reverse(self._direction)

    def reversed(self):
        """Returnerer en Way med motsatt retning"""
        return Way(Cardinal.reverse(self._direction), self._length)

    def __str__(self):
        return self._direction + ": " + str(self._length)

class Track:
    """Lagrer en sekvens med Ways."""
    def __init__(self):
        self._track = []

    def add(self, cardinal, length: int):
        """Legger en strekning til tracken"""
        way = Way(cardinal, length)
        if len(self._track) == 0:
            self._track.append(way)
        else:
            last = self._track[-1]
            relation = Cardinal.relation(last.get_direction(), way.get_direction())
            if relation == Relative.FORWARD:
                last.add(way._length)
            elif relation == Relative.BACK:
                last.add(-way._length)
                if last.get_length() == 0:
                    self._track.remove(last)
            else:
                self._track.append(way)

    def distance(self):
        """Returnerer summen av alle strekning i self"""
        sum = 0
        for way in self._track:
            sum += way.get_length()
        return sum

    def cardinal(self, index):
        """Returnerer retninga på strekninga på index"""
        return self._track[index].get_direction()

    def length(self, index):
        """Returnerer lengden på strekninga på index"""
        return self._track[index].get_length()

    def __len__(self):
        return len(self._track)

    def __str__(self):
        s = ""
        for way in self._track:
            s += str(way) + "\n"
        return s

class Tracker:
    """Definerer et objekt som kan tracke en robots bevegelse."""

    def __init__(self, orientation = Cardinal.NORTH):
        self._orientation = orientation
        self._track = Track()

    def turn(self, relative):
        """Snur trackerens orientering"""
        self._orientation = Cardinal.turn(self._orientation, relative)

    def right(self):
        """Snur trackeren mot høyre"""
        self.turn(Relative.RIGHT)

    def left(self):
        """Snur trackeren mot venstre"""
        self.turn(Relative.LEFT)

    def back(self):
        """Snur trackeren rundt"""
        self.turn(Relative.BACK)

    def distance(self):
        """Regner ut den totale strekningen som er tracket.
        Returnerer strekningen som en int i mm."""
        return self._track.distance()
    
    def tracklength(self):
        """Regner ut det totale antallet strekninger som er blitt kjørt."""
        return len(self._track)

    def move(self, distance: int):
        """Beveger trackeren distance rett fram (utfra trackerens orientering)."""
        self._track.add(self._orientation, distance)

    def backtrack(self):
        """Returnerer den neste handlinga som må gjøres for å kunne gjøre tilbake langs track."""
        drx = Cardinal.reverse(self._track.cardinal(-1))
        if drx != self._orientation:
            return Cardinal.relation(self._orientation, drx)
        else:
            return self._track.length(-1)

    def __str__(self):
        return "Orientation: " + self._orientation + "\n" + str(self._track)