import flet as ft
import cv2
import os
from datetime import datetime
from flet.core.gesture_detector import GestureDetector, DragUpdateEvent
from flet.core.types import MouseCursor
from PIL import Image


def main(page: ft.Page):
    page.window.width = 400

    toparea = ft.Text(value='0')
    leftarea = ft.Text(value='0')

    def takepicture(e):
        if not os.path.exists('assets'):
            os.makedirs('assets')
        cap = cv2.VideoCapture(0)
        cv2.namedWindow('You_face', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('You_face', 300, 200)
        while True:
            ret, frame = cap.read()
            cv2.imshow('You_face', frame)
            key = cv2.waitKey(1)

            if key == ord('s'):
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f'capture.jpg'
                cv2.imwrite(os.path.join('assets', filename), frame)
                print('You successfully saved the image')

                myImage.src = f'assets/{filename}'
                #myImage.src = f'assets/imagem.jpg'
                page.update()
                break
            if key == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def cropmypicture(e):
        # A primeira coisa é esconder o componente editphoto durante o corte
        editphoto.content.visible = False
        page.update()

        # Obter as coordenadas (top, left) e o tamanho (width, height) do editphoto
        top = float(toparea.value)  # Acessando a posição top do GestureDetector
        left = float(leftarea.value)  # Acessando a posição left do GestureDetector
        right = left + float(editphoto.content.width)  # Largura do Container
        bottom = top + float(editphoto.content.height)  # Altura do Container

        # Verificando se as coordenadas estão corretas
        print(f"Coordenadas de corte - Top: {top}, Left: {left}, Right: {right}, Bottom: {bottom}")

        fullscreen = Image.open('assets/imagem2.jpg')

        # Redimensionar a imagem
        resized = fullscreen.resize((640, 480))
        print(f"Tamanho da imagem redimensionada: {resized.size}")  # Para verificar o tamanho da imagem

        # Definir a área para crop
        area = (left, top, right, bottom)

        # Fazer crop
        cropped_image = resized.crop(area)
        print(f"Tamanho da imagem cortada: {cropped_image.size}")  # Para verificar o tamanho após o crop

        # Salvar a imagem cortada apenas se for válida
        if cropped_image is not None:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            cropped_image.save(f'assets/imagem_cortada_{timestamp}.jpg')
            print('Imagem cortada com sucesso!')
            myImage.src = f'assets/imagem_cortada_{timestamp}.jpg'

            page.update()
        else:
            print("Erro: A imagem cortada está inválida ou vazia.")

    def changeposition(e: DragUpdateEvent):
        # Atualizar a posição do editphoto
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        print('top:',e.control.top,'left:', e.control.left)
        toparea.value = max(0, e.control.top)
        leftarea.value = max(0, e.control.left)

        page.update()

    def changesize(e):
        # Atualizar o tamanho do editphoto com base no slider
        editphoto.content.width = e.control.value
        editphoto.content.height = e.control.value
        page.update()

    changesize = ft.Slider(
        min=10,
        max=350,
        value=200,
        label='Change size',
        on_change=changesize
    )

    myImage = ft.Image(src='assets/imagem2.jpg',fit=ft.ImageFit.FILL)
    editphoto = ft.GestureDetector(
        drag_interval=10,
        top=10,
        left=10,
        mouse_cursor=MouseCursor.MOVE,
        on_pan_update=changeposition,
        content=ft.Container(
            border=ft.border.all(5, 'red'),
            width=345,
            height=155,
            visible=True
        )
    )

    def cropagain(e):
        # Exibir novamente o editphoto quando o usuário clicar em "Crop again"
        editphoto.content.visible = True
        page.update()

    page.add(
        ft.Column(
            controls=[
                ft.ElevatedButton('Take your face', on_click=takepicture),
                ft.Stack(
                    controls=[
                        ft.Container(width=640,height=480,content=myImage,bgcolor='pink'),
                        editphoto
                    ]
                ),
                ft.Row(controls=[
                    ft.ElevatedButton(text='Crop my picture', bgcolor='blue', color='white', on_click=cropmypicture),
                    ft.ElevatedButton(text='Crop again', bgcolor='blue', color='white', on_click=cropagain),
                ]),
                changesize,
                toparea,
                leftarea
            ]
        )
    )


ft.app(target=main, assets_dir='assets')
