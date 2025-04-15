import cv2
import base64
from crop2 import Crop
import flet as ft


# Lista para armazenar os quadros capturados
capturas = []
captura_em_andamento = True  # Variável para controlar o loop de captura

# Função para capturar a imagem da câmera



# Função assíncrona para capturar a imagem da câmera e atualizar a interface do Flet
def capturar_camera(img_output):
    global captura_em_andamento, capturas
    cap = cv2.VideoCapture(1)  # Inicializa a câmera
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



    cap.release()


# Função assíncrona para capturar uma foto e salvar
def tirar_foto(img_output):
    global capturas, captura_em_andamento
    if capturas:
        # Pega o último quadro da lista de capturas
        captura = capturas[-1]

        # Salva a foto
        filename = f"foto_capturada.jpg"  # Nome único para cada foto
        cv2.imwrite(filename, captura)  # Salva a imagem capturada


        # Exibe a foto capturada
        img_output.src_base64 = base64.b64encode(cv2.imencode('.jpg', captura)[1].tobytes()).decode('utf-8')

        img_output.update()

        # Pausa o loop da câmera
        captura_em_andamento = False


# Função assíncrona para reiniciar a câmera
def  reiniciar_camera(img_output):
    global captura_em_andamento, capturas
    captura_em_andamento = True  # Reinicia o controle do loop de captura
    capturas = []  # Limpa as capturas anteriores
    # Chama a função de captura da câmera de forma assíncrona
    capturar_camera(img_output)

def verificar_imagem(page:ft.Page):
    crop = Crop(page)
    image_output = ft.Image(fit=ft.ImageFit.FILL)
    imagem_cortada = ft.Image(src='assets/imagem_cortada.jpg')

    return ft.Container(
        width=1800,
        height=700,
        visible=True,

        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[

                ft.Container(
                    width=920,
                    height=670,

                    content=ft.Column(
                        alignment=ft.alignment.top_left,
                        offset=(-0.01, 0),
                        controls=[
                            ft.Row(

                                controls=[
                                    ft.Stack(

                                        controls=[
                                            ft.Container(width=640, height=480,
                                                         content=image_output,
                                                         bgcolor='pink', margin=ft.margin.only(left=10)),
                                            gesture := crop.criar_gesture_detector()
                                        ]
                                    ),
                                    ft.Container(
                                        width=640, height=480, bgcolor=ft.Colors.PINK,
                                        content=imagem_cortada
                                    )

                                ]
                            ),
                            ft.Row(
                                controls=[
                                    crop_button := ft.ElevatedButton(text="crop imagem", bgcolor=ft.Colors.RED,
                                                                     on_click=lambda e: crop.crop_picture(imagem_cortada,
                                                                                                          gesture)),
                                    capture_button := ft.ElevatedButton(text="Capturar Foto",
                                                                        on_click=lambda e: tirar_foto(
                                                                            image_output)),
                                    start_button := ft.ElevatedButton(text="Reiniciar Câmera",
                                                                      on_click=lambda e: reiniciar_camera(image_output)),

                                ]
                            )

                        ]
                    )
                ),

            ]
        )
    )