"""
modules/port_scanner.py

Módulo que contiene la clase `PortScanner`, encargada de realizar el
escaneo de puertos de un servidor a partir de una URL o dirección IP
ingresada por el usuario, y de generar un informe con recomendaciones.

Requerimiento 1 (Escaneo basado en URL) y parte del Requerimiento 3
(Informe) de la Entrega 1 se resuelven en este módulo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlparse

import nmap


@dataclass
class ResultadoPuerto:
    """Representa el resultado del escaneo de un puerto específico."""

    puerto: int
    protocolo: str
    estado: str
    servicio: str


@dataclass
class ResultadoEscaneo:
    """Representa el resultado completo del escaneo de un host."""

    objetivo: str
    host: str
    estado_host: str
    puertos: list[ResultadoPuerto] = field(default_factory=list)

    @property
    def puertos_abiertos(self) -> list[ResultadoPuerto]:
        return [p for p in self.puertos if p.estado == "open"]


class PortScanner:
    """
    Encapsula el escaneo de puertos de un host usando la librería
    `python-nmap`.

    Uso básico:
        scanner = PortScanner()
        resultado = scanner.escanear("https://ejemplo.com")
        informe = scanner.generar_informe(resultado)
    """

    PUERTOS_POR_DEFECTO = "22,80,443,8080"

    # Recomendaciones básicas asociadas a puertos comunes. Este diccionario
    # se irá ampliando en la Entrega 2 con más puertos y detalle.
    RECOMENDACIONES = {
        21: "El puerto FTP (21) suele transportar credenciales sin cifrar; "
            "considera reemplazarlo por SFTP/FTPS o cerrarlo si no se usa.",
        22: "El puerto SSH (22) está abierto; asegúrate de deshabilitar el "
            "acceso por contraseña y usar autenticación por llave.",
        23: "El puerto Telnet (23) transmite la información sin cifrar; "
            "se recomienda deshabilitarlo y usar SSH en su lugar.",
        80: "El puerto HTTP (80) está abierto; si el servicio expone "
            "información sensible, redirige el tráfico a HTTPS (443).",
        443: "El puerto HTTPS (443) está abierto; verifica que el "
             "certificado TLS esté vigente y correctamente configurado.",
        3306: "El puerto de MySQL (3306) está expuesto; restringe el "
              "acceso solo a hosts de confianza mediante firewall.",
        3389: "El puerto de Escritorio Remoto (3389) está expuesto a la "
              "red; considera usar una VPN en lugar de exponerlo "
              "directamente.",
        8080: "El puerto 8080 (proxy/HTTP alterno) está abierto; verifica "
              "que el servicio que lo usa esté actualizado y protegido.",
    }

    def __init__(self, puertos: str = PUERTOS_POR_DEFECTO):
        self.puertos = puertos
        self._scanner = nmap.PortScanner()

    @staticmethod
    def extraer_host(url: str) -> str:
        """
        Obtiene el host (dominio o IP) a partir de una URL o de un texto
        ingresado directamente por el usuario (p. ej. "ejemplo.com",
        "http://ejemplo.com" o "192.168.1.10").
        """
        url = url.strip()
        if "://" not in url:
            url = f"//{url}"
        parsed = urlparse(url)
        return parsed.hostname or url.lstrip("/")

    def escanear(self, url: str) -> ResultadoEscaneo:
        """
        Ejecuta el escaneo de puertos sobre el host obtenido a partir de
        `url` y devuelve un `ResultadoEscaneo`.
        """
        host = self.extraer_host(url)

        if not host:
            raise ValueError("La URL ingresada no es válida.")

        try:
            self._scanner.scan(host, self.puertos)
        except nmap.PortScannerError as ex:
            raise ValueError(f"Error de Nmap: {ex}") from ex

        hosts = self._scanner.all_hosts()

        if not hosts:
            raise ValueError(
                f"No fue posible escanear '{host}'. Verifica que la URL "
                "sea correcta y que el host esté accesible."
            )

        # Nmap puede resolver un dominio a una dirección IP.
        # Usamos el host que Nmap devuelve realmente.
        host_nmap = hosts[0]

        estado_host = self._scanner[host_nmap].state()

        resultado = ResultadoEscaneo(
            objetivo=url,
            host=host_nmap,
            estado_host=estado_host,
        )

        for protocolo in self._scanner[host_nmap].all_protocols():
            for puerto in sorted(self._scanner[host_nmap][protocolo]):
                datos = self._scanner[host_nmap][protocolo][puerto]

                resultado.puertos.append(
                    ResultadoPuerto(
                        puerto=puerto,
                        protocolo=protocolo,
                        estado=datos.get("state", "desconocido"),
                        servicio=datos.get("name", ""),
                    )
                )

        return resultado


    def generar_informe(self, resultado: ResultadoEscaneo) -> str:
        lineas = [
            f"Informe de escaneo para: {resultado.objetivo}",
            f"Host analizado: {resultado.host} ({resultado.estado_host})",
            "",
        ]

        if not resultado.puertos_abiertos:
            lineas.append(
                "No se encontraron puertos abiertos entre los analizados "
                f"({self.puertos})."
            )
        else:
            lineas.append("Puertos abiertos encontrados:")
            for p in resultado.puertos_abiertos:
                servicio = p.servicio or "desconocido"
                lineas.append(f"  - Puerto {p.puerto}/{p.protocolo} ({servicio})")

            lineas.append("")
            lineas.append("Recomendaciones:")
            recomendaciones_dadas = False
            for p in resultado.puertos_abiertos:
                recomendacion = self.RECOMENDACIONES.get(p.puerto)
                if recomendacion:
                    lineas.append(f"  - Puerto {p.puerto}: {recomendacion}")
                    recomendaciones_dadas = True

            if not recomendaciones_dadas:
                lineas.append(
                    "  - No hay recomendaciones específicas para los "
                    "puertos encontrados; revisa que cada servicio "
                    "expuesto sea realmente necesario."
                )
            lineas.append(
                "  - En general, cierra o filtra con un firewall los "
                "puertos y servicios que no sean estrictamente necesarios."
            )

        return "\n".join(lineas)
