import cv2
import numpy as np
from show_bb import show_boundingBoxes

def apply_mask(img_bgr, img_mask):
    b, g, r = cv2.split(img_bgr)
    b *= img_mask
    g *= img_mask
    r *= img_mask
    return cv2.merge((b, g, r))


def background_remove(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', gray)
    # Otsu's thresholding
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imshow('thresh', thresh)
    thresh -= 255
    thresh_mask = np.copy(thresh)
    thresh *= 255
    # cv2.waitKey(0)
    return apply_mask(img, thresh_mask)


def apply_preprocessing(original_image,csv_file):


    # 1 passo: preenchemos de branco as areas ref a textos
    temp_image = np.copy(original_image)
    temp_image,legend_bbs, legend_txts, x_labels,y_labels = show_boundingBoxes(temp_image, csv_file)

    # 2 passo: aplicar operacao de fechamento (dilatacao)
    kernel = np.ones((5, 5), np.uint8)
    temp_image = cv2.morphologyEx(temp_image, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow('com dilatacao ',temp_image)
    # cv2.imshow('imagem de entrada ',original_image)
    # cv2.waitKey(0)

    # 3 passo: remover background
    # temp_image = background_remove(temp_image)
    # cv2.imshow('background_remove ',temp_image)
    # cv2.imshow('imagem de entrada ',original_image)
    # cv2.waitKey(0)

    return temp_image, legend_bbs, legend_txts, x_labels,y_labels

