import flet as ft
from controle import Controle

def historico(page: ft.Page):
    dados =Controle.lista_de_controles

    def filtrar_dados(data_selecionada):
        linhas.controls.clear()

        if not data_selecionada:
            linhas.controls.append(
                ft.Container(
                    content=ft.Text(value='Data não selecionada.', color=ft.Colors.BLACK, size=20)
                )
            )
            linhas.update()
            return

        # Formata a data para comparar com a lista
        data_formatada = data_selecionada.strftime("%d-%m-%Y")
        campo_data.value = data_formatada
        page.update()

        encontrou = False  # Flag para verificar se encontrou algum item

        for item in dados:
            if item.data == data_formatada:
                encontrou = True
                linhas.controls.append(
                    ft.Row(
                        expand=True,
                        controls=[
                            ft.TextField(value=item.hora, read_only=True, label='hora', max_lines=4, multiline=True,
                                         width=150, bgcolor=ft.Colors.WHITE),
                            ft.TextField(value=item.data, read_only=True, label='data', max_lines=4, multiline=True,
                                         width=150, bgcolor=ft.Colors.WHITE),
                            ft.TextField(value=item.padrao, read_only=True, label='padrão', max_lines=4, multiline=True,
                                         width=400, bgcolor=ft.Colors.WHITE),
                            ft.TextField(value=item.valor_identificado, read_only=True, label='valor identificado',
                                         max_lines=4, multiline=True, width=400, bgcolor=ft.Colors.WHITE),
                            ft.TextField(value=item.comentario, read_only=True, label='comentario', max_lines=4,
                                         multiline=True, width=300, bgcolor=ft.Colors.WHITE),
                        ]
                    )
                )

        if not encontrou:
            linhas.controls.append(
                ft.Container(
                    content=ft.Text(value='Não foram encontrados controles', color=ft.Colors.BLACK, size=20)
                )
            )

        linhas.update()

    return ft.Container(
        expand=True,
        padding=ft.padding.only(left=10,top=10),

        visible=False,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Text(value='Histórico',size=70,color=ft.Colors.BLUE,weight=ft.FontWeight.BOLD),

                ft.Row(

                    controls=[
                        campo_data := ft.TextField(
                            label='Data',
                            read_only=True,
                            width=250,
                            border_radius=10,
                            bgcolor=ft.Colors.WHITE
                        ),
                        botao_selecionar_data := ft.ElevatedButton("selecionar data", on_click=lambda e: page.open(
                            ft.DatePicker(
                                on_change=lambda f: filtrar_dados(f.control.value)
                            )
                        ))
                    ]
                ),
                ft.Container(expand=True,height=50),

                linhas:=ft.Column(
                    expand=True,

                    controls=[]
                ),


            ]
        )
    )
