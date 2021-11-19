class Relative:
    """Enumerativ klasse for relative retninger"""
    FORWARD = "FORWARD"
    RIGHT = "RIGHT"
    BACK = "BACK"
    LEFT = "LEFT"
    _directions = [FORWARD, RIGHT, BACK, LEFT]

    def value(relative):
        return Relative._directions.index(relative)

    def get(value: int):
        return Relative._directions[value%4]

class Cardinal:
    """Enumerativ klasse for himmelretninger"""
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"
    _directions = [NORTH, EAST, SOUTH, WEST]

    def value(cardinal):
        return Cardinal._directions.index(cardinal)

    def get(value: int):
        return Cardinal._directions[value%4]

    def turn(cardinal, relative):
        """Returnerer himmelretningen som er i direction retning fra self"""
        return Cardinal.get(Cardinal.value(cardinal)+Relative.value(relative))

    def relation(cardinal1, cardinal2):
        """Returnerer forholdet (en relativ retning) mellom denne himmelretningen og en annen."""
        return Relative.get((Cardinal.value(cardinal2)-Cardinal.value(cardinal1))%4)

    def reverse(cardinal):
        """Tilsvarer self.turn(Relative.BACK).  Returnerer den motsatte himmelretningen av denne."""
        return Cardinal.turn(cardinal, Relative.BACK)
