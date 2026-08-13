"""Local account profile — remember last username, login state."""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_FILE = os.path.join(BASE, 'account_profile.json')


def load_profile():
    try:
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}


def save_profile(profile):
    try:
        with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False)
    except:
        pass


def get_last_username():
    u = load_profile().get('last_username', '')
    return u or ''


def set_last_username(username):
    p = load_profile()
    p['last_username'] = username
    save_profile(p)


def clear_profile():
    save_profile({})
