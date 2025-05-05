import os

import easyocr
import cv2
import numpy as np
from PIL import Image, ImageEnhance


def remove_noise_and_enhance(image_array):
    # 1. Verifica se já está em escala de cinza; se for colorida, converte
    if len(image_array.shape) == 3:
        img = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    else:
        img = image_array.copy()
    img = cv2.resize(img, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img_filtered = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    img_thresh = cv2.adaptiveThreshold(
        img_filtered, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        25, 10
    )

    inverted = cv2.bitwise_not(img_thresh)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(inverted, connectivity=8)
    sizes = stats[1:, -1]

    # Reduz o limite para evitar apagar caracteres
    min_size = int((img.shape[0] * img.shape[1])*0.00001)
    cleaned_mask = np.zeros_like(inverted)
    for i in range(1, num_labels):
        if sizes[i - 1] >= min_size:
            cleaned_mask[labels == i] = 255

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    reinforced = cv2.dilate(cleaned_mask, kernel, iterations=1)


    pil_image = Image.fromarray(reinforced)
    enhanced_image = ImageEnhance.Contrast(pil_image).enhance(1.5)



    final_image= np.array(enhanced_image)

    return final_image


def corrigir_confusoes_contextual(texto: str, probabilidade: float) -> str:
    """
    Corrige B ↔ 8 quando o 8 está na penúltima posição antes de um número.
    Aplica a correção apenas se a confiança for baixa.
    """
    corrigido = texto
    if probabilidade < 0.8:  # Ajuste esse limite conforme necessário
        # Verifica se o '8' está na penúltima posição e é seguido por um número
        if len(texto) > 2 and texto[-2] == '8' and texto[-1].isdigit():
            corrigido = texto[:-2] + 'B' + texto[-1]  # Substitui o penúltimo '8' por 'B'
    return corrigido








