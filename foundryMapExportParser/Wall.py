from enum import Enum


class MovementRestriction(Enum):
    Normal = "Normal"
    No = "None"


class LightRestriction(Enum):
    ReverseProximity = "ReverseProximity"
    Proximity = "Proximity"
    Normal = "Normal"
    Limited = "Limited"
    No = "None"


class SightRestriction(Enum):
    ReverseProximity = "ReverseProximity"
    Proximity = "Proximity"
    Normal = "Normal"
    Limited = "Limited"
    No = "None"


class SoundRestiction(Enum):
    ReverseProximity = "ReverseProximity"
    Proximity = "Proximity"
    Normal = "Normal"
    Limited = "Limited"
    No = "None"


class Direction(Enum):
    Both = "Both"
    Left = "Left"
    Right = "Right"


class Door(Enum):
    SecretDoorClosed = "SecretDoorClosed"
    SecretDoorOpened = "SecretDoorOpened"
    SecretDoorLocked = "SecretDoorLocked"
    Closed = "Closed"
    Opened = "Opened"
    Locked = "Locked"
    No = "No"


class Wall:
    def __init__(self):
        self.position_from: tuple[int, int] = None
        self.position_to: tuple[int, int] = None
        self.movement_restrictions: MovementRestriction = None
        self.light_restriction: LightRestriction = None
        self.sight_restriction: SightRestriction = None
        self.sound_restriciton: SoundRestiction = None
        self.direction: Direction = None
        self.door: Door = None
