import flet as ft
import datetime
from dateutil.relativedelta import relativedelta
import resultado_observable

validade = resultado_observable.ResultadoObservable('')
juliano = resultado_observable.ResultadoObservable('')
fabricacao = resultado_observable.ResultadoObservable('')

def selecao_tanques(page:ft.Page)->ft.Container:
    def on_valor_alterado(_):
        validade_result.value = validade.get()
        data_result.value = juliano.get()
        fabricacao_result.value = fabricacao.get()
        page.update()


        # Registrar os observadores (isso será executado uma única vez)

    validade.subscribe(on_valor_alterado)
    juliano.subscribe(on_valor_alterado)
    fabricacao.subscribe(on_valor_alterado)

    tanque_selecionado:str=''
    def clear():
        data_result.value = ''
        validade_result.value = ''
        fabricacao_result.value = ''
        digito.value = ' '
        produtos.value = ' '
        page.update()

    def ativar_botao_carregar_modelo(e):
        if digito.value != ' ' and produtos.value != ' ' and tanque_selecionado:
            iniciar_modelo.visible = True
            page.update()
        else:
            iniciar_modelo.visible = False
            page.update()

    def calcular_validade(produto: str) -> datetime.date:
        data_atual = datetime.date.today()
        validade_4 = data_atual + relativedelta(months=9)
        validade_light = data_atual + relativedelta(months=7)
        validade_zero = data_atual + relativedelta(months=6)
        match produto:
            case '4%':
                imagem_padrao.image.src='assets/produtos/moca_4.png'
                imagem_padrao.update()
                return datetime.date(day=1, month=validade_4.month, year=validade_4.year)
            case 'moça 340':
                imagem_padrao.image.src = 'assets/produtos/moca_340.png'
                imagem_padrao.update()
                return datetime.date(day=1, month=validade_4.month, year=validade_4.year)
            case 'edição limitada':
                imagem_padrao.image.src = 'assets/produtos/moca_395_edicao_limitada.png'
                imagem_padrao.update()
                return datetime.date(day=1, month=validade_4.month, year=validade_4.year)
            case 'light':
                imagem_padrao.image.src = 'assets/produtos/moca_light.png'
                imagem_padrao.update()
                return datetime.date(day=1, month=validade_light.month, year=validade_light.year)
            case 'zero lactose':
                imagem_padrao.image.src = 'assets/produtos/moca_zero.png'
                imagem_padrao.update()
                return datetime.date(day=validade_zero.day, month=validade_zero.month, year=validade_zero.year)
            case _:
                return datetime.date(0, 0, 0)

    def obter_batch() -> str:
        resultado = ''
        # Obtém a data atual
        hoje = datetime.date.today()
        # Obtém o número do dia dentro do ano (semelhante ao "DayOfYear" em C#)
        dia_do_ano = hoje.timetuple().tm_yday
        ultimo_digito_ano = str(hoje.year)[-1]
        if dia_do_ano < 100:
            resultado = f'L{ultimo_digito_ano}0{dia_do_ano}9264'
        else:
            resultado = f'L{ultimo_digito_ano}{dia_do_ano}9264'
        return resultado

    def preencher_campos(numero_lote: str):
        batch: str = obter_batch()
        data.value = batch[0:5]
        planta.value = batch[5:11]
        lote.value = numero_lote

    def carregar_modelo(e):
        hoje = datetime.date.today()
        validade.set(calcular_validade(produtos.value).strftime("%d %m %Y"))
        juliano.set(f'{data.value}{planta.value}{digito.value}{lote.value}')
        fabricacao.set(f'F{hoje.strftime("%d %m %Y")} 00:00')
        # exibir dados:

        validade_result.value = validade.get()
        data_result.value = juliano.get()
        fabricacao_result.value = fabricacao.get()

        # desabilitar seleção de digito e produto
        digito.disabled = True
        produtos.disabled = True
        page.update()


    def escolher_tanque(e):
        clear()
        iniciar_modelo.visible = False
        digito.disabled = False
        produtos.disabled = False
        nonlocal tanque_selecionado
        match e.control.data:
            case 'T901':
                preencher_campos('1')
                e.control.bgcolor = ft.Colors.GREEN
                e.control.text = 'Envasando'
                t902.bgcolor = ft.Colors.BLACK
                t902.text = 'Parado'
                t903.bgcolor = ft.Colors.BLACK
                t903.text = 'Parado'
                t904.bgcolor = ft.Colors.BLACK
                t904.text = 'Parado'
                t905.bgcolor = ft.Colors.BLACK
                t905.text = 'Parado'
                t906.bgcolor = ft.Colors.BLACK
                t906.text = 'Parado'
                tanque_selecionado='T901'
                page.update()

            case 'T902':
                preencher_campos('2')
                e.control.bgcolor = ft.Colors.GREEN
                e.control.text = 'Envasando'
                t901.bgcolor = ft.Colors.BLACK
                t901.text = 'Parado'
                t903.bgcolor = ft.Colors.BLACK
                t903.text = 'Parado'
                t904.bgcolor = ft.Colors.BLACK
                t904.text = 'Parado'
                t905.bgcolor = ft.Colors.BLACK
                t905.text = 'Parado'
                t906.bgcolor = ft.Colors.BLACK
                t906.text = 'Parado'
                tanque_selecionado='T902'
                page.update()
            case 'T903':
                preencher_campos('3')
                e.control.bgcolor = ft.Colors.GREEN
                e.control.text = 'Envasando'
                t902.bgcolor = ft.Colors.BLACK
                t902.text = 'Parado'
                t901.bgcolor = ft.Colors.BLACK
                t901.text = 'Parado'
                t904.bgcolor = ft.Colors.BLACK
                t904.text = 'Parado'
                t905.bgcolor = ft.Colors.BLACK
                t905.text = 'Parado'
                t906.bgcolor = ft.Colors.BLACK
                t906.text = 'Parado'
                tanque_selecionado='T903'
                page.update()
            case 'T904':
                preencher_campos('4')
                e.control.bgcolor = ft.Colors.GREEN
                e.control.text = 'Envasando'
                t902.bgcolor = ft.Colors.BLACK
                t902.text = 'Parado'
                t903.bgcolor = ft.Colors.BLACK
                t903.text = 'Parado'
                t901.bgcolor = ft.Colors.BLACK
                t901.text = 'Parado'
                t905.bgcolor = ft.Colors.BLACK
                t905.text = 'Parado'
                t906.bgcolor = ft.Colors.BLACK
                t906.text = 'Parado'
                tanque_selecionado='T904'
                page.update()
            case 'T905':
                preencher_campos('5')
                e.control.bgcolor = ft.Colors.GREEN
                e.control.text = 'Envasando'
                t902.bgcolor = ft.Colors.BLACK
                t902.text = 'Parado'
                t903.bgcolor = ft.Colors.BLACK
                t903.text = 'Parado'
                t904.bgcolor = ft.Colors.BLACK
                t904.text = 'Parado'
                t901.bgcolor = ft.Colors.BLACK
                t901.text = 'Parado'
                t906.bgcolor = ft.Colors.BLACK
                t906.text = 'Parado'
                tanque_selecionado='T905'
                page.update()
            case 'T906':
                preencher_campos('6')
                e.control.bgcolor = ft.Colors.GREEN
                e.control.text = 'Envasando'
                t902.bgcolor = ft.Colors.BLACK
                t902.text = 'Parado'
                t903.bgcolor = ft.Colors.BLACK
                t903.text = 'Parado'
                t904.bgcolor = ft.Colors.BLACK
                t904.text = 'Parado'
                t905.bgcolor = ft.Colors.BLACK
                t905.text = 'Parado'
                t901.bgcolor = ft.Colors.BLACK
                t901.text = 'Parado'
                tanque_selecionado='T906'
                page.update()
    return ft.Container(
        expand=True,
        image=ft.DecorationImage(src='assets/fundo.png', fit=ft.ImageFit.COVER, opacity=0.5),
        content=ft.Row(

                    visible=True,
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Container(
                            padding=ft.padding.all(10),
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            data := ft.TextField(width=100, value='', label='data', read_only=True),
                                            planta := ft.TextField(width=100, value='', label='planta da fabrica',
                                                                   read_only=True),
                                            digito := ft.Dropdown(
                                                label='digito',
                                                disabled=True,
                                                on_change=ativar_botao_carregar_modelo,
                                                options=[
                                                    ft.DropdownOption(text=' '),
                                                    ft.DropdownOption(text='0'),
                                                    ft.DropdownOption(text='A'),
                                                    ft.DropdownOption(text='B'),
                                                    ft.DropdownOption(text='C'),
                                                    ft.DropdownOption(text='D'),
                                                    ft.DropdownOption(text='E'),
                                                ]
                                            ),
                                            lote := ft.TextField(width=200, value='', label='lote', read_only=True),

                                            produtos := ft.Dropdown(
                                                label='produto',
                                                disabled=True,
                                                on_change=ativar_botao_carregar_modelo,
                                                options=[
                                                    ft.DropdownOption(text=' '),
                                                    ft.DropdownOption(text='zero lactose'),
                                                    ft.DropdownOption(text='light'),
                                                    ft.DropdownOption(text='4%'),
                                                    ft.DropdownOption(text='moça 340'),
                                                    ft.DropdownOption(text='edição limitada'),

                                                ]
                                            ),
                                            iniciar_modelo := ft.IconButton(
                                                bgcolor=ft.Colors.GREEN,
                                                icon=ft.Icons.PLAY_ARROW,
                                                on_click=carregar_modelo,
                                                visible=False

                                            )

                                        ]
                                    ),
                                    ft.Row(
                                        spacing=200,

                                        controls=[
                                            ft.Column(
                                                controls=[
                                                    ft.Row(
                                                        controls=[
                                                            ft.Stack(
                                                                alignment=ft.alignment.center,
                                                                controls=[
                                                                    ft.Image(src="assets/tanque.png",
                                                                             repeat=ft.ImageRepeat.NO_REPEAT,
                                                                             width=200, height=200),
                                                                    ft.Column(
                                                                        alignment=ft.alignment.center,
                                                                        controls=[
                                                                            ft.Text(
                                                                                value='T901',
                                                                                style=ft.TextStyle(
                                                                                    color=ft.Colors.BLACK,
                                                                                    italic=True,
                                                                                    decoration_thickness=5),
                                                                                offset=ft.Offset(x=0.6, y=0)
                                                                            ),
                                                                            t901 := ft.Button(text="parado",
                                                                                              on_click=escolher_tanque,
                                                                                              data='T901'),
                                                                        ]
                                                                    )

                                                                ]
                                                            ),
                                                            ft.Stack(
                                                                alignment=ft.alignment.center,
                                                                controls=[

                                                                    ft.Image(src="assets/tanque.png",
                                                                             repeat=ft.ImageRepeat.NO_REPEAT,
                                                                             width=200, height=200),
                                                                    ft.Column(
                                                                        alignment=ft.alignment.center,
                                                                        controls=[
                                                                            ft.Text(
                                                                                value='T902',
                                                                                style=ft.TextStyle(
                                                                                    color=ft.Colors.BLACK,
                                                                                    italic=True,
                                                                                    decoration_thickness=5),
                                                                                offset=ft.Offset(x=0.6, y=0)
                                                                            ),
                                                                            t902 := ft.Button(text="parado",
                                                                                              on_click=escolher_tanque,
                                                                                              data='T902'),
                                                                        ]
                                                                    )

                                                                ]
                                                            ),
                                                            ft.Stack(
                                                                alignment=ft.alignment.center,
                                                                controls=[
                                                                    ft.Image(src="assets/tanque.png",
                                                                             repeat=ft.ImageRepeat.NO_REPEAT,
                                                                             width=200, height=200),
                                                                    ft.Column(
                                                                        alignment=ft.alignment.center,
                                                                        controls=[
                                                                            ft.Text(
                                                                                value='T903',
                                                                                style=ft.TextStyle(
                                                                                    color=ft.Colors.BLACK,
                                                                                    italic=True,
                                                                                    decoration_thickness=5),
                                                                                offset=ft.Offset(x=0.6, y=0)
                                                                            ),
                                                                            t903 := ft.Button(text="parado",
                                                                                              on_click=escolher_tanque,
                                                                                              data='T903'),
                                                                        ]
                                                                    )

                                                                ]
                                                            ),

                                                        ]
                                                    ),
                                                    ft.Row(
                                                        controls=[
                                                            ft.Stack(
                                                                alignment=ft.alignment.center,
                                                                controls=[
                                                                    ft.Image(src="assets/tanque.png",
                                                                             repeat=ft.ImageRepeat.NO_REPEAT,
                                                                             width=200, height=200),
                                                                    ft.Column(
                                                                        alignment=ft.alignment.center,
                                                                        controls=[
                                                                            ft.Text(
                                                                                value='T904',
                                                                                style=ft.TextStyle(
                                                                                    color=ft.Colors.BLACK,
                                                                                    italic=True,
                                                                                    decoration_thickness=5),
                                                                                offset=ft.Offset(x=0.6, y=0)
                                                                            ),
                                                                            t904 := ft.Button(text="parado",
                                                                                              on_click=escolher_tanque,
                                                                                              data='T904'),
                                                                        ]
                                                                    )

                                                                ]
                                                            ),
                                                            ft.Stack(
                                                                alignment=ft.alignment.center,
                                                                controls=[
                                                                    ft.Image(src="assets/tanque.png",
                                                                             repeat=ft.ImageRepeat.NO_REPEAT,
                                                                             width=200, height=200),
                                                                    ft.Column(
                                                                        alignment=ft.alignment.center,
                                                                        controls=[
                                                                            ft.Text(
                                                                                value='T905',
                                                                                style=ft.TextStyle(
                                                                                    color=ft.Colors.BLACK,
                                                                                    italic=True,
                                                                                    decoration_thickness=5),
                                                                                offset=ft.Offset(x=0.6, y=0)
                                                                            ),
                                                                            t905 := ft.Button(text="parado",
                                                                                              on_click=escolher_tanque,
                                                                                              data='T905'),
                                                                        ]
                                                                    )

                                                                ]
                                                            ),
                                                            ft.Stack(
                                                                alignment=ft.alignment.center,
                                                                controls=[
                                                                    ft.Image(src="assets/tanque.png",
                                                                             repeat=ft.ImageRepeat.NO_REPEAT,
                                                                             width=200, height=200),
                                                                    ft.Column(
                                                                        alignment=ft.alignment.center,
                                                                        controls=[
                                                                            ft.Text(
                                                                                value='T906',
                                                                                style=ft.TextStyle(
                                                                                    color=ft.Colors.BLACK,
                                                                                    italic=True,
                                                                                    decoration_thickness=5),
                                                                                offset=ft.Offset(x=0.6, y=0)
                                                                            ),
                                                                            t906 := ft.Button(text="parado",
                                                                                              on_click=escolher_tanque,
                                                                                              data='T906'),
                                                                        ]
                                                                    )

                                                                ]
                                                            ),
                                                        ]
                                                    ),

                                                ]
                                            ),







                                        ]
                                    ),

                                    ft.Row(
                                        controls=[
                                            modelo_carimbo := ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text(value="Padrão", size=50),
                                                        ft.Container(
                                                            width=600,
                                                            height=230,
                                                            border_radius=10,
                                                            bgcolor=ft.Colors.BLUE,
                                                            padding=ft.padding.only(left=10, top=10),
                                                            content=ft.Column(
                                                                controls=[
                                                                    ft.Row(
                                                                        controls=[ft.Text(
                                                                            value='VÁLIDO ATÉ/VALIDO HASTA/LOTE:',
                                                                            size=30)]),
                                                                    ft.Row(
                                                                        controls=[validade_result := ft.Text(size=30)]),
                                                                    ft.Row(controls=[data_result := ft.Text(size=30)]),
                                                                    ft.Row(controls=[
                                                                        fabricacao_result := ft.Text(size=30)])

                                                                ]
                                                            )
                                                        )
                                                    ]
                                                )
                                            ),


                                        ]
                                    )
                                ]
                            )
                        ),
                        ft.Column(
                            controls=[
                                ft.Container(height=60),
                                imagem_padrao:=ft.Container(
                                    width=700, height=731,
                                    bgcolor=ft.Colors.RED_900,
                                    border_radius=10,
                                    image=ft.DecorationImage(
                                        src='assets/produtos/logo.png',
                                        fit=ft.ImageFit.FILL,

                                    )
                                )
                            ]
                        )


                    ]
                )
    )


