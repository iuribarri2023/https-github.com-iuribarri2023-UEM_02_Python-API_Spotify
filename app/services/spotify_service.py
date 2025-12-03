import base64
import time
import requests

from flask import current_app

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

class SpotifyService:
    def __init__(self):
        self.client_id = current_app.config["SPOTIFY_CLIENT_ID"]
        self.client_secret = current_app.config["SPOTIFY_CLIENT_SECRET"]
        self._access_token = None
        self._token_expires_at = 0
    
    def _get_access_token(self):
        """Obtiene un token de Spotify usando Client Credentials."""
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token

        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode("utf-8")
        ).decode("utf-8")

        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()

        self._access_token = token_data["access_token"]
        self._token_expires_at = time.time() + token_data.get("expires_in", 3600) - 60

        return self._access_token
    
    def _get_headers(self):
        token = self._get_access_token()
        return {"Authorization": f"Bearer {token}"}

    def search(self, q, type_="track", limit=10, market="ES"):
        """
        Replica aproximada de GET /v1/search de Spotify (solo type=track en este ejemplo).
        """
        url = f"{SPOTIFY_API_BASE_URL}/search"
        params = {
            "q": q,
            "type": type_,
            "limit": limit,
            "market": market,
        }
        headers = self._get_headers()
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_track(self, track_id):
        """Replica GET /v1/tracks/{id}."""
        url = f"{SPOTIFY_API_BASE_URL}/tracks/{track_id}"
        headers = self._get_headers()
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def get_album(self, album_id):
        """Replica GET /v1/albums/{id}."""
        url = f"{SPOTIFY_API_BASE_URL}/albums/{album_id}"
        headers = self._get_headers()
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def get_artist(self, artist_id):
        """Replica GET /v1/artists/{id}."""
        url = f"{SPOTIFY_API_BASE_URL}/artists/{artist_id}"
        headers = self._get_headers()
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()
