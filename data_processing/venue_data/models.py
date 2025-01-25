from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ArtistEvent:
    """Represents an artist event at a venue."""
    name: str
    date: datetime
    venue: str
    scraper_type: Optional[str] = None  # Added to track which scraper found this event
    
    def __post_init__(self):
        """Validate and clean data after initialization."""
        # Ensure name is a string and stripped
        self.name = str(self.name).strip()
        
        # Ensure date is a datetime
        if isinstance(self.date, str):
            try:
                self.date = datetime.fromisoformat(self.date)
            except ValueError as e:
                raise ValueError(f"Invalid date format for {self.name}: {e}")
                
        # Ensure venue is a string
        self.venue = str(self.venue).strip()