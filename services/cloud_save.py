"""Cloud save using GitHub API — account system with password + UUID."""
import json, base64, time, threading, os, hashlib, uuid

try:
    import requests
except ImportError:
    requests = None

from services.cloud_config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME

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


def _hash_password(password, account_uuid):
    return hashlib.sha256(f"{password}:{account_uuid}".encode()).hexdigest()


class CloudSave:
    def __init__(self):
        self._username = None
        self._account_uuid = None
        self._nickname = None
        self._last_sync = 0
        self._dirty = False
        self._syncing = False
        self._load_local_profile()

    def _load_local_profile(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uf = os.path.join(base, 'account_profile.json')
        if os.path.exists(uf):
            try:
                with open(uf, 'r', encoding='utf-8') as f:
                    p = json.load(f)
                    self._username = p.get('last_username')
                    self._account_uuid = p.get('account_uuid')
                    self._nickname = p.get('nickname')
            except:
                pass

    def _save_local_profile(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uf = os.path.join(base, 'account_profile.json')
        try:
            with open(uf, 'w', encoding='utf-8') as f:
                json.dump({'last_username': self._username,
                           'account_uuid': self._account_uuid,
                           'nickname': self._nickname}, f, ensure_ascii=False)
        except:
            pass

    @property
    def username(self):
        return self._username

    @property
    def account_uuid(self):
        return self._account_uuid

    @property
    def nickname(self):
        return self._nickname or self._username or ''

    def is_logged_in(self):
        return self._username is not None and len(self._username) > 0

    def logout(self):
        self._username = None
        self._account_uuid = None
        self._nickname = None
        self._save_local_profile()

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

    def _get_file(self, username):
        url = f"{API_BASE}/contents/players/{username}.json"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return None
        try:
            return json.loads(base64.b64decode(resp.json()["content"]).decode())
        except:
            return None

    def register(self, username, password, nickname, callback=None):
        """Register new account. UUID assigned once at registration."""
        def _do():
            if not requests:
                return self._cb(callback, (False, "网络库不可用"))
            if not username or len(username) < 2:
                return self._cb(callback, (False, "用户名至少2个字符"))
            if not password or len(password) < 4:
                return self._cb(callback, (False, "密码至少4个字符"))
            account_uuid = str(uuid.uuid4())
            data = {
                "uuid": account_uuid,
                "username": username,
                "nickname": nickname or username,
                "password_hash": _hash_password(password, account_uuid),
                "registered_at": time.time(),
                "last_sync": time.time(),
            }
            try:
                resp = self._put_file(username, data)
            except:
                return self._cb(callback, (False, "网络连接失败，请检查网络"))
            if resp.status_code in [200, 201]:
                self._username = username
                self._account_uuid = account_uuid
                self._nickname = nickname or username
                self._save_local_profile()
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
                        self._account_uuid = account_uuid
                        self._nickname = nickname or username
                        self._save_local_profile()
                        self._cb(callback, (True, "注册成功"))
                        return
                self._cb(callback, (False, "存档仓库创建失败"))
                return
            if resp.status_code == 422:
                self._cb(callback, (False, "用户名已存在"))
                return
            msg = _ERROR_MESSAGES.get(resp.status_code, f"注册失败({resp.status_code})")
            self._cb(callback, (False, msg))
        threading.Thread(target=_do, daemon=True).start()

    def login(self, username, password, callback=None):
        """Login with username + password. Verifies password hash."""
        def _do():
            if not requests:
                return self._cb(callback, (False, "网络库不可用"))
            try:
                data = self._get_file(username)
            except:
                return self._cb(callback, (False, "网络连接失败"))
            if data is None:
                return self._cb(callback, (False, "账号不存在"))
            account_uuid = data.get("uuid", "")
            pwd_hash = data.get("password_hash")
            if not account_uuid or not pwd_hash:
                return self._cb(callback, (False, "账号数据损坏"))
            if _hash_password(password, account_uuid) != pwd_hash:
                return self._cb(callback, (False, "密码错误"))
            self._username = username
            self._account_uuid = account_uuid
            self._nickname = data.get("nickname", username)
            self._save_local_profile()
            self._cb(callback, (True, "登录成功", data))
        threading.Thread(target=_do, daemon=True).start()

    def change_nickname(self, new_nickname, callback=None):
        if not self._username or not requests:
            return self._cb(callback, (False, "未登录"))
        def _do():
            try:
                data = self._get_file(self._username)
            except:
                return self._cb(callback, (False, "网络连接失败"))
            if data is None:
                return self._cb(callback, (False, "账号不存在"))
            data["nickname"] = new_nickname
            try:
                resp = self._put_file(self._username, data)
            except:
                return self._cb(callback, (False, "网络连接失败"))
            if resp.status_code in [200, 201]:
                self._nickname = new_nickname
                self._save_local_profile()
                self._cb(callback, (True, "昵称已修改"))
            else:
                self._cb(callback, (False, _ERROR_MESSAGES.get(resp.status_code, "修改失败")))
        threading.Thread(target=_do, daemon=True).start()

    def upload(self, save_data, callback=None):
        """Upload save data to cloud. Non-blocking."""
        if not self._username or not requests:
            return
        self._syncing = True
        def _do():
            data = {"uuid": self._account_uuid, "username": self._username,
                    "nickname": self._nickname or self._username,
                    "password_hash": self._password_hash if hasattr(self, '_password_hash') else None,
                    "save": save_data, "last_sync": time.time()}
            try:
                existing = self._get_file(self._username)
                if existing:
                    data["uuid"] = existing.get("uuid", self._account_uuid)
                    data["password_hash"] = existing.get("password_hash")
                    data["registered_at"] = existing.get("registered_at", time.time())
            except:
                pass
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
