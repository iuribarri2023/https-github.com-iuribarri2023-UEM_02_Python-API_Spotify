import os

class Configuration:
    DEBUG= False
    
    # Flask Smorest Configuration
    API_TITLE = "API Música en Euskera"
    API_VERSION = "v0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    #Spotify variables
    SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID","743c7a9e6a844954a03589528ac3d6b3")
    SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET","bf01f5a01fda4d608d52007362fcce5f")

    
