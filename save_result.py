import cv2
import numpy as np
from bar_localization import estimate_position
from csv_generator import gen_bars_descriptors

# gen_bars_descriptors(cnt_bars, cnt_legs,'fig1')
def save_result(original_image, cnt_bars, cnt_legs, name_file):
    result_image = np.copy(original_image)

    # marcando barras detectadas
    for bar in cnt_bars:
        cv2.drawContours(result_image, [bar['cnt']], 0, (0, 0, 255), thickness=2)
        if(len(cnt_legs)>0):
            cv2.putText(
                result_image,  # numpy array on which text is written
                # str(count),  # text
                bar['bar_class'],
                (bar['center'][0] - int(len(bar['bar_class']) * 10 / 2), bar['center'][1]),
                # position at which writing has to start
                cv2.FONT_HERSHEY_SIMPLEX,  # font family
                0.5,  # font size
                (209, 80, 0, 255),  # font color
                1)  # font stroke

    # marcando legendas, caso existam
    for leg in cnt_legs:
        cv2.drawContours(result_image, [leg['cnt']], 0, (255, 0, 0), thickness=2)

    # salvando csv
    gen_bars_descriptors(cnt_bars, cnt_legs, name_file)
    # saving final image
    cv2.imwrite(name_file+'.png', result_image)


    # cv2.imshow('image final', cv2.resize(result_image, (300,300)))
    # cv2.waitKey()
