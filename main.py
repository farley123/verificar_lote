
import flet as ft
from selecao_tanques import selecao_tanques
from verificacao_imagem import verificar_imagem
from selecao_tanques import selecao_tanques


def main(page: ft.Page):
    toggle:bool=False
    page.title = 'Verificação de carimbo linha SIG'
    page.window.full_screen=True
    page.padding=0
    page.spacing=0


    def mudar_para_verificacao_de_lote(e):
        tela_selecao_de_tanques.visible = False
        tela_verificacao_de_imagem.visible=True
        page.update()


    def mudar_para_selecao_de_tanque(e):
        tela_selecao_de_tanques.visible=True
        tela_verificacao_de_imagem.visible=False
        page.update()

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
                        text="Verificação de carimbos",
                        on_click=mudar_para_verificacao_de_lote
                    ),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Seleção de tanques",
                        on_click=mudar_para_selecao_de_tanque
                    ),
                ]
            ),
        ],
    )

    principal = ft.Container(
        expand=True,
        content=ft.ResponsiveRow(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        ft.ResponsiveRow(
                            expand=True,
                            controls=[
                                tela_selecao_de_tanques := selecao_tanques(page),
                                tela_verificacao_de_imagem := verificar_imagem(page)
                            ]
                        )
                    ]
                )


            ]
        )
    )

    page.add(principal)









ft.app(main, assets_dir="assets")
