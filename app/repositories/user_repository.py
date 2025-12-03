import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from flask import current_app

DATA_FILE_DEFAULT = Path(__file__).resolve().parents[2] / "data" / "users.json"

# Datos de ejemplo por si el archivo no existe o es ilegible
DEFAULT_USERS = [
    {
        "id": "11111111-1111-1111-1111-111111111111",
        "name": "Ane Ibarrola",
        "email": "ane@example.com",
        "favorite_tracks": [
            "1mea3bSkSGXuIRvnydlB5b",
            "4sPmO7WMQUAf45kwMOtONw",
        ],
        "favorite_artists": [
            "4gzpq5DPGxSnKTe4SA8HAU",
            "4dpARuHxo51G3z768sgnrY",
        ],
    },
    {
        "id": "22222222-2222-2222-2222-222222222222",
        "name": "Jon Arrieta",
        "email": "jon@example.com",
        "favorite_tracks": [
            "0VjIjW4GlUZAMYd2vXMi3b",
            "4P7VFiaZb3xrXoqGwZXC3J",
        ],
        "favorite_artists": [
            "1Xyo4u8uXC1ZmMpatF05PJ",
            "5INjqkS1o8h1imAzPqGZBb",
        ],
    },
]


def _data_file() -> Path:
    """Devuelve la ruta del JSON de usuarios según config o el valor por defecto."""
    try:
        cfg_path = current_app.config.get("USERS_DATA_PATH")
        if cfg_path:
            return Path(cfg_path)
    except Exception:
        # Si no hay app context o config, usar la ruta base
        pass
    return DATA_FILE_DEFAULT


def _load_users() -> List[Dict]:
    """Lee el archivo JSON de usuarios y devuelve datos o semilla si falta/errores."""
    data_file = _data_file()
    if not data_file.exists():
        _save_users(DEFAULT_USERS)
        return list(DEFAULT_USERS)

    try:
        with data_file.open("r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                _save_users(DEFAULT_USERS)
                return list(DEFAULT_USERS)
            return json.loads(content)
    except json.JSONDecodeError:
        _save_users(DEFAULT_USERS)
        return list(DEFAULT_USERS)


def _save_users(users: List[Dict]) -> None:
    data_file = _data_file()
    data_file.parent.mkdir(parents=True, exist_ok=True)
    with data_file.open("w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def get_all_users() -> List[Dict]:
    return _load_users()


def get_user_by_id(user_id: str) -> Optional[Dict]:
    return next((u for u in _load_users() if u["id"] == user_id), None)


def create_user(data: Dict) -> Dict:
    users = _load_users()
    user = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "email": data["email"],
        "favorite_tracks": data.get("favorite_tracks", []),
        "favorite_artists": data.get("favorite_artists", []),
    }
    users.append(user)
    _save_users(users)
    return user


def update_user(user_id: str, updates: Dict) -> Optional[Dict]:
    users = _load_users()
    for u in users:
        if u["id"] == user_id:
            for key in ("name", "email", "favorite_tracks", "favorite_artists"):
                if key in updates:
                    u[key] = updates[key]
            _save_users(users)
            return u
    return None


def delete_user(user_id: str) -> bool:
    users = _load_users()
    filtered = [u for u in users if u["id"] != user_id]
    if len(filtered) == len(users):
        return False
    _save_users(filtered)
    return True
