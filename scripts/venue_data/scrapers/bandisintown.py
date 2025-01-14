import os
import logging
from datetime import datetime
from typing import List
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from .base import VenueScraper
from ..models import ArtistEvent
import time
import random
import json

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

class BandsInTownScraper(VenueScraper):
    """Scraper for BandsInTown venue pages."""
    
    def __init__(self):
        super().__init__()
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with proper options."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Add anti-bot detection evasion
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=options)
            # Execute CDP commands to prevent detection
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def __del__(self):
        """Clean up resources."""
        self.cleanup()
    
    def cleanup(self):
        """Clean up browser resources safely."""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                logger.debug("Chrome driver cleaned up successfully")
            except Exception as e:
                logger.error(f"Error cleaning up Chrome driver: {e}")
    
    @property
    def scraper_type(self) -> str:
        return "bandisintown"
    
    def save_screenshot(self, venue_key: str):
        """Save screenshot for debugging."""
        try:
            screenshots_dir = Path("logs/screenshots")
            screenshots_dir.mkdir(exist_ok=True, parents=True)
            
            filename = screenshots_dir / f"{venue_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(str(filename))
            logger.debug(f"Screenshot saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
    
    def get_events(self, venue_key: str, venue_info: dict) -> List[ArtistEvent]:
        """Get events from BandsInTown using JSON-LD data."""
        try:
            url = venue_info['scrapers'][self.scraper_type]['url']
            logger.info(f"Fetching events for {venue_key} from {url}")
            
            # Load the page
            self.driver.get(url)
            
            try:
                # Find all script tags with type="application/ld+json"
                script_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    'script[type="application/ld+json"]'
                )
                
                events = []
                for script in script_elements:
                    try:
                        # Parse JSON content
                        json_content = json.loads(script.get_attribute('innerHTML'))
                        
                        # If it's an array, check each item
                        if isinstance(json_content, list):
                            for item in json_content:
                                if item.get('@type') == 'MusicEvent':
                                    try:
                                        # Extract event info
                                        artist = item['performer']['name']
                                        date_str = item['startDate']
                                        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                                        
                                        events.append(ArtistEvent(
                                            name=artist,
                                            date=date,
                                            venue=venue_info['name']
                                        ))
                                        logger.debug(f"Found event: {artist} on {date}")
                                    except Exception as e:
                                        logger.warning(f"Error parsing event data: {e}")
                                        continue
                    except json.JSONDecodeError as e:
                        logger.warning(f"Error decoding JSON from script tag: {e}")
                        continue
                
                if not events:
                    logger.warning(f"No events found for {venue_key}, saving screenshot")
                    self.save_screenshot(venue_key)
                
                logger.info(f"Found {len(events)} events for {venue_key}")
                return events
                
            except Exception as e:
                logger.error(f"Error finding JSON-LD data: {e}")
                self.save_screenshot(venue_key)
                raise
                
        except WebDriverException as e:
            logger.error(f"WebDriver error for {venue_key}: {e}")
            self.save_screenshot(venue_key)
            raise
        except Exception as e:
            logger.error(f"Error scraping {venue_key}: {e}")
            self.save_screenshot(venue_key)
            raise
        finally:
            if os.environ.get('SAVE_ALL_SCREENSHOTS'):
                self.save_screenshot(venue_key) 