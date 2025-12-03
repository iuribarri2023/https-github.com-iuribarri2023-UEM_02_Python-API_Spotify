from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..services.spotify_service import SpotifyService
from ..schemas.spotify_schemas import (
    SearchQuerySchema,
    SearchResultSchema,
    AlbumSchema,
    ArtistSchema,
    FullTrackSchema,
)

blp = Blueprint(
    "spotify",
    "spotify",
    url_prefix="/v1",
    description="Endpoints tipo Spotify",
)


def _map_tracks(tracks):
    filtered = []
    for t in tracks:
        artist_names = " ".join(a.get("name", "") for a in t.get("artists", []))
        track_name = t.get("name", "")
        album_name = t.get("album", {}).get("name", "")
        filtered.append(
            {
                "id": t.get("id"),
                "name": track_name,
                "artists": [a.get("name", "") for a in t.get("artists", [])],
                "album": album_name,
                "preview_url": t.get("preview_url"),
                "external_url": t.get("external_urls", {}).get("spotify"),
            }
        )
    return filtered


def _map_albums(albums):
    filtered = []
    for a in albums:
        artist_names = " ".join(ar.get("name", "") for ar in a.get("artists", []))
        album_name = a.get("name", "")
        filtered.append(
            {
                "id": a.get("id"),
                "name": album_name,
                "artists": [ar.get("name", "") for ar in a.get("artists", [])],
                "release_date": a.get("release_date"),
                "total_tracks": a.get("total_tracks"),
                "external_url": a.get("external_urls", {}).get("spotify"),
            }
        )
    return filtered


def _map_artists(artists):
    filtered = []
    for a in artists:
        name = a.get("name", "")
        genres = " ".join(a.get("genres", []))
        filtered.append(
            {
                "id": a.get("id"),
                "name": name,
                "genres": a.get("genres", []),
                "followers": a.get("followers", {}).get("total"),
                "external_url": a.get("external_urls", {}).get("spotify"),
            }
        )
    return filtered


@blp.route("/search")
class SearchResource(MethodView):
    """
    Replica: GET https://api.spotify.com/v1/search
    Soporta track, album y artist; respeta el esquema de Spotify.
    """

    @blp.arguments(SearchQuerySchema, location="query")
    @blp.response(200, SearchResultSchema)
    def get(self, args):
        q = args["q"]
        type_ = args.get("type", "track")
        limit = args.get("limit", 10)
        market = args.get("market", "ES")

        if type_ not in {"track", "album", "artist"}:
            abort(400, message="Solo se soportan type=track, album o artist en esta API.")

        try:
            service = SpotifyService()
            data = service.search(q=q, type_=type_, limit=limit, market=market)

            if type_ == "track":
                items = _map_tracks(data.get("tracks", {}).get("items", []))
            elif type_ == "album":
                items = _map_albums(data.get("albums", {}).get("items", []))
            else:
                items = _map_artists(data.get("artists", {}).get("items", []))

            return {"type": type_, "count": len(items), "items": items}
        except Exception as e:
            abort(500, message=str(e))


@blp.route("/tracks/<string:track_id>")
class TrackResource(MethodView):
    """
    Replica: GET https://api.spotify.com/v1/tracks/{id}
    """

    @blp.response(200, FullTrackSchema)
    def get(self, track_id):
        try:
            service = SpotifyService()
            t = service.get_track(track_id)

            result = {
                "id": t.get("id"),
                "name": t.get("name"),
                "artists": [a.get("name", "") for a in t.get("artists", [])],
                "album": t.get("album", {}).get("name", ""),
                "duration_ms": t.get("duration_ms"),
                "preview_url": t.get("preview_url"),
                "external_url": t.get("external_urls", {}).get("spotify"),
            }

            return result
        except Exception as e:
            abort(500, message=str(e))


@blp.route("/albums/<string:album_id>")
class AlbumResource(MethodView):
    """
    Replica: GET https://api.spotify.com/v1/albums/{id}
    """

    @blp.response(200, AlbumSchema)
    def get(self, album_id):
        try:
            service = SpotifyService()
            a = service.get_album(album_id)
            return {
                "id": a.get("id"),
                "name": a.get("name"),
                "artists": [ar.get("name", "") for ar in a.get("artists", [])],
                "release_date": a.get("release_date"),
                "total_tracks": a.get("total_tracks"),
                "external_url": a.get("external_urls", {}).get("spotify"),
            }
        except Exception as e:
            abort(500, message=str(e))


@blp.route("/artists/<string:artist_id>")
class ArtistResource(MethodView):
    """
    Replica: GET https://api.spotify.com/v1/artists/{id}
    """

    @blp.response(200, ArtistSchema)
    def get(self, artist_id):
        try:
            service = SpotifyService()
            a = service.get_artist(artist_id)
            return {
                "id": a.get("id"),
                "name": a.get("name"),
                "genres": a.get("genres", []),
                "followers": a.get("followers", {}).get("total"),
                "external_url": a.get("external_urls", {}).get("spotify"),
            }
        except Exception as e:
            abort(500, message=str(e))
