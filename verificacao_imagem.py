import cv2
import base64

import selecao_tanques
from crop2 import Crop
import flet as ft








def verificar_imagem(page:ft.Page):
    crop = Crop(page)

    image_output = ft.Image(fit=ft.ImageFit.FILL)
    imagem_cortada = ft.Image(src='assets/imagem_cortada.jpg')
    # Lista para armazenar os quadros capturados
    capturas = []
    captura_em_andamento = True  # Variável para controlar o loop de captura

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
            inicar_camera.visible = True
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
                                                    imagem_analisar:=ft.Container(
                                                        width=640, height=480, bgcolor=ft.Colors.PINK,
                                                        content=imagem_cortada
                                                    ),
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
                                                                                     on_click=lambda
                                                                                         e: crop.crop_picture(
                                                                                         imagem_cortada,
                                                                                         gesture,ajustar_largura_slider,ajustar_altura_slider)),
                                                    capture_button := ft.ElevatedButton(icon=ft.Icons.CAMERA,
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