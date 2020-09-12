import cv2
import numpy as np
import math
import statistics

def get_center_bar(image, cnt_rects):

    image_copy = np.copy(image)
    lst_bgr = []
    lst_cent_rec = []
    for cnt in cnt_rects:
        # cv2.drawContours(image, cnt, 0, (0, 0, 255), thickness=1)
        cnt = cnt[0]
        a = cnt[0, 0]
        b = cnt[2, 0]

        cx = a[0] + int(abs(b[0] - a[0]) / 2)
        cy = a[1] + int(abs(b[1] - a[1]) / 2)

        lst_cent_rec.append([cx, cy])

        cv2.circle(image_copy, (cx, cy), 2, (0, 255, 0), 2)
        cv2.drawContours(image_copy, [cnt], 0, (0, 0, 255), thickness=1)
        lst_bgr.append(image[cy, cx,:])

        cv2.imshow('imagem original ', image_copy)
        cv2.waitKey()
    return lst_bgr, lst_cent_rec

"""
legend_bbs: cont das bbs referentes as legendas de texto
lst_cent_rec:coord de todas as bbs dos retangulos detectados na etapa anterior
retorna uma lista com as coord das bbs color legend e outra lista atualizada com  os centros das barras
"""
def classify_cnt(image, cnt_rects, legend_bbs):

    cnt_bars = list(cnt_rects)
    cnt_legs = []


    for cnt_leg in legend_bbs:
        cx = int(cnt_leg[0][0] + (cnt_leg[1][0] - cnt_leg[0][0]) / 2)
        cy = int(cnt_leg[0][1] + (cnt_leg[1][1] - cnt_leg[0][1]) / 2)

        dist_min = None
        leg_coord = None  # guardamos o centro dos retangulos referentes as legendas
        indice = -1
        # larg = abs(cnt_leg[0][1] - cnt_leg[1][1])
        larg = abs(cnt_leg[0][0] - cnt_leg[1][0])
        for i in range(len(cnt_rects)):
            element = cnt_rects[i]
            cent_rec = element['center']
            a = cent_rec[0]
            b = cent_rec[1]


            distance = math.sqrt((a - cx) ** 2 + (b - cy) ** 2)
            if ((dist_min is None or distance < dist_min) and distance < larg):
                dist_min = distance
                leg_coord = cent_rec
                indice = i


        # cnt_bars.remove(cnt_rects[indice])
        if(indice > -1):
            leg = cnt_rects.pop(indice)
            color_leg = image[leg_coord[1], leg_coord[0], :]
            cnt_legs.append({'cnt':leg['cnt'],
                             'center': leg['center'],
                             'fill': (int(color_leg[0]), int(color_leg[1]), int(color_leg[2]))})

    return  cnt_rects, cnt_legs

def remove_false_bars(image, cnt_bars):
    cnt_true_bars = []

    max_larg = 0
    width_lst = []
    thresh = 10.
    for cnt in cnt_bars:
        rect = cv2.minAreaRect(cnt['cnt'])
        if(abs(rect[2]) < 45):
            width_lst.append(rect[1][0])
        else:
            if(abs(rect[2]) <= 90 ):
                width_lst.append(rect[1][1])
            else:
                return None,None
        # cv2.minAreaRect returns -> center (x,y), (width, height), angle of rotation

    # in this case, we assume that false bars are thin when it compared to the true bars
    if(len(width_lst)>0):

        max_width = max(width_lst)
    # for i in range(len(cnt_bars)):
    for cnt, width in zip(cnt_bars,width_lst):
        # cnt = cnt_bars[i]
        rect = cv2.minAreaRect(cnt['cnt'])
        # width = rect[1][1]

        if(abs(width-max_width)<thresh):
            cnt_true_bars.append(cnt)
            # cv2.circle(image, (a[0],a[1]), 2, (0,255,0), 2)
            cv2.drawContours(image, [cnt['cnt']], 0, (0, 0, 255), thickness=2)
            # cv2.imshow('remove false bars', image)
            # cv2.waitKey()
    return cnt_true_bars, image

""""
cnt_rects = list de dic {'cnt', 'center'}contornos dos retangulos detectados
legend_bbs = bb referentes as legendas
"""
def classify_bars(original_image, cnt_rects, legend_bbs, legend_txts):
    image = np.copy(original_image)
    lst_info_bar = []
    lst_info_leg = []


    # 1st find bar center
    # _, lst_cent_rec = get_center_bar(image, cnt_rects)

    # 1st  prediz quais sao os contornos referentes a legendas e quais nao sao
    cnt_bars, cnt_legs = classify_cnt(image, cnt_rects, legend_bbs)

    for cnt_leg, t_leg in zip(cnt_legs, legend_txts):
        cnt_leg['text'] = t_leg

    # 2rd eliminar falsas barras...
    cnt_bars, image = remove_false_bars(image, cnt_bars)
    # cv2.imshow('classify ', image)
    # cv2.waitKey()

    # 3rd classifica as barras conforme a sua cor
    for cnt_bar in cnt_bars:
        bar_color = image[cnt_bar['center'][1], cnt_bar['center'][0], :]
        cnt_bar['bar_class'] = '-'
        cnt_bar['fill'] = '-'
        for cnt_leg, t_leg in zip(cnt_legs, legend_txts):
            color_leg = cnt_leg['fill']
            if (bar_color[0] == color_leg[0] and bar_color[1] == color_leg[1] and bar_color[2] == color_leg[2]):
                cnt_bar['bar_class'] =  t_leg
                cnt_bar['fill'] = bar_color

                cv2.putText(
                    image,  # numpy array on which text is written
                    # str(count),  # text
                    t_leg,
                    (cnt_bar['center'][0] - int(len(t_leg) * 10 / 2), cnt_bar['center'][1]),
                    # position at which writing has to start
                    cv2.FONT_HERSHEY_SIMPLEX,  # font family
                    0.5,  # font size
                    (209, 80, 0, 255),  # font color
                    1)  # font stroke

                # cv2.imshow('com labels ', image)
                # cv2.waitKey()
                break
    return cnt_bars, cnt_legs

