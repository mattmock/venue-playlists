"""Flask application runner."""
from venue_playlists_api import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 