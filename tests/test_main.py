import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from modules.port_scanner import PortScanner


def test_extraer_host_url_https():
    assert PortScanner.extraer_host("https://ejemplo.com") == "ejemplo.com"


def test_extraer_host_url_http():
    assert PortScanner.extraer_host("http://ejemplo.com") == "ejemplo.com"


def test_extraer_host_sin_protocolo():
    assert PortScanner.extraer_host("ejemplo.com") == "ejemplo.com"


def test_extraer_host_ip():
    assert PortScanner.extraer_host("192.168.1.10") == "192.168.1.10"


def test_extraer_host_url_con_ruta():
    assert PortScanner.extraer_host(
        "https://ejemplo.com/login"
    ) == "ejemplo.com"
