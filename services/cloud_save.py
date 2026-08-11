"""Cloud save using GitHub API — non-blocking, background sync."""
import json, base64, time, threading, os

try:
    import requests
except ImportError:
    requests = None

from services.cloud_config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME
from services.device_id import get_device_id

try:
    from services.cloud_config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME
except (ImportError, ModuleNotFoundError):
    GITHUB_TOKEN = ""
    REPO_OWNER = ""
    REPO_NAME = ""

API_BASE = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


class CloudSave:
    def __init__(self):
        self._device_id = get_device_id()
        self._username = None
        self._last_sync = 0
        self._dirty = False
        self._syncing = False
        self._load_local_username()

    def _load_local_username(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uf = os.path.join(base, 'cloud_user.txt')
        if os.path.exists(uf):
            try:
                with open(uf, 'r') as f:
                    self._username = f.read().strip()
            except:
                pass

    def _save_local_username(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uf = os.path.join(base, 'cloud_user.txt')
        try:
            with open(uf, 'w') as f:
                f.write(self._username or '')
        except:
            pass

    @property
    def username(self):
        return self._username

    def is_logged_in(self):
        return self._username is not None and len(self._username) > 0

    def register(self, username, callback=None):
        """Register device to username. Callback(result) called on UI thread."""
        def _do():
            if not requests:
                return self._cb(callback, (False, "网络库不可用"))
            data = {"uuid": self._device_id, "username": username, "registered_at": time.time()}
            url = f"{API_BASE}/contents/players/{username}.json"
            sha = self._github_sha(url)
            content = base64.b64encode(json.dumps(data, ensure_ascii=False).encode()).decode()
            payload = {"message": f"{username} register", "content": content}
            if sha:
                payload["sha"] = sha
            resp = requests.put(url, headers=HEADERS, json=payload, timeout=10)
            if resp.status_code in [200, 201]:
                self._username = username
                self._save_local_username()
                self._cb(callback, (True, "注册成功"))
            else:
                self._cb(callback, (False, f"注册失败: {resp.status_code}"))
        threading.Thread(target=_do, daemon=True).start()

    def login(self, username, callback=None):
        """Login as username. Downloads existing save if available."""
        def _do():
            if not requests:
                return self._cb(callback, (False, "网络库不可用"))
            url = f"{API_BASE}/contents/players/{username}.json"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                return self._cb(callback, (False, f"账号不存在: {resp.status_code}"))
            try:
                data = json.loads(base64.b64decode(resp.json()["content"]).decode())
            except:
                return self._cb(callback, (False, "数据解析失败"))
            if data.get("uuid") != self._device_id:
                self._username = username
                self._save_local_username()
                self._cb(callback, (True, "登录成功", data))
                return
            self._username = username
            self._save_local_username()
            self._cb(callback, (True, "登录成功", data))
        threading.Thread(target=_do, daemon=True).start()

    def upload(self, save_data, callback=None):
        """Upload save data to cloud. Non-blocking."""
        if not self._username or not requests:
            return
        self._syncing = True
        def _do():
            url = f"{API_BASE}/contents/players/{self._username}.json"
            sha = self._github_sha(url)
            data = {"uuid": self._device_id, "username": self._username,
                    "save": save_data, "last_sync": time.time()}
            content = base64.b64encode(json.dumps(data, ensure_ascii=False).encode()).decode()
            payload = {"message": f"{self._username} sync {time.strftime('%H:%M:%S')}",
                       "content": content}
            if sha:
                payload["sha"] = sha
            resp = requests.put(url, headers=HEADERS, json=payload, timeout=10)
            if resp.status_code in [200, 201]:
                self._dirty = False
                self._last_sync = time.time()
                self._cb(callback, (True, "同步成功"))
            else:
                self._cb(callback, (False, f"同步失败:{resp.status_code}"))
            self._syncing = False
        threading.Thread(target=_do, daemon=True).start()

    def download(self, callback=None):
        """Download save from cloud."""
        if not self._username or not requests:
            return self._cb(callback, (False, None))
        def _do():
            url = f"{API_BASE}/contents/players/{self._username}.json"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                return self._cb(callback, (False, None))
            try:
                data = json.loads(base64.b64decode(resp.json()["content"]).decode())
            except:
                return self._cb(callback, (False, None))
            self._cb(callback, (True, data.get("save")))
        threading.Thread(target=_do, daemon=True).start()

    def mark_dirty(self):
        self._dirty = True

    def should_sync(self):
        return self._dirty and not self._syncing and self.is_logged_in()

    def _github_sha(self, url):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code == 200:
                return resp.json().get("sha")
        except:
            pass
        return None

    def _cb(self, callback, result):
        if callback:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: callback(result), 0)
