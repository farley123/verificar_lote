
import easyocr
import cv2
import numpy as np
import processar_imagem
from PIL import Image

def ocr(image_np_array):
    # Criar um leitor OCR para os idiomas desejados
    imagem=processar_imagem.remove_noise_and_enhance(image_np_array)
    image_pill=Image.fromarray(imagem)
    image_pill.save('image_tratada.png')
    reader = easyocr.Reader(['en', 'pt'], gpu=True)

    # Executar o OCR diretamente no array da imagem
    result = reader.readtext(
        imagem,
        allowlist='0123456789ABF:L',
        low_text=0.5
    )


    # Exibir o texto extraído
    print("Texto detectado:")
    for (bbox, text, prob) in result:
        texto_corrigido = processar_imagem.corrigir_confusoes_contextual(text, prob)
        print(f"Original: {text} | Corrigido: {texto_corrigido} | Confiança: {prob:.2f}")
