import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "users.json"


def _load_users() -> List[Dict]:
    """Lee el archivo JSON de usuarios y devuelve lista vacía si falta o es inválido."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except json.JSONDecodeError:
        return []


def _save_users(users: List[Dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
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
