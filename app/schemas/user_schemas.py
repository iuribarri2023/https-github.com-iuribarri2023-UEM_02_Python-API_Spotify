from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    favorite_tracks = fields.List(
        fields.String(),
        load_default=list,
        description="Lista de IDs de canciones de Spotify"
    )
    favorite_artists = fields.List(
        fields.String(),
        load_default=list,
        description="Lista de IDs de artistas de Spotify"
    )


class UserCreateSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    favorite_tracks = fields.List(fields.String(), load_default=list)
    favorite_artists = fields.List(fields.String(), load_default=list)


class UserUpdateSchema(Schema):
    name = fields.String()
    email = fields.Email()
    favorite_tracks = fields.List(fields.String())
    favorite_artists = fields.List(fields.String())
