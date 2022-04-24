from dataclasses import dataclass

@dataclass
class MIDINote:
    x: float
    y: float
    z: float = 0.0