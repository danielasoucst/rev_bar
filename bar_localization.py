import cv2
import numpy as np

def get_extremes_bars(cnt_bars):

    min = {'index': 0, 'value': cnt_bars[0]['center'][0]}
    max = {'index': 0, 'value': cnt_bars[0]['center'][0]}
    for i in range(1,len(cnt_bars)):
        if(cnt_bars[i]['center'][0] < min['value']):
            min = {'index': i, 'value': cnt_bars[i]['center'][0]}
        if(cnt_bars[i]['center'][0]> max['value']):
            max = {'index': i, 'value': cnt_bars[i]['center'][0]}

    return cnt_bars[min['index']], cnt_bars[max['index']]

def estimate_position(original_image, cnt_bars, x_labels,y_labels):
    image_copy = np.copy(original_image)

    # left_bar, right_bar = get_extremes_bars(cnt_bars)
    for bar in cnt_bars:

        dist_lst = []
        dist_lst_y = []

        bar['nearest_x_label'] = '-'
        bar['nearest_y_label'] = '-'
        cv2.circle(image_copy, bar['center'], 2, (0, 255, 255), 2)
        # b = bar['cnt'][0, 0, 1]
        cv2.circle(image_copy, (bar['cnt'][0, 0, 0],bar['cnt'][0, 0, 1]) , 2, (0, 255, 0), 2)

        for label in x_labels:
            dist = abs((label['x'] + label['width']/2) - bar['center'][0])
            dist_lst.append(dist)
            # cv2.circle(image_copy, (int(label['x'] + label['width']/2), int(label['y'] + label['height']/2)), 2, (0, 255, 0), 2)


        for label in y_labels:
            dist = abs((label['y'] + label['height']/2) - bar['cnt'][0, 0, 1])
            dist_lst_y.append(dist)
            # cv2.circle(image_copy, (int(label['x'] + label['width']/2), int(label['y'] + label['height']/2)), 2, (0, 255, 0), 2)

        # find label in axis X nearest
        if(len(dist_lst)>0):
            index1 = dist_lst.index(min(dist_lst))
            label_near = x_labels[index1]
            bar['nearest_x_label'] = label_near['text']

        # find label in axis Y nearest
        if (len(dist_lst_y) > 0):
            index1 = dist_lst_y.index(min(dist_lst_y))
            label_near = y_labels[index1]
            bar['nearest_y_label'] = label_near['text']

        # cv2.imshow('center labels', image_copy)
        # cv2.waitKey()

    return cnt_bars

