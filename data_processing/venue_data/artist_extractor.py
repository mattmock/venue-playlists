import logging
from typing import List
import openai
from .models import ArtistEvent
from .constants import MESSAGE_PREFIX
from datetime import datetime

logger = logging.getLogger(__name__)

class ArtistExtractor:
    """Extract artist events from text using OpenAI."""
    
    def process_chunks(self, text_chunks: List[str]) -> List[ArtistEvent]:
        """Process text chunks and extract artist events."""
        events = []
        for chunk in text_chunks:
            try:
                # Format message for OpenAI
                message = MESSAGE_PREFIX + chunk
                
                # Get response from OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": message}],
                    temperature=0
                )
                
                # Parse response
                text = response.choices[0].message.content
                events.extend(self._parse_events(text))
                
            except Exception as e:
                logger.error(f"Error processing chunk: {e}")
                continue
        
        return events
    
    def _parse_events(self, text: str) -> List[ArtistEvent]:
        """Parse events from OpenAI response."""
        events = []
        for line in text.split('\n'):
            if not line.strip() or '|' not in line:
                continue
                
            try:
                # Split line into artist and date
                artist, date_str = [x.strip() for x in line.split('|')]
                
                # Parse date (format: "MMM DD")
                date = datetime.strptime(date_str, "%b %d")
                
                # Add current year
                current_year = datetime.now().year
                date = date.replace(year=current_year)
                
                events.append(ArtistEvent(
                    name=artist,
                    date=date,
                    venue=""  # Will be set by venue processor
                ))
                
            except Exception as e:
                logger.warning(f"Error parsing line '{line}': {e}")
                continue
        
        return events