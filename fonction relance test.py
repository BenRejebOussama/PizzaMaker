import pytest

def conditional_retry(should_retry_func):
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            try:
                return test_func(*args, **kwargs)
            except AssertionError:
                if should_retry_func():
                    # une seule relance
                    return test_func(*args, **kwargs)
                raise
        return wrapper
    return decorator

# Exemple d'une fonction qui décide si on relance
def should_retry():
    # ici tu peux mettre ton API call, logique métier, etc.
    return True

@pytest.mark.parametrize("page", ["homepage"], indirect=True)
@conditional_retry(should_retry)
def test_example(page):
    page.goto("https://example.com")
    assert page.title() == "Not the expected title"  # volontairement faux