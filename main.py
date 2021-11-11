#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase

class MazeRobot:
    """
    Objekter av klassen har metoder som lar en robot bevege seg, og finne vegen gjennom en labyrint
    """
    wheel_diam = 55.5  # Diameter på hjula. Klassevariabel
    axle_track = 124  # Avstand mellom hjula. Klassevariabel

    
    def __init__(self, left_port, right_port, head_port, us_port):
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
        self.head = Motor(head_port)
        self.sensor = UltrasonicSensor(us_port)
        self.base = DriveBase(self.left_motor, self.right_motor, wheel_diameter = MazeRobot.wheel_diam, axle_track = MazeRobot.axle_track)
    
    """
    ================================================
    -- Grunnleggende metoder for robotbevegelse
    ================================================
    """

    def drive(self, distance):
        """Kjører 200 mm (20cm) rett fram."""

        self.base.straight(distance)
    
    def turn_right(self):
        """Roboten roterer 90 grader mot høyre"""
        
        self.base.turn(90)
    
    
    def turn_left(self):
        """Roboten roterer 90 grader mot venstre"""

        self.base.turn(-90)
    
    def forward(self):
        """
        Kjører 20 cm fram
        """
        self.drive(200)
    
    """
    ================================================
    -- Metoder for styring av UL-sensor
    ================================================
    """

    def turn_head(self, deg):
        """
        Snur huet til en vinkel deg fra normal.
        (Positiv retning mot høyre)
        """
        # Snur huet med mål deg grader fra normal
        # Hastighet 180 grader i sekundet
        self.head.run_target(180, deg)
    
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
    
    
    def sees_wall(self, distance):
        """
        Returnerer True om sensoren kan se noe som er nærmere enn distance mm.
        """
        return (self.sensor.distance() <= distance)
    
    
    def check_right(self):
        """
        Snur huet til høyre, kikker etter vegger, og snur tilbake
        Returnerer True om den har sett en vegg.
        """
        self.turn_head_right() # Snur huet mot høyre
        r = self.sees_wall(300) # Er det en vegg der? Lagrer i r
        self.turn_head_straight() # Snur huet fram igjen
        return r
    
    
    def check_front(self):
        """Returnerer True om den ser en vegg nærmere enn 20 cm foran"""
        self.turn_head_straight()
        return self.sees_wall(200)
    
    """
    ================================================
    -- Metoder for navigering
    ================================================
    """

    def enter_right(self):
        """Kjører inn i en åpning til høyre"""
        self.drive(150)
        self.turn_right()
        self.drive(150)

    def direction(self):
        if not self.check_right():
            self.enter_right()
        elif self.check_front():
            self.turn_left()
        else:
            self.drive(20)
    
    def follow_right(self):
        for i in range(100):
            self.direction()
        
        


robot = MazeRobot(Port.A, Port.D, Port.C, Port.S3)

robot.follow_right()