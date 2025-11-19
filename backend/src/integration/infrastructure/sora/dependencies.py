import random

from src.integration.infrastructure.sora.adapter import SoraRestAdapter
from src.integration.infrastructure.sora.llm_provider import get_provider_config
from src.integration.infrastructure.sora.llm_provider.browsers.chrome import ChromeBrowser
from src.integration.infrastructure.sora.llm_provider.directors.sora import SoraDirector
from src.integration.infrastructure.sora.task_repository import SoraTaskRepository


def get_sora_task_repository():
    return SoraTaskRepository()


def get_sora_rest_adapter():
    return SoraRestAdapter(get_sora_task_repository())


# Lazy initialization of browsers
_browsers = None

def _get_browsers():
    global _browsers
    if _browsers is None:
        _browsers = [
            ChromeBrowser(get_sora_rest_adapter(), browser_name="chrome"),
            ChromeBrowser(get_sora_rest_adapter(), browser_name="chrome2"),
            ChromeBrowser(get_sora_rest_adapter(), browser_name="chrome3")
        ]
    return _browsers


def get_sora_director():
    browsers = _get_browsers()
    browser = random.choice(browsers)
    return SoraDirector(browser, get_provider_config("sora"))