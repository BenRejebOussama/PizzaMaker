import socket
import tempfile
import os
import pytest

# Sauvegarde de la classe socket originale
_original_socket = socket.socket

class BoundSocket(socket.socket):
    _bind_addr = None  # pour IPv4/TCP
    _unix_paths = []   # garder les chemins temporaires pour cleanup

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        bind_addr = getattr(self, "_bind_addr", None)

        if self.family == socket.AF_INET and self.type == socket.SOCK_STREAM:
            if bind_addr:
                try:
                    super().bind((bind_addr, 0))
                    print(f"[shim] Bound IPv4 fd={self.fileno()} to {bind_addr}")
                    self.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    try:
                        self.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                    except OSError:
                        pass
                except Exception as e:
                    print(f"[shim] Impossible de binder IPv4 fd={self.fileno()} sur {bind_addr}: {e}")

        elif self.family == socket.AF_UNIX:
            # Création d'un fichier temporaire pour le bind Unix
            path = tempfile.mktemp(prefix="playwright_", suffix=".sock")
            BoundSocket._unix_paths.append(path)
            try:
                super().bind(path)
                print(f"[shim] Bound Unix fd={self.fileno()} to {path}")
            except Exception as e:
                print(f"[shim] Impossible de binder Unix fd={self.fileno()} sur {path}: {e}")


# Ajouter une option pytest --bind-addr
def pytest_addoption(parser):
    parser.addoption(
        "--bind-addr",
        action="store",
        default=None,
        help="Forcer l'adresse IP pour les sockets créés pendant les tests (IPv4/TCP)."
    )


@pytest.fixture(autouse=False)
def force_bind_addr(request):
    """
    Fixture manuelle : si --bind-addr est fourni, patch socket.socket
    pour la durée du test.
    """
    bind_addr = request.config.getoption("--bind-addr")

    if not bind_addr:
        # Pas de patch si option absente
        yield
        return

    # Injecter l'adresse dans BoundSocket
    BoundSocket._bind_addr = bind_addr
    socket.socket = BoundSocket
    yield

    # Restore socket original
    socket.socket = _original_socket

    # Cleanup des fichiers temporaires Unix
    for path in BoundSocket._unix_paths:
        try:
            os.unlink(path)
            print(f"[shim] Removed temp Unix socket {path}")
        except FileNotFoundError:
            pass
    BoundSocket._unix_paths.clear()