from abc import ABC, abstractmethod
from typing import List
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from ..models import ArtistEvent

logger = logging.getLogger(__name__)

class VenueScraper(ABC):
    """Base class for venue scrapers."""
    
    def __init__(self):
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retries."""
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session
    
    @property
    @abstractmethod
    def scraper_type(self) -> str:
        """Return the type identifier for this scraper."""
        pass
    
    @abstractmethod
    def get_events(self, venue_key: str, venue_info: dict) -> List[ArtistEvent]:
        """Get all events for a venue."""
        pass