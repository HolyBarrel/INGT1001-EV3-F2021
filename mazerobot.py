#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from tracker import *
from direction import Relative
from pybricks.media.ev3dev import SoundFile
from math import ceil, floor

class MazeRobot:
    """
    Objekter av klassen har metoder som lar en robot bevege seg, og finne vegen gjennom en labyrint
    """
    debug = True
    wheel_diam = 56  # Diameter på hjula. Klassevariabel
    axle_track = 127  # Avstand mellom hjula. Klassevariabel
    right_right = 120 # Hvor mange millimeter roboten kjører fram og til høyre i en sving
    right_front = 160 
    ideal_distance = 75 # Hvor langt unna kan vegger være?
    wall_sensitivity = 75
    finish_color = Color.RED # Farge på målstreken
    inch = 20 # Hvor mange millimeter roboten kjører av gangen
    length_adjust = 1 # Skaleringsfaktor for backtracking

    
    def __init__(self, left_port, right_port, head_port, us_port, cs_port):
        """
        __init__ -> MazeRobot
        Konstruktør for klassen, som tar inn portplassering av den gjeldende
        robotens porter og konstruerer et objekt av klassen 'MazeRobot'
        Dette objektet arver axle_track og wheel_diam som klassevariabler
        og danner nye objektvariabler gitt i konstruktøren
        @params left_port, right_port, head_port, us_port
        
        """    

        self.left_motor = Motor(left_port)
        self.right_motor = Motor(right_port)
        self.head = Motor(head_port, positive_direction=Direction.COUNTERCLOCKWISE)
        self.sensor = UltrasonicSensor(us_port)
        self.color_sensor = ColorSensor(cs_port)
        self.base = DriveBase(self.left_motor, self.right_motor, wheel_diameter = MazeRobot.wheel_diam, axle_track = MazeRobot.axle_track)
        self.tracker = Tracker()
        self.ev3 = EV3Brick()
        self.ev3.speaker.set_speech_options(language='no', voice='f5')
    

    """
    ================================================
    -- Grunnleggende metoder for robotbevegelse
    ================================================
    """
    def drive(self, distance):
        """Kjører 200 mm (20cm) rett fram."""

        self.base.straight(distance)
        self.tracker.move(floor(distance/MazeRobot.length_adjust))
     
    def turn_right(self):
        """Roboten roterer 90 grader mot høyre"""
        
        self.base.turn(90)
        self.tracker.right()
    
    
    def turn_left(self):
        """Roboten roterer 90 grader mot venstre"""

        self.base.turn(-90)
        self.tracker.left()
    
    def turn_back(self):
        """Roboten snur 180 grader"""
        self.base.turn(-180)
        self.tracker.back()
    
    """
    ================================================
    -- Metoder for styring av ultralydsensor
    ================================================
    """

    def turn_head(self, deg):
        """
        Snur huet til en vinkel deg fra normal.
        (Positiv retning mot høyre)
        """
        # Snur huet med mål deg grader fra normal
        # Hastighet 180 grader i sekundet
        self.head.run_target(180, deg-90)
    
    def turn_head_right(self):
        """
        Snur huet mot høyre (90 grader)
        """
        #Snur hodet 90 grader mot høyre
        self.turn_head(90)
    
    
    def turn_head_straight(self):
        """
        Snur huet rett fram
        """
        #Snur hodet rett fram
        self.turn_head(0)
    
    def _distance(self):
        return self.sensor.distance()

    def _sees_wall(self, distance):
        """
        Returnerer True om sensoren kan se noe som er nærmere enn distance mm.
        """
        return (self._distance() <= distance)
    
    
    def _distance_front(self):
        """Snur huet rett fram og returnerer avstanden til veggen"""
        self.turn_head_straight()
        return self._distance()
    
    def _distance_right(self):
        self.turn_head_right()
        return self._distance()

    def _check_right(self):
        """
        Snur huet til høyre og kikker etter vegger
        Returnerer True om den har sett en vegg.
        """
        return self._distance_right() <= (MazeRobot.ideal_distance + MazeRobot.right_right) # Er det en vegg der?
    
    
    def _check_front(self):
        """
        Snur huet rett fram og kikker etter vegger
        Returnerer True om den har sett en vegg.
        """
        return self._distance_front() <= MazeRobot.wall_sensitivity
    
    """
    ================================================
    -- Diverse
    ================================================
    """
    
    def print(self, something):
        """Skriver ut en beskjed på ev3-skjermen"""
        self.ev3.screen.print(something)
    
    def _sees_finish_line(self):
        """Sjekker om fargesensorer ser mållinja"""
        #if MazeRobot.debug: print("sees_finish_line")
        color = self.color_sensor.color()
        return color == MazeRobot.finish_color
    
    def celebrate(self):
        self.ev3.speaker.play_file(SoundFile.FANFARE)
    
    def speak(self, message):
        self.ev3.speaker.say(message)
    
    """
    ================================================
    -- Metoder for navigering
    ================================================
    """

    def _adjust(self):
        distance = self._distance_right()
        maximum = 2*MazeRobot.ideal_distance
        if distance < maximum:
            turn_angle = floor((distance/MazeRobot.ideal_distance - 1)*45)
            self.base.turn(turn_angle)

    def _nudge(self):
        self.drive(MazeRobot.inch)
        #self._adjust()

    def _enter_right(self):
        """Kjører inn i en åpning til høyre"""
        if MazeRobot.debug: print("enter_right")
        self.drive(MazeRobot.right_front)
        self.turn_right()
        self.drive(MazeRobot.right_right)
    
    def _follow_hall(self, distance):
        """Kjører langs en vegg, mens den sjekker til høyre.
        Om den ser en åpning, tar den inn til høyre.
        Løkka brytes og returnerer true om roboten passerer mållinja.
        Ellers false.
        """
        if MazeRobot.debug: print("follow_hall ", distance)
        for i in range((distance-MazeRobot.wall_sensitivity+25)//MazeRobot.inch):
            if self._sees_finish_line():
                return True
            if self._check_right():
                self._nudge()
            else:
                self._enter_right()
                return False
        return False
    
    def follow_right(self):
        """Roboten finner vegen gjennom en labyrint ved å følge høyre vegg.
        Avslutter når den ser mållinja."""
        if MazeRobot.debug: print("follow_right")
        while True:
            distance = self._distance_front()
            if distance < MazeRobot.wall_sensitivity:
                self.turn_left()
            elif self._follow_hall(distance):
                return

    def _execute(self, command):
        """Tolker og utfører en kommando (enten en Relative eller en int)"""
        if MazeRobot.debug: print("execute ", command)
        if command == Relative.LEFT:
            self.turn_left()
        elif command == Relative.RIGHT:
            self.turn_right()
        elif command == Relative.BACK:
            self.turn_back()
        elif command == Relative.FORWARD:
            pass
        else:
            self.drive(ceil(command*MazeRobot.length_adjust))
    
    def backtrack(self):
        """Bruker tracker til å kjøre tilbake samme vegen som den har kjørt,
        og hopper over eventuelle blindveger."""
        if MazeRobot.debug: print("backtrack")
        while self.tracker.tracklength() > 0:
            command = self.tracker.backtrack()
            self._execute(command)
        self.turn_back()
    
    def solve_maze(self):
        """Roboten løser en labyrint. Først vil den finne vegen til målstreken, deretter vil den prøve å finne raskeste veg tilbake."""
        self.follow_right()
        self.celebrate()
        self.print(self.tracker)
        self.backtrack()
        