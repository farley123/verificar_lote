
import easyocr
import cv2
import numpy as np
import processar_imagem
from PIL import Image
import resultado_observable
from resultado_observable import ResultadoObservable

resultado_ocr:ResultadoObservable=resultado_observable.ResultadoObservable('')

def ocr(image_np_array):
    texto_corrigido=[]
    # Criar um leitor OCR para os idiomas desejados
    imagem=processar_imagem.remove_noise_and_enhance(image_np_array)
    image_pill=Image.fromarray(imagem)
    image_pill.save('image_tratada.png')
    reader = easyocr.Reader(['en', 'pt'], gpu=True)

    # Executar o OCR diretamente no array da imagem
    result = reader.readtext(
        imagem,
        allowlist='0123456789ABF:L ',
        low_text=0.5
    )


    # Exibir o texto extraído
    print("Texto detectado:")
    for (bbox, text, prob) in result:
        texto_corrigido.append(processar_imagem.corrigir_confusoes_contextual(text, prob))
        print(f"Original: {text} | Corrigido: {texto_corrigido} | Confiança: {prob:.2f}")
    resultado_ocr.set(formatar_resultado(texto_corrigido))

def formatar_resultado(resultado):
    if len(resultado)<7:
        print(len(resultado))
        return f'Não foi possivel fazer a leitura da imagem corretamente considere por favor fazer a leitura manualmente'
    if len(resultado)==8:
        resultado[6]=f'{resultado[6]} {resultado[7]}'
        del resultado[7]
    return f'{resultado[0]} {resultado[1]} {resultado[2]}\n{resultado[3]}\n{resultado[4]} {resultado[5]} {resultado[6]}'