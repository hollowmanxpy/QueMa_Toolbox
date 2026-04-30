import urllib.request
import urllib.error
import json
import threading

# [修复] 统一升级为 1.2.0，阻断错误的升级提示
CURRENT_VERSION = "1.2.0"
CHECK_URL = "https://api.github.com/repos/hollowmanxpy/QueMa_Toolbox/releases/latest"

def check_for_updates(callback):
    def _task():
        try:
            req = urllib.request.Request(CHECK_URL, headers={'User-Agent': 'QueMa_Office'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                latest_tag = data.get('tag_name', '').replace('v', '')
                download_url = data.get('html_url', '')

                if latest_tag > CURRENT_VERSION:
                    callback(True, latest_tag, download_url)
                else:
                    callback(False, CURRENT_VERSION, "")
        except (urllib.error.URLError, json.JSONDecodeError):
            callback(False, CURRENT_VERSION, "")

    threading.Thread(target=_task, daemon=True).start()