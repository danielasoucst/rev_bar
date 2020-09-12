import cv2
import pymeanshift as pms
import numpy as np


def apply_mask(img_bgr, img_mask):
    b, g, r = cv2.split(img_bgr)
    b *= img_mask
    g *= img_mask
    r *= img_mask
    return cv2.merge((b, g, r))

def rectangle_detection(thresh):
    # # convert the image to grayscale, blur it, and find edges
    # # in the image
    img_colored = np.copy(thresh)
    # thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    img_gray = np.copy(thresh)
    # # gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # thresh = cv2.Canny(gray, 30, 200)
    # cv2.imshow('canny', thresh)

    contours, h = cv2.findContours(thresh, 1, 2)

    qtde_rect = 0
    lst_cnt = []
    lst_cnt_info = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        if len(approx) == 4:
            # print "square"
            cv2.drawContours(img_colored, [cnt], 0, (0, 0, 255), thickness=1)
            qtde_rect += 1
            lst_cnt.append(cnt)

            a = approx[0, 0]
            b = approx[2, 0]

            cx = a[0] + int(abs(b[0] - a[0]) / 2)
            cy = a[1] + int(abs(b[1] - a[1]) / 2)

            lst_cnt_info.append({'cnt': cnt, 'center': (cx, cy)})
            # cv2.drawContours(cv2.cvtColor(img_gray,cv2.COLOR_GRAY2BGR), [cnt], 0, (255, 255, 255), thickness=1)
            # cv2.imshow('detecyion', cv2.cvtColor(img_gray,cv2.COLOR_GRAY2BGR))

        # else:
        #     cv2.imshow('not recog', img_gray)


    # print('retangulos detectados ', qtde_rect)
    # # cv2.drawContours(img, [cnt], 0, (0, 255, 0), thickness=1)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    return img_colored, qtde_rect, lst_cnt, lst_cnt_info


"""
k : parametro para o kernel utilizado na erosao
"""
def bar_detect(input_image, k = 5):

    temp_image = np.copy(input_image)

    # aplicamos segmentacao
    (segmented_image, labels_image, number_regions) = pms.segment(input_image, spatial_radius=6,
                                                                  range_radius=4.5, min_density=50)

    qtde_rect = 0
    cnt_rects = []
    cnt_rects_info = []
    lst_countaprox = []
    for label in range(1, number_regions):
        filter = np.full(shape=labels_image.shape,fill_value=label,dtype=float)
        result = labels_image - filter
        filtered_img = result == 0

        # A detecao ocorre na imagem colorida
        # filtered_img = apply_mask(temp_image, filtered_img.astype(np.uint8))


        filtered_img = filtered_img.astype(np.uint8)*255

        # Como algumas linhas ou outros residuos podem ter sido reconhecidos como grupos, aplicamos a erosao
        # kernel = np.ones((k, k), np.uint8)
        filtered_img = cv2.erode(filtered_img, (5,5), iterations=1)
        # cv2.imshow('erode', filtered_img)
        # cv2.waitKey()
        # So entao o algoritmo para deteccao de retangulos eh aplicado
        filtered_img, t, lst_cnt, lst_cnt_info = rectangle_detection(filtered_img)
        if t > 0:
            cnt_rects.append(lst_cnt)
            cnt_rects_info += lst_cnt_info

            qtde_rect += t
            # cv2.imshow('rectangle after ', filtered_img)
            # cv2.waitKey()

        for cnt,cnt_info in zip(lst_cnt, lst_cnt_info):

            cv2.drawContours(temp_image, [cnt_info['cnt']], 0, (0, 0, 255), thickness=2)
            cv2.circle(temp_image, cnt_info['center'], 2, (0, 255, 0), 2)

    # print('Total de barras reconhecidas', qtde_rect)
    # cv2.imshow('final ', temp_image)
    # cv2.waitKey()

        # return output_image, qtde_rect
    # return temp_image, cnt_rects, cnt_rects_info, lst_countaprox
    return temp_image, cnt_rects_info, lst_countaprox
