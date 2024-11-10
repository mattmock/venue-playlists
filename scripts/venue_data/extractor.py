from openai import OpenAI
import os
from functools import lru_cache
from typing import List
from . import constants
from .models import ArtistEvent
from datetime import datetime

class ArtistExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    @lru_cache(maxsize=32)
    def extract_artists_from_text(self, text: str) -> List[ArtistEvent]:
        """Extract artist names and dates from text using OpenAI."""
        try:
            print(f"Sending chunk of length {len(text)} to OpenAI")
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": constants.MESSAGE_PREFIX + text}],
                model="gpt-3.5-turbo",
            )
            print(f"OpenAI response: {completion.choices[0].message.content[:200]}")
            
            artist_events = []
            current_year = datetime.now().year
            for line in completion.choices[0].message.content.split("\n"):
                if "|" in line:
                    artist, date_str = line.split("|")
                    try:
                        # Handle "MMM DD" format
                        date_str = date_str.strip()
                        if len(date_str) == 6:  # "NOV 09" format
                            date = datetime.strptime(f"{current_year} {date_str}", "%Y %b %d")
                            # If date is in the past, assume next year
                            if date < datetime.now():
                                date = date.replace(year=current_year + 1)
                        else:
                            # Try original YYYY-MM-DD format
                            date = datetime.strptime(date_str, "%Y-%m-%d")
                        
                        artist_events.append(ArtistEvent(
                            name=artist.strip(),
                            date=date
                        ))
                    except ValueError as e:
                        print(f"Error parsing date '{date_str}': {e}")
                        continue
            return artist_events
        except Exception as e:
            print(f"Error extracting artists: {e}")
            return []

    def process_chunks(self, chunks: List[str]) -> List[ArtistEvent]:
        """Process multiple text chunks and return unique artists with dates."""
        all_artists = []
        for chunk in chunks:
            all_artists.extend(self.extract_artists_from_text(chunk))
        
        # Remove duplicates while preserving order
        seen = set()
        return [a for a in all_artists if not (a.name in seen or seen.add(a.name))]