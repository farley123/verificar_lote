
import flet as ft
from crop2 import Crop
from selecao_tanques import selecao_tanques
import cv2
import base64

from verificacao_imagem import verificar_imagem


def main(page: ft.Page):
    toggle:bool=False
    page.title = 'Verificação de carimbo linha SIG'
    page.window.full_screen=True

    def fullscreen(e):
        nonlocal toggle
        toggle=not toggle
        page.window.full_screen= toggle
        page.update()
        print(toggle)

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.VERIFIED),
        leading_width=40,
        title=ft.Text("Verificação de carimbo SIG"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[

            ft.IconButton(ft.Icons.FULLSCREEN,on_click=fullscreen),

            ft.PopupMenuButton(
                tooltip='Menu',
                items=[
                    ft.PopupMenuItem(text="Ir para:"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Verificação de carimbos"
                    ),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Seleção de tanques"
                    ),
                ]
            ),
        ],
    )

    principal = ft.Container(
        content=ft.Row(
            controls=[
                selecao_tanques(page),
                verificar_imagem(page)

            ]
        )
    )

    page.add(principal)

    #page.run_task(capturar_camera, image_output)







ft.app(main, assets_dir="assets")
