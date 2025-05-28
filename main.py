
import flet as ft
from verificacao_imagem import verificar_imagem
from selecao_tanques import selecao_tanques
from selecao_tanques import validade
from historico import historico


def main(page: ft.Page):
    toggle:bool=False
    page.title = 'DUPLO CHECK DIGITAL SIG'
    page.window.full_screen=True
    page.padding=0
    page.spacing=0


    def mudar_para_verificacao_de_lote(e):
        tela_selecao_de_tanques.visible = False
        tela_historico.visible=False
        tela_verificacao_de_imagem.visible=True

        page.update()


    def mudar_para_selecao_de_tanque(e):
        tela_selecao_de_tanques.visible=True
        tela_verificacao_de_imagem.visible=False
        tela_historico.visible=False
        page.update()

    def mudar_para_historico(e):
        tela_historico.visible=True
        tela_historico.content.controls[3].controls.clear()
        tela_historico.content.controls[1].controls[0].value=''
        tela_verificacao_de_imagem.visible=False
        tela_selecao_de_tanques.visible=False
        page.update()

    def fullscreen(e):
        nonlocal toggle
        toggle=not toggle
        page.window.full_screen= toggle
        page.update()
        print(toggle)




    page.appbar = ft.AppBar(
        leading=ft.Image(src='assets/logo.jpg',repeat=ft.ImageRepeat.NO_REPEAT),
        leading_width=100,

        title=ft.Text("DUPLO CHECK DIGITAL SIG",style=ft.TextStyle(color=ft.Colors.WHITE,weight=ft.FontWeight.BOLD,size=40)),
        center_title=True,
        bgcolor='#0079c0',
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
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Histórico",
                        on_click=mudar_para_historico
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
                                tela_verificacao_de_imagem := verificar_imagem(page),
                                tela_historico:=historico(page)
                            ]
                        )
                    ]
                )


            ]
        )
    )

    page.add(principal)









ft.app(main, assets_dir="assets")
