# API Spotify (Flask + Flask-Smorest)

## Descripción
API REST que gestiona usuarios y sus preferencias musicales sin base de datos (JSON en disco) e integra Spotify para buscar y obtener información de canciones, álbumes y artistas.

## Estructura
- `main.py`: punto de entrada; crea y arranca la app.
- `app/__init__.py`: factoría Flask, configura Flask-Smorest, registra blueprints y expone rutas `/` y `/health`.
- `app/config.py`: configuración de Flask-Smorest y credenciales de Spotify (variables de entorno `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`).
- `app/extensions.py`: instancia `Api` de Flask-Smorest.
- `app/api/spotify_api.py`: endpoints `/v1/search`, `/v1/tracks/<id>`, `/v1/albums/<id>`, `/v1/artists/<id>`.
- `app/api/users.py`: CRUD de usuarios en `/v1/users` y detalle de favoritos `/v1/users/<id>/favorites/details`.
- `app/services/spotify_service.py`: cliente hacia Spotify (client credentials), métodos `search`, `get_track`, `get_album`, `get_artist`.
- `app/repositories/user_repository.py`: lectura/escritura de `data/users.json` (sin BD).
- `app/schemas/*`: esquemas Marshmallow para validación y respuestas.
- `data/users.json`: datos de ejemplo de usuarios con favoritos.

## Endpoints principales
- `GET /docs`: UI Swagger (OpenAPI en `/openapi.json`).
- `GET /health`: comprobación de estado.
- `GET /v1/search?q=<texto>&type=track|album|artist&limit=&market=`: búsqueda en Spotify.
- `GET /v1/tracks/<id>` / `GET /v1/albums/<id>` / `GET /v1/artists/<id>`: detalle directo desde Spotify.
- `GET /v1/users`: lista de usuarios.
- `POST /v1/users`: crea usuario (`name`, `email`, opcional `favorite_tracks`, `favorite_artists`).
- `GET /v1/users/<id>` / `PATCH /v1/users/<id>` / `DELETE /v1/users/<id>`: operaciones CRUD.
- `GET /v1/users/<id>/favorites/details`: obtiene metadatos de canciones y artistas favoritos vía Spotify.

## Requisitos
- Python 3.11+ recomendado.
- Instalar dependencias: `pip install -r requirements.txt`.
- Variables de entorno: `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` (se usan valores por defecto de demostración si no se establecen).

## Ejecución
1) `python main.py`
2) Abrir `http://localhost:5000/` para landing, `http://localhost:5000/docs` para probar la API.

## Datos de ejemplo
`data/users.json` incluye dos usuarios con listas de canciones y artistas de Spotify. Estas listas alimentan el endpoint de detalles de favoritos.
