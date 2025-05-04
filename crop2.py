import cv2
import flet as ft
from flet.core.gesture_detector import GestureDetector, DragUpdateEvent
from flet.core.types import MouseCursor
from PIL import Image
import time
import os
import io
import base64
from ocr import ocr
import numpy as np


class Crop:
    def __init__(self, page: ft.Page):
        self.page = page
        self.top_area = 0
        self.left_area = 0
        self.largura_area_corte:float=100
        self.altura_area_corte: float = 100
        self.imagem_width=640
        self.imagem_height=480
        self.left=0
        self.right=0
        self.bottom=0
        self.top=0

    def resetar_crop(self,slider_largura:ft.Slider,slider_altura:ft.Slider,gesture_detector:ft.GestureDetector):
        self.left_area = 10
        self.top_area = 10
        self.largura_area_corte = 100
        self.altura_area_corte = 100

        gesture_detector.left = self.left_area
        gesture_detector.top = self.top_area
        gesture_detector.content.width = self.largura_area_corte
        gesture_detector.content.height = self.altura_area_corte
        gesture_detector.update()

        slider_largura.max = self.imagem_width - self.left_area
        slider_largura.value = self.largura_area_corte
        slider_largura.update()

        slider_altura.max = self.imagem_height - self.top_area
        slider_altura.value = self.altura_area_corte
        slider_altura.update()

        self.page.update()

    def habilitar_crop(self,gesture:ft.GestureDetector):
        gesture.disabled=False,
        gesture.content.visible=True
        self.page.update()

    def desabilitar_crop(self,gesture:ft.GestureDetector):
        gesture.disabled=True
        gesture.content.visible=False
        self.page.update()

    def esperar_foto_ser_salva(self,path,timeout=2):
        start=time.time()
        while not os.path.exists(path):
            print('nao existe',path)
            if (time.time() - start) >timeout:
                raise TimeoutError(f'o caminho {path} não foi salvo a tempo')
            time.sleep(0.05)
        print('existe',path)

    def criar_gesture_detector(self):
        return ft.GestureDetector(
        drag_interval=10,
        top=10,
        left=10,
        disabled=True,
        mouse_cursor=MouseCursor.MOVE,
        on_pan_update=self.changeposition,
        content=ft.Container(
            border=ft.border.all(5, ft.Colors.RED),
            width=self.largura_area_corte,
            height=self.altura_area_corte,
            visible=False

        )
    )


    def changeposition(self, e: DragUpdateEvent):
        # Tamanho da imagem base (o limite)
        self.imagem_width = 640
        self.imagem_height = 480

        # Tamanho do container de corte
        box_width = e.control.content.width
        box_height = e.control.content.height

        margem_esquerda = 10

        # Novo top e left calculados com delta
        new_top = e.control.top + e.delta_y
        new_left = e.control.left + e.delta_x

        # Limitar para não sair da área da imagem
        e.control.top = max(0, min(new_top, self.imagem_height - box_height))
        e.control.left = max(margem_esquerda, min(new_left, self.imagem_width + margem_esquerda - box_width))

        # Atualizar variáveis
        self.top_area = e.control.top
        self.left_area = e.control.left

        self.page.update()

    def crop_picture(self, imagem: ft.Image, gesture_detector: ft.GestureDetector,slider_largura,slider_altura):
        try:
            # Esconder temporariamente o componente de crop
            gesture_detector.content.visible = True
            self.page.update()

            # Aguarda a imagem original ser salva
            self.esperar_foto_ser_salva('foto_capturada.jpg', 2)

            # Abrir imagem original (com tamanho real)
            fullscreen = Image.open('foto_capturada.jpg')
            img_width_real, img_height_real = fullscreen.size

            # Tamanho da imagem exibida no app
            self.imagem_width = 640
            self.imagem_height = 480

            # Fatores de escala entre imagem exibida e imagem real
            fator_x = img_width_real / self.imagem_width
            fator_y = img_height_real / self.imagem_height

            # Margem lateral que desloca a imagem no layout
            margem_esquerda = 10

            # Coordenadas do container de crop no layout Flet
            self.left = (self.left_area - margem_esquerda) * fator_x
            self.top = self.top_area * fator_y
            self.right = self.left + self.largura_area_corte * fator_x
            self.bottom = self.top + self.altura_area_corte * fator_y
            print('largura area de corte:',self.largura_area_corte)
            # Arredonda e limita dentro da imagem real
            left = int(round(max(0, min(self.left, img_width_real))))
            right = int(round(max(0, min(self.right, img_width_real))))
            top = int(round(max(0, min(self.top, img_height_real))))
            bottom = int(round(max(0, min(self.bottom, img_height_real))))

            # Área de crop final
            area = (left, top, right, bottom)

            # Faz o crop
            cropped_image = fullscreen.crop(area)

            # Verifica se a imagem é válida
            if cropped_image.width > 0 and cropped_image.height > 0:
                buffered = io.BytesIO()
                cropped_image.save(buffered, format="JPEG")
                img_bytes = buffered.getvalue()
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                imagem.src_base64 = img_base64
                imagem.update()
                self.page.update()
                image_data = base64.b64decode(img_base64)
                image_pil = Image.open(io.BytesIO(image_data)).convert('RGB')
                image_np = np.array(image_pil)

                # Agora chamar a função
                ocr(image_np)
                #resetar crop
                self.resetar_crop(slider_largura, slider_altura, gesture_detector)


            else:
                print("Erro: Imagem cortada está vazia ou inválida.")

        except Exception as e:
            print(f"Erro ao realizar o crop: {e}")











