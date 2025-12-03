from marshmallow import Schema, fields


class SearchQuerySchema(Schema):
    q = fields.String(required=True, description="Texto de busqueda (como en Spotify)")
    type = fields.String(
        load_default="track",
        description="Tipo de busqueda: track, album o artist"
    )
    limit = fields.Integer(
        load_default=10,
        description="Numero maximo de resultados"
    )
    market = fields.String(
        load_default="ES",
        description="Codigo de pais (ej. ES)"
    )


class TrackSchema(Schema):
    id = fields.String()
    name = fields.String()
    artists = fields.List(fields.String())
    album = fields.String()
    preview_url = fields.String(allow_none=True)
    external_url = fields.String(allow_none=True)


class AlbumSchema(Schema):
    id = fields.String()
    name = fields.String()
    artists = fields.List(fields.String())
    release_date = fields.String()
    total_tracks = fields.Integer()
    external_url = fields.String(allow_none=True)


class ArtistSchema(Schema):
    id = fields.String()
    name = fields.String()
    genres = fields.List(fields.String())
    followers = fields.Integer()
    external_url = fields.String(allow_none=True)


class SearchResultSchema(Schema):
    type = fields.String()
    count = fields.Integer()
    items = fields.List(fields.Raw())


class FavoritesDetailSchema(Schema):
    tracks = fields.List(fields.Nested(TrackSchema))
    artists = fields.List(fields.Nested(ArtistSchema))


class FullTrackSchema(Schema):
    """
    Esquema simplificado para /v1/tracks/{id}.
    Si quieres, puedes hacer un esquema mas fiel a Spotify.
    """
    id = fields.String()
    name = fields.String()
    artists = fields.List(fields.String())
    album = fields.String()
    duration_ms = fields.Integer()
    preview_url = fields.String(allow_none=True)
    external_url = fields.String(allow_none=True)
