from typing import Dict, Type
import logging
from .scrapers.base import VenueScraper
from .scrapers.bandisintown import BandsInTownScraper

logger = logging.getLogger(__name__)

class ScraperFactory:
    """Factory for creating venue scrapers."""
    
    _scrapers: Dict[str, Type[VenueScraper]] = {}
    
    @classmethod
    def register(cls, name: str, scraper_class: Type[VenueScraper]) -> None:
        """Register a scraper class."""
        cls._scrapers[name] = scraper_class
        logger.info(f"Registered scraper: {name}")
    
    @classmethod
    def get_scraper_for_venue(cls, venue_info: dict) -> VenueScraper:
        """Get appropriate scraper for venue based on configuration."""
        scrapers = venue_info.get('scrapers', {})
        if not scrapers:
            raise ValueError("No scrapers configured for venue")
        
        # Get highest priority scraper
        available_scrapers = sorted(
            scrapers.items(),
            key=lambda x: x[1].get('priority', 999)
        )
        
        if not available_scrapers:
            raise ValueError("No valid scrapers found")
        
        scraper_type = available_scrapers[0][0]
        return cls.get_scraper(scraper_type)
    
    @classmethod
    def get_scraper(cls, scraper_type: str) -> VenueScraper:
        """Get a scraper instance by type."""
        if scraper_type not in cls._scrapers:
            raise ValueError(f"Unknown scraper type: {scraper_type}")
        return cls._scrapers[scraper_type]()

# Register available scrapers
ScraperFactory.register("bandisintown", BandsInTownScraper) 