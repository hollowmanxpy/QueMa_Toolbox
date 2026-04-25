import urllib.request
import urllib.error
import json
import threading

CURRENT_VERSION = "1.1.0"
# 使用您提供的 GitHub 仓库地址
CHECK_URL = "https://api.github.com/repos/hollowmanxpy/QueMa_Toolbox/releases/latest"


def check_for_updates(callback):
    """
    异步检查更新。不会阻塞主线程。
    :param callback: 接收 (has_update, latest_version, download_url)
    """

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
        # 修复了宽泛异常警告，精确捕获网络与解析错误
        except (urllib.error.URLError, json.JSONDecodeError):
            callback(False, CURRENT_VERSION, "")

    threading.Thread(target=_task, daemon=True).start()