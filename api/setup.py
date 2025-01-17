from setuptools import setup, find_packages

setup(
    name="venue-playlists-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "pyyaml"
    ],
) 