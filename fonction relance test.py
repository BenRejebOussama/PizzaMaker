import pytest

# Flag pour suivre si un test a déjà été relancé
_retry_flag = {}

def should_retry():
    # Ta logique métier : appel API, variable globale, etc.
    return True

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    test_name = item.nodeid
    try:
        yield  # exécute le test normalement
    except Exception:
        if should_retry() and not _retry_flag.get(test_name, False):
            _retry_flag[test_name] = True
            item.obj(**item.funcargs)  # relance une seule fois le test
        else:
            raise