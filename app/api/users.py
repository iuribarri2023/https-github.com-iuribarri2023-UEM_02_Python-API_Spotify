from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schemas.user_schemas import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from ..schemas.spotify_schemas import FavoritesDetailSchema
from ..services.spotify_service import SpotifyService
from ..repositories import user_repository as repo

blp = Blueprint(
    "users",
    "users",
    url_prefix="/v1/users",   # siguiendo el estilo de /v1/users/{id}
    description="Gestión de usuarios (almacenados en JSON)"
)


@blp.route("")
class UserListResource(MethodView):

    @blp.response(200, UserSchema(many=True))
    def get(self):
        """
        Listar todos los usuarios.
        """
        users = repo.get_all_users()
        return users

    @blp.arguments(UserCreateSchema)
    @blp.response(201, UserSchema)
    def post(self, new_data):
        """
        Crear un usuario nuevo.
        """
        user = repo.create_user(new_data)
        return user


@blp.route("/<string:user_id>")
class UserResource(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        """
        Obtener un usuario por ID.
        """
        user = repo.get_user_by_id(user_id)
        if not user:
            abort(404, message="Usuario no encontrado")
        return user

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def patch(self, updates, user_id):
        """
        Actualizar un usuario (parcial).
        """
        user = repo.update_user(user_id, updates)
        if not user:
            abort(404, message="Usuario no encontrado")
        return user

    @blp.response(204)
    def delete(self, user_id):
        """
        Eliminar un usuario.
        """
        ok = repo.delete_user(user_id)
        if not ok:
            abort(404, message="Usuario no encontrado")
        # 204 -> sin contenido
        return ""


@blp.route("/<string:user_id>/favorites/details")
class UserFavoritesDetailResource(MethodView):
    """
    Devuelve info detallada de canciones y artistas favoritos del usuario.
    """

    @blp.response(200, FavoritesDetailSchema)
    def get(self, user_id):
        user = repo.get_user_by_id(user_id)
        if not user:
            abort(404, message="Usuario no encontrado")

        try:
            service = SpotifyService()
            track_details = []
            for track_id in user.get("favorite_tracks", []):
                t = service.get_track(track_id)
                track_details.append({
                    "id": t.get("id"),
                    "name": t.get("name"),
                    "artists": [a.get("name", "") for a in t.get("artists", [])],
                    "album": t.get("album", {}).get("name", ""),
                    "preview_url": t.get("preview_url"),
                    "external_url": t.get("external_urls", {}).get("spotify"),
                })

            artist_details = []
            for artist_id in user.get("favorite_artists", []):
                a = service.get_artist(artist_id)
                artist_details.append({
                    "id": a.get("id"),
                    "name": a.get("name"),
                    "genres": a.get("genres", []),
                    "followers": a.get("followers", {}).get("total"),
                    "external_url": a.get("external_urls", {}).get("spotify"),
                })

            return {"tracks": track_details, "artists": artist_details}
        except Exception as e:
            abort(500, message=str(e))
