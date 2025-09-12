import subprocess
import pytest
import sys
import os
from playwright.sync_api import sync_playwright

NAMESPACE = "testns"
IP_ADDR = "1.2.3.4/24"

def setup_namespace():
    print(f"[ns] Création du namespace {NAMESPACE} avec IP {IP_ADDR}")
    subprocess.run(f"sudo ip netns add {NAMESPACE}", shell=True, check=True)
    subprocess.run(f"sudo ip link add veth0 type veth peer name veth1", shell=True, check=True)
    subprocess.run(f"sudo ip link set veth1 netns {NAMESPACE}", shell=True, check=True)
    subprocess.run(f"sudo ip addr add {IP_ADDR} dev veth0", shell=True, check=True)
    subprocess.run(f"sudo ip netns exec {NAMESPACE} ip addr add {IP_ADDR} dev veth1", shell=True, check=True)
    subprocess.run(f"sudo ip link set veth0 up", shell=True, check=True)
    subprocess.run(f"sudo ip netns exec {NAMESPACE} ip link set lo up", shell=True, check=True)
    print("[ns] Namespace prêt")

def cleanup_namespace():
    print(f"[ns] Suppression du namespace {NAMESPACE}")
    subprocess.run(f"sudo ip netns delete {NAMESPACE}", shell=True)

@pytest.fixture
def network_namespace():
    """
    Fixture pour exécuter un test dans un namespace réseau temporaire.
    Tout Playwright lancé dans ce test utilisera IP_ADDR comme IP source.
    """
    setup_namespace()
    try:
        yield
    finally:
        cleanup_namespace()