import cv2
import base64

from controle import Controle
from crop2 import Crop
import flet as ft
from selecao_tanques import juliano,fabricacao,validade
from ocr import resultado_ocr
from datetime import datetime





def verificar_imagem(page:ft.Page):
    crop = Crop(page)
    exibir_padrao=ft.Text(value='')
    exibir_ocr=ft.Text(value='')
    image_output = ft.Image(fit=ft.ImageFit.FILL)
    modal_salvar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Salvar controle"),
        content=ft.Text("Você tem certeza que deseja salvar?"),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: close_modal(e)),
            ft.TextButton("Confirmar", on_click=lambda e: confirm_action(e))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def close_modal(e):
        modal_salvar.open = False
        page.update()

    def confirm_action(e):
        modal_salvar.open = False
        page.snack_bar = ft.SnackBar(ft.Text("Ação confirmada!"))
        page.snack_bar.open = True
        page.update()
        controle= Controle(
            hora=datetime.now().strftime('%H:%M'),
            data=datetime.now().strftime("%d-%m-%Y"),
            padrao=exibir_padrao.value[:-5].strip(),
            valor_identificado=exibir_ocr.value[0:69].strip(),
            comentario=comentario.content.value
        )
        controle.adicionar_controle(controle)
        comentario.visible=False
        comentario.content.value=''
        exibir_ocr.value=''
        habilitar_salvar_modal.visible=False
        ocr_correto_icone.visible = False
        ocr_incorreto_icone.visible=False
        page.update()

    imagem_cortada = ft.Image(src='assets/imagem_cortada.jpg')
    # Lista para armazenar os quadros capturados
    capturas = []
    captura_em_andamento = True  # Variável para controlar o loop de captura

    def chamar_modal(e):
        page.dialog = modal_salvar
        modal_salvar.open = True
        page.update()

    def verificar_ocr_igual_padrao(e):
        capture_button.visible=False
        verificar_button.visible=False
        print('padrao:',exibir_padrao.value[:-5])
        print('ocr:', exibir_ocr.value[0:69])
        if exibir_padrao.value[:-5].strip() == exibir_ocr.value[0:69].strip():
            ocr_incorreto_icone.visible=False
            page.update()
            ocr_correto_icone.visible=True
            habilitar_salvar_modal.visible=True
            crop_button.visible=False
            comentario.visible=True
            page.update()
            print('carimbos iguais')
        else:
            ocr_correto_icone.visible=False
            page.update()
            ocr_incorreto_icone.visible = True
            habilitar_salvar_modal.visible = False
            print('carimbos diferentes')

            crop_button.visible=False
            page.update()





    def atualizar_padrao(_=None):
        exibir_padrao.value = (
            "VÁLIDO ATÉ / VALIDO HASTA / LOTE:\n"
            f"{validade.get()}\n"
            f"{juliano.get()}\n"
            f"{fabricacao.get()}"
        )
        page.update()

    def atualizar_ocr(_=None):
        exibir_ocr.value =(
            "VÁLIDO ATÉ / VALIDO HASTA / LOTE:\n"
            f"{resultado_ocr.get()}\n"
        )

        page.update()

    resultado_ocr.subscribe(atualizar_ocr)
    validade.subscribe(atualizar_padrao)
    juliano.subscribe(atualizar_padrao)
    fabricacao.subscribe(atualizar_padrao)

    def ajustar_largura_area_de_corte(e):
        nova_largura = float(e.control.value)

        # Limite da direita da imagem (imagem começa em x = 10 por causa da margem)
        limite_direita = crop.imagem_width + 10
        largura_maxima = limite_direita - crop.left_area

        # Aplicar limite
        nova_largura = min(nova_largura, largura_maxima)

        # Atualizar o crop
        crop.largura_area_corte = nova_largura
        gesture.content.width = nova_largura
        gesture.content.update()



    def ajustar_altura_area_de_corte(e):
        nova_altura = float(e.control.value)

        # Limite da direita da imagem (imagem começa em x = 10 por causa da margem)
        limite_inferior = crop.imagem_height
        altura_maxima = limite_inferior - crop.top_area

        # Aplicar limite
        nova_altura = min(nova_altura, altura_maxima)

        # Atualizar o crop
        crop.altura_area_corte = nova_altura
        gesture.content.height = nova_altura
        gesture.content.update()

    def capturar_camera(img_output):

        crop.desabilitar_crop(gesture)
        nonlocal captura_em_andamento, capturas
        if captura_em_andamento:
            print('captura em andamente,ignorando')
        #desabilita o botao de tirar foto para que o usuario nao ligue a camera já ligada
        inicar_camera.disabled = True
        inicar_camera.visible = False
        page.update()
        cap = cv2.VideoCapture(0)  # Inicializa a câmera
        #verificar se a camera realmente iniciou
        if not cap.isOpened():
            print('erro ao abrir a camera')
            return
        try:
            while captura_em_andamento:
                ret, frame = cap.read()
                if not ret:
                    break

                # Não converte para RGB, mantém em BGR, que é o padrão do OpenCV
                frame_bgr = frame

                # Converte a imagem para JPEG e depois para base64
                _, buffer = cv2.imencode('.jpg', frame_bgr)
                img_bytes = buffer.tobytes()
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')

                # Atualiza a imagem no app Flet de forma assíncrona
                img_output.src_base64 = img_base64
                img_output.update()

                # Armazena o quadro atual na lista (se necessário)
                capturas.append(frame)
        except Exception as e:
            print(f"Erro durante captura: {e}")

        finally:
            captura_em_andamento = False
            if 'cap' in locals() and cap.isOpened():
                try:
                    cap.release()
                except cv2.error as e:
                    print(f"Erro ao liberar câmera: {e}")

    # Função assíncrona para reiniciar a câmera
    def reiniciar_camera(img_output):
        resultado_ocr.set('')
        ocr_correto_icone.visible=False
        ocr_incorreto_icone.visible=False
        verificar_button.visible=False
        comentario.visible=False

        habilitar_salvar_modal.visible=False
        crop_button.visible=False

        #habilita o botao de tirar foto
        capture_button.visible=True
        page.update()
        nonlocal captura_em_andamento, capturas
        captura_em_andamento = True  # Reinicia o controle do loop de captura
        capturas.clear()
        capturar_camera(img_output)



    def tirar_foto(img_output):
        nonlocal capturas, captura_em_andamento
        if capturas:
            # Pega o último quadro da lista de capturas
            captura = capturas[-1]

            # Salva a foto
            filename = f"foto_capturada.jpg"  # Nome único para cada foto
            cv2.imwrite(filename, captura)  # Salva a imagem capturada

            # Exibe a foto capturada
            img_output.src_base64 = base64.b64encode(cv2.imencode('.jpg', captura)[1].tobytes()).decode('utf-8')

            img_output.update()
            crop.habilitar_crop(gesture)
            # Pausa o loop da câmera
            captura_em_andamento = False
            #após tirar a foto habilita ligar a camera novamente
            inicar_camera.disabled = False
            capture_button.visible=False
            inicar_camera.visible = True
            crop_button.visible = True
            gesture.visible=True
            page.update()

    def resetar_crop(slider_largura:ft.Slider,slider_altura:ft.Slider,gesture_detector:ft.GestureDetector):
        crop.left_area = 10
        crop.top_area = 10
        crop.largura_area_corte = 100
        crop.altura_area_corte = 100

        gesture_detector.left = crop.left_area
        gesture_detector.top = crop.top_area
        gesture_detector.content.width = crop.largura_area_corte
        gesture_detector.content.height = crop.altura_area_corte
        gesture_detector.update()

        slider_largura.max = crop.imagem_width - crop.left_area
        slider_largura.value = crop.largura_area_corte
        slider_largura.update()

        slider_altura.max = crop.imagem_height - crop.top_area
        slider_altura.value = crop.altura_area_corte
        slider_altura.update()

        page.update()

    def cortar_imagem(e):

        gesture.visible = True
        page.update()
        crop.crop_picture()
        e.control.visible=False
        gesture.visible=False
        verificar_button.visible = True
        # resetar crop
        resetar_crop(ajustar_largura_slider, ajustar_altura_slider, gesture)
        page.update()

    return ft.Container(
        visible=False,
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(

            controls=[

                ft.Container(
                    padding=ft.padding.all(15),
                    expand=True,
                    bgcolor=ft.Colors.BLACK,
                    content=ft.Column(


                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Stack(

                                                        controls=[
                                                            ft.Container(width=640, height=480,
                                                                         content=image_output,
                                                                         bgcolor='pink',
                                                                         margin=ft.margin.only(left=10)),
                                                            gesture := crop.criar_gesture_detector()

                                                        ]
                                                    ),

                                                    padrao:=ft.Container(
                                                        width=640,
                                                        height=480,

                                                        bgcolor=ft.Colors.PINK,
                                                        content=ft.Column(
                                                            controls=[
                                                                ft.Column(
                                                                    controls=[
                                                                        ft.Text(value="Padrão",size=30,color=ft.Colors.WHITE),
                                                                        ft.Container(
                                                                            width=400,
                                                                            height=100,
                                                                            border_radius=10,
                                                                            margin=ft.margin.only(left=10, top=10),
                                                                            padding=ft.padding.only(top=10, left=10),
                                                                            bgcolor=ft.Colors.BLUE,
                                                                            content=exibir_padrao
                                                                        ),
                                                                        ft.Text(value="Valor identificado", size=30,
                                                                                color=ft.Colors.WHITE),

                                                                        ft.Row(
                                                                            controls=[
                                                                                valor_identificado_content:=ft.Container(
                                                                                    width=400,
                                                                                    height=100,
                                                                                    border_radius=10,
                                                                                    margin=ft.margin.only(left=10,
                                                                                                          top=10),
                                                                                    padding=ft.padding.only(top=10,
                                                                                                            left=10),
                                                                                    bgcolor=ft.Colors.BLUE,
                                                                                    content=exibir_ocr

                                                                                ),
                                                                                ocr_correto_icone:=ft.Icon(
                                                                                    visible=False,
                                                                                    name=ft.Icons.VERIFIED_ROUNDED,
                                                                                    size=100,
                                                                                    color=ft.Colors.GREEN
                                                                                ),
                                                                                ocr_incorreto_icone:=ft.Icon(
                                                                                    visible=False,
                                                                                    name=ft.Icons.DANGEROUS_ROUNDED,
                                                                                    size=100,
                                                                                    color=ft.Colors.RED
                                                                                )

                                                                            ]
                                                                        ),
                                                                        ft.Row(
                                                                            controls=[
                                                                                comentario:=ft.Container(
                                                                                    visible=False,
                                                                                    margin=ft.margin.only(left=10,
                                                                                                          top=10),
                                                                                    content=ft.TextField(
                                                                                        border_radius=10,
                                                                                        bgcolor=ft.Colors.BLUE,
                                                                                        label='comentário',
                                                                                        label_style=ft.TextStyle(
                                                                                            color=ft.Colors.WHITE),
                                                                                        multiline=True,
                                                                                        width=400,

                                                                                        max_lines=2
                                                                                    ),
                                                                                ),
                                                                            ]
                                                                        ),


                                                                        ft.Row(
                                                                            controls=[

                                                                                verificar_button:=ft.ElevatedButton(text='Verificar',on_click=verificar_ocr_igual_padrao,visible=False),
                                                                                habilitar_salvar_modal:=ft.ElevatedButton(text='Salvar',on_click=chamar_modal,visible=False),

                                                                                modal_salvar

                                                                            ]
                                                                        )

                                                                    ]
                                                                )



                                                            ]
                                                        )

                                                    )
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Column(
                                                        controls=[
                                                            ft.Row(
                                                                spacing=150,
                                                                controls=[
                                                                    ft.Text(value='ajustar altura',color=ft.Colors.WHITE),

                                                                    ft.Text(value='ajustar lagura',color=ft.Colors.WHITE)
                                                                ]

                                                            ),
                                                            ft.Row(

                                                                controls=[
                                                                    ajustar_altura_slider := ft.Slider(
                                                                        min=10,
                                                                        max=crop.imagem_height-crop.top if crop.top>0 else 480,
                                                                        label='{value}%',
                                                                        on_change=ajustar_altura_area_de_corte
                                                                    ),
                                                                    ajustar_largura_slider := ft.Slider(
                                                                        min=10,
                                                                        max=crop.imagem_width-crop.left if crop.left>0 else 640,
                                                                        label='{value}%',
                                                                        on_change=ajustar_largura_area_de_corte
                                                                    )

                                                                ]

                                                            )
                                                        ]
                                                    )
                                                ]
                                            ),

                                            ft.Row(

                                                alignment=ft.MainAxisAlignment.START,
                                                controls=[
                                                    crop_button := ft.ElevatedButton(icon=ft.Icons.CROP_5_4,
                                                                                     text="cortar a foto",
                                                                                     bgcolor=ft.Colors.RED,
                                                                                     visible=False,
                                                                                     on_click=cortar_imagem),

                                                    capture_button := ft.ElevatedButton(icon=ft.Icons.CAMERA,
                                                                                        visible=False,
                                                                                        text="Tirar a foto",
                                                                                        on_click=lambda e: tirar_foto(
                                                                                            image_output)),
                                                    inicar_camera := ft.ElevatedButton(icon=ft.Icons.START,
                                                                                       text="Ligar a câmera",
                                                                                       on_click=lambda
                                                                                           e: reiniciar_camera(
                                                                                           image_output)),

                                                ]
                                            ),

                                        ]
                                    ),



                                ]
                            ),


                        ]
                    )
                ),


            ]
        )
    )