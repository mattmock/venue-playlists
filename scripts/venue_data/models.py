from dataclasses import dataclass
from datetime import datetime

@dataclass
class ArtistEvent:
    """Represents an artist's performance event.
    
    Attributes:
        name: The artist's name
        date: The performance date as a datetime object
    """
    name: str
    date: datetime