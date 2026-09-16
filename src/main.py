import flet as ft

from modules.port_scanner import PortScanner


def main(page: ft.Page):
    page.title = "Escáner de puertos"

    scanner = PortScanner()

    async def escanear(e):
        url = url_box.value.strip() if url_box.value else ""
        if not url:
            result.value = "Por favor ingresa una URL o dirección IP."
            page.update()
            return

        send_btn.disabled = True
        url_box.disabled = True
        result.value = f"Escaneando {url} ..."
        page.update()

        try:
            resultado = scanner.escanear(url)
            result.value = scanner.generar_informe(resultado)
        except ValueError as ex:
            result.value = str(ex)
        except Exception as ex:  # cualquier otro error inesperado del escaneo
            result.value = f"Ocurrió un error inesperado al escanear: {ex}"
        finally:
            send_btn.disabled = False
            url_box.disabled = False
            page.update()

    url_box = ft.TextField(label="URL o dirección IP", hint_text="ej. https://ejemplo.com", expand=True)
    send_btn = ft.Button("Escanear", on_click=escanear)
    result = ft.Text(
        "Ingresa una URL o dirección IP y haz clic en Escanear.",
        selectable=True,
    )

    page.add(
        ft.Row(controls=[url_box, send_btn]),
        ft.Row(controls=[result], expand=True),
    )


if __name__ == "__main__":
    ft.run(main)
