import flet as ft
import cv2
import os
from datetime import datetime
from flet.core.gesture_detector import GestureDetector, DragUpdateEvent
from flet.core.types import MouseCursor
from PIL import Image
import asyncio

class Crop:
    def __init__(self, page: ft.Page):
        self.page = page
        self.top_area = 0
        self.left_area = 0



    def criar_gesture_detector(self):
        return ft.GestureDetector(
        drag_interval=10,
        top=10,
        left=10,
        mouse_cursor=MouseCursor.MOVE,
        on_pan_update=self.changeposition,
        content=ft.Container(
            border=ft.border.all(5, ft.Colors.RED),
            width=345,
            height=155,
            visible=True
        )
    )
    def changeposition(self,e: DragUpdateEvent):
        # Atualizar a posição do editphoto
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        print('top:',e.control.top,'left:', e.control.left)
        self.top_area = max(0, e.control.top)
        self.left_area = max(0, e.control.left)

        self.page.update()

    def crop_picture(self,imagem:ft.Image,gesture_detector:ft.GestureDetector):
        # A primeira coisa é esconder o componente editphoto durante o corte
        gesture_detector.content.visible = True
        self.page.update()


        # Obter as coordenadas (top, left) e o tamanho (width, height) do editphoto
        top = float(self.top_area)  # Acessando a posição top do GestureDetector
        left = float(self.left_area)  # Acessando a posição left do GestureDetector
        right = left + float(gesture_detector.content.width)  # Largura do Container
        bottom = top + float(gesture_detector.content.height)  # Altura do Container

        # Verificando se as coordenadas estão corretas
        print(f"Coordenadas de corte - Top: {top}, Left: {left}, Right: {right}, Bottom: {bottom}")

        fullscreen = Image.open('foto_capturada.jpg')
        print('tamanho imagem original',fullscreen.size)
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
            cropped_image.save(f'assets/imagem_cortada.jpg')
            print('Imagem cortada com sucesso!')
            self.page.window.maximized=True
            imagem.src='assets/imagem_cortada.jpg'
            imagem.update()

            print(imagem.src)






        else:
            print("Erro: A imagem cortada está inválida ou vazia.")

        self.page.update()