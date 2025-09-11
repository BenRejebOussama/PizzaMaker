import os
import socket
import pytest

# On garde une référence de la classe socket originale
_original_socket = socket.socket


class BoundSocket(socket.socket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        bind_addr = os.getenv("BIND_ADDR")
        if bind_addr and self.family == socket.AF_INET and self.type == socket.SOCK_STREAM:
            try:
                # Bind sur BIND_ADDR avec un port libre
                self.bind((bind_addr, 0))

                # Activer low-latency (TCP_NODELAY / TCP_QUICKACK)
                self.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                try:
                    self.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                except OSError:
                    pass  # Pas dispo partout
            except Exception as e:
                print(f"[shim] Impossible de binder sur {bind_addr}: {e}")


@pytest.fixture(autouse=False)
def force_bind_addr():
    """
    Fixture manuelle : si BIND_ADDR est défini,
    patch socket.socket -> BoundSocket pour la durée du test.
    """
    if not os.getenv("BIND_ADDR"):
        # Rien à faire si pas de BIND_ADDR
        yield
        return

    socket.socket = BoundSocket
    yield
    socket.socket = _original_socket