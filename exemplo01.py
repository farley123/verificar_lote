import easyocr



import cv2

import numpy as np

from PIL import Image, ImageEnhance






################################

# Criar um leitor OCR para os idiomas desejados (aqui estamos usando 'en' para inglês e 'pt' para português)
reader = easyocr.Reader(['en', 'pt'],gpu=True)

# Caminho para a imagem que você deseja processar
image_path = 'assets/imagem03.png'  # Substitua pelo caminho da sua imagem

# Realizar o OCR na imagem
result = reader.readtext(image_path,allowlist ='0123456789ABF:L ', low_text=0.5)

# Exibir o texto extraído
print("Texto detectado:")
for (bbox, text, prob) in result:
    print(f"{text}",end=' ')