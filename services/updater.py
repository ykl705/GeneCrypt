"""Auto-update via GitHub Releases — download APK + open installer."""
import os, threading, time

try:
    import requests
except ImportError:
    requests = None

APP_VERSION = "0.1.1"
REPO = "ykl705/GeneCrypt"


def _parse_version(v):
    try:
        return tuple(int(x) for x in v.lstrip('v').split('.')[:3])
    except:
        return (0, 0, 0)


def check_update(callback=None):
    """Check latest GitHub Release version. callback(latest_version, download_url)."""
    def _do():
        if not requests:
            return _cb(callback, (None, None))
        try:
            r = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest",
                             timeout=10, verify=False)
            if r.status_code != 200:
                return _cb(callback, (None, None))
            data = r.json()
            latest = data.get("tag_name", "").lstrip('v')
            dl_url = None
            for asset in data.get("assets", []):
                if asset.get("name", "").endswith(".apk"):
                    dl_url = asset.get("browser_download_url")
                    break
            _cb(callback, (latest, dl_url))
        except:
            _cb(callback, (None, None))
    threading.Thread(target=_do, daemon=True).start()


def has_update(latest):
    return _parse_version(latest) > _parse_version(APP_VERSION)


def download_apk(download_url, progress_cb=None, done_cb=None):
    """Download APK to app storage. progress_cb(pct). done_cb(path or None)."""
    def _do():
        if not requests:
            return _cb2(done_cb, None)
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        apk_path = os.path.join(base, "update.apk")
        try:
            r = requests.get(download_url, stream=True, timeout=60, verify=False)
            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(apk_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=65536):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total and progress_cb:
                        pct = int(downloaded * 100 / total)
                        progress_cb(pct)
            _cb2(done_cb, apk_path)
        except:
            _cb2(done_cb, None)
    threading.Thread(target=_do, daemon=True).start()


def open_installer(apk_path):
    """Open Android package installer for the downloaded APK."""
    try:
        from jnius import autoclass
        from android.storage import app_storage_path
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        File = autoclass('java.io.File')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        f = File(apk_path)
        uri = Uri.fromFile(f)
        intent = Intent(Intent.ACTION_VIEW)
        intent.setDataAndType(uri, "application/vnd.android.package-archive")
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        PythonActivity.mActivity.startActivity(intent)
        return True
    except:
        return False


def _cb(callback, result):
    if callback:
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: callback(result), 0)


def _cb2(callback, result):
    if callback:
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: callback(result), 0)
