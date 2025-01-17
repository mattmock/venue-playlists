# Future Concepts

Ideas that need more exploration and brainstorming before moving to concrete features.

## Spotify Integration Concepts

### Playlist Organization
- Challenge: Spotify API doesn't support folder management
- Potential Solutions:
  - Implement consistent naming convention (e.g., "[City] - [Venue] - [Month Year]")
  - Use playlist descriptions for enhanced metadata
  - Focus on website as primary browsing interface
- Questions to Explore:
  - Impact on user experience for direct Spotify profile browsers
  - Trade-offs between different naming conventions
  - Ways to maintain organization as project scales to more cities

### Web UI Automation
- Challenge: Automate folder creation/management through Spotify's web interface
- Technical Approach:
  - Use Selenium/Playwright to interact with Spotify Web Player
  - Simulate manual folder creation and playlist organization
- Major Considerations:
  - High maintenance burden due to UI changes
  - Session handling and authentication complexity
  - Potential rate limiting or detection by Spotify
  - Need for robust error handling and recovery
- Might be worth exploring as proof of concept, but likely too fragile for production use

## User Experience Concepts

### Integrated Music Discovery & Event Tracking
- Challenge: Users discover songs they like while browsing playlists in Spotify, but connecting back to the live event is cumbersome
- Use Case Focus:
  - Quick sampling of venue's upcoming artists
  - Easy way to preview and track interesting shows
  - NOT meant for extended listening sessions
- Potential Solutions:
  - Integrate Spotify Web Playback SDK for quick previews:
    - 30-second song samples with artist/event context
    - Two-button action system:
      - "Open Event" button with dropdown/popup for:
        - BandsInTown link
        - Songkick link
        - Spotify artist page
        - Venue's ticket page
      - "Track Event" button for internal tracking
    - Quick skip/next to sample different artists
    - Emphasis on event details over playback controls
  - Build a lightweight "interested in" tracking system
  - Focus on bridging discovery to existing services
- User Authentication Benefits:
  - Save interesting shows while sampling
  - Quick-add to personal event tracking list
  - Basic preferences for music recommendations
- Questions to Explore:
  - How to optimize the UI for quick sampling vs extended listening
  - Ways to make event tracking/saving as frictionless as possible
  - Premium subscription requirement impact (Web Playback SDK requires Spotify Premium)
  - Browser compatibility and mobile support considerations
  - User data privacy considerations and GDPR compliance
  - Strategy for users without Premium (fallback features)
  - Balance between feature utility and app simplicity
  - Best practices for external service deep linking

## AI Integration Concepts

### AI-Assisted Scraping Enhancement
- Challenge: Making scraping more robust and reducing manual configuration
- Potential Applications:
  - Automated venue calendar discovery:
    - Use AI to analyze venue websites
    - Identify calendar/events pages
    - Extract relevant URLs and patterns
  - Robust artist name extraction:
    - Use AI to parse complex event titles
    - Handle various formatting styles
    - Extract support acts and headliners
    - Understand context (e.g., "with special guests")
  - Venue discovery and validation:
    - Help identify new venues in target cities
    - Validate venue data and categorization
- Major Considerations:
  - API cost management:
    - Implement efficient prompt strategies
    - Cache AI responses where possible
    - Use AI as fallback for simpler methods
  - Reliability and verification:
    - Need human verification for critical changes
    - Balance automation with accuracy
    - Implement confidence scoring
  - Maintenance overhead:
    - Keep prompts updated and effective
    - Handle API changes and costs
    - Monitor and tune performance
- Might be worth exploring for specific high-value use cases first 