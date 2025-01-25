from setuptools import setup, find_packages

setup(
    name="venue-playlists-scripts",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'venue-playlists-api',  # Our API package
        'pyyaml',
        'requests',
        'beautifulsoup4'
    ]
) 