import vk_api
import os


_session = None

def get_session():
    global _session
    if _session:
        return _session
    _session = vk_api.VkApi(token=os.environ.get("TOKEN"))
    return _session
