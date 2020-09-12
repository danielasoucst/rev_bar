import cv2
import numpy as np

def change_bar_color(original_image, cnt_bars, cnt_legs, new_colors):
    temp_image = np.copy(original_image)

    if(len(cnt_legs) == len(new_colors)):
        for e_leg, n_color in zip(cnt_legs, new_colors):
            e_leg['fill'] = n_color
            cv2.drawContours(temp_image, [e_leg['cnt']], 0, n_color, thickness=-1)

            for e_bar in cnt_bars:
                if e_bar['bar_class'] == e_leg['text']:
                    e_bar['fill'] = n_color
                    cv2.drawContours(temp_image, [e_bar['cnt']], 0,n_color, thickness=-1)


        # cv2.imshow('com nova coloracao', temp_image)
        # cv2.waitKey(0)
    return temp_image
