"""Cloud save using GitHub API — non-blocking, background sync."""
import json, base64, time, threading, os

try:
    import requests
except ImportError:
    requests = None

from services.cloud_config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME
from services.device_id import get_device_id

API_BASE = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

_ERROR_MESSAGES = {
    400: "请求格式错误",
    401: "Token 无效",
    403: "无权限访问存档仓库",
    404: "存档仓库不存在",
    422: "数据校验失败",
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

    def _ensure_repo(self):
        try:
            resp = requests.post(
                "https://api.github.com/user/repos",
                headers=HEADERS,
                json={"name": REPO_NAME, "private": False, "auto_init": True},
                timeout=10)
            return resp.status_code in [201, 422]
        except:
            return False

    def _put_file(self, username, data):
        url = f"{API_BASE}/contents/players/{username}.json"
        sha = self._github_sha(url)
        content = base64.b64encode(json.dumps(data, ensure_ascii=False).encode()).decode()
        payload = {"message": f"{username} sync {time.strftime('%H:%M:%S')}",
                   "content": content}
        if sha:
            payload["sha"] = sha
        return requests.put(url, headers=HEADERS, json=payload, timeout=10)

    def register(self, username, callback=None):
        """Register device to username. Callback(result) called on UI thread."""
        def _do():
            if not requests:
                return self._cb(callback, (False, "网络库不可用"))
            data = {"uuid": self._device_id, "username": username, "registered_at": time.time()}
            try:
                resp = self._put_file(username, data)
            except:
                return self._cb(callback, (False, "网络连接失败，请检查网络"))
            if resp.status_code in [200, 201]:
                self._username = username
                self._save_local_username()
                self._cb(callback, (True, "注册成功"))
                return
            if resp.status_code == 404:
                if self._ensure_repo():
                    try:
                        resp = self._put_file(username, data)
                    except:
                        return self._cb(callback, (False, "网络连接失败"))
                    if resp.status_code in [200, 201]:
                        self._username = username
                        self._save_local_username()
                        self._cb(callback, (True, "注册成功"))
                        return
                self._cb(callback, (False, "存档仓库创建失败"))
                return
            msg = _ERROR_MESSAGES.get(resp.status_code, f"注册失败({resp.status_code})")
            self._cb(callback, (False, msg))
        threading.Thread(target=_do, daemon=True).start()

    def login(self, username, callback=None):
        """Login as username. Downloads existing save if available."""
        def _do():
            if not requests:
                return self._cb(callback, (False, "网络库不可用"))
            url = f"{API_BASE}/contents/players/{username}.json"
            try:
                resp = requests.get(url, headers=HEADERS, timeout=10)
            except:
                return self._cb(callback, (False, "网络连接失败"))
            if resp.status_code != 200:
                msg = _ERROR_MESSAGES.get(resp.status_code, f"登录失败({resp.status_code})")
                if resp.status_code == 404:
                    msg = "账号不存在"
                return self._cb(callback, (False, msg))
            try:
                data = json.loads(base64.b64decode(resp.json()["content"]).decode())
            except:
                return self._cb(callback, (False, "数据解析失败"))
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
            data = {"uuid": self._device_id, "username": self._username,
                    "save": save_data, "last_sync": time.time()}
            try:
                resp = self._put_file(self._username, data)
            except:
                self._syncing = False
                return self._cb(callback, (False, "网络连接失败"))
            if resp.status_code in [200, 201]:
                self._dirty = False
                self._last_sync = time.time()
                self._cb(callback, (True, "同步成功"))
            else:
                self._cb(callback, (False, _ERROR_MESSAGES.get(resp.status_code, f"同步失败({resp.status_code})")))
            self._syncing = False
        threading.Thread(target=_do, daemon=True).start()

    def download(self, callback=None):
        """Download save from cloud."""
        if not self._username or not requests:
            return self._cb(callback, (False, None))
        def _do():
            url = f"{API_BASE}/contents/players/{self._username}.json"
            try:
                resp = requests.get(url, headers=HEADERS, timeout=10)
            except:
                return self._cb(callback, (False, None))
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
