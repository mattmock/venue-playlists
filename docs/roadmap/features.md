# Feature Roadmap

## Core Features

### Multi-City Support
- [ ] Support for additional cities beyond SF
- [ ] Automated City Expansion:
   - Venue Discovery:
     - Semi-automated venue discovery:
       - Generate initial venue list from Google Places/Reviews
       - Simple admin UI to review/edit venues
       - Quick "approve/reject" interface
       - Bulk venue approval for obvious matches
   - Venue Data Collection:
     - Assisted URL matching:
       - Suggest BandsInTown/Songkick URLs
       - Show side-by-side venue comparison
       - "One-click" config generation after approval
   - Quality Control:
     - Confidence scoring for venue matches
     - Manual review interface for low confidence matches
     - Automated venue data validation

### Music Discovery
- [ ] Add venue filtering by music genre
- [ ] Implement playlist history tracking
- [ ] Smart Artist Discovery:
   - Highlight lesser-known artists similar to user's favorites
   - Show "If you like X, check out Y playing at Z venue"
   - Focus on artists with <100k monthly listeners
   - Compare artist genres with user's top genres
   - Add "Hidden Gems" section for each venue
   - Show Spotify popularity score comparison
   - User Authentication Features:
     - Analyze user's Spotify listening history for better recommendations
     - Create personalized venue recommendations based on music taste
     - Alert users when similar artists announce shows
     - Track which recommendations led to event attendance 