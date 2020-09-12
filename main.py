import os
import cv2
import numpy as np
from preprocess import apply_preprocessing
from bar_detection import bar_detect
from bar_classifier import classify_bars
from bar_coloration import change_bar_color
from bar_localization import estimate_position
from save_result import save_result
import pickle
import pandas as pd


bars_detected = []
leg_detected = []


"""reading dataset - academic or quartz"""
# dataset = 'academic'
dataset = 'quartz'
input_dir = 'input/'+dataset+'/'
col_names = ['image_name', 'qtde_bar', 'qtde_leg']
data = pd.read_csv('input/'+dataset+'_bars.csv', names=col_names)

image_name = data['image_name'][1:]
bars_detected_gd = np.array(data['qtde_bar'][1:], dtype=np.float32)
leg_detected_gd =  np.array(data['qtde_leg'][1:], dtype=np.float32)

i = 1
for file_name, bars, leg in zip(image_name, bars_detected_gd, leg_detected_gd):

    print('_- GDImage: %s bars: %s legend: %s' % (file_name, bars, leg))
    original_image = cv2.imread(input_dir + file_name + '.png')
    csv_dir = input_dir+file_name +'-pred1-texts.csv'

    # legend_bbs= coordenadas do texto da legenda
    # legend_txts = str legenda
    image_posp, legend_bbs, legend_txts, x_labels, y_labels = apply_preprocessing(original_image, csv_dir)
    image_bar, cnt_bars, lst_countaprox = bar_detect(image_posp)

    cnt_legs = []
    if len(legend_bbs) > 0:
        # coordenadas do centro da bb
        cnt_bars, cnt_legs = classify_bars(original_image, cnt_bars, legend_bbs, legend_txts)

    # Bar coloration option

    """
    Colors
    c1 = (127,201,127)
    c2 = (190,174,212)
    c3 = (253,192,134)
    c4 = (255,255,153)
    """
    new_colors = [(127, 201, 127), (190, 174, 212)]
    # new_colors = [(127,201,127), (190,174,212), (253,192,134)]

    # new_color_image = change_bar_color(original_image, cnt_bars, cnt_legs, new_colors)

    cnt_bars = estimate_position(original_image, cnt_bars, x_labels, y_labels)
    print('Image (%d/%d): %s bars: %d legend: %d' % (i, len(image_name),file_name, len(cnt_bars), len(cnt_legs)))
    if not os.path.exists('result/'+dataset):
        os.makedirs('result/'+dataset)
    save_result(original_image, cnt_bars, cnt_legs, 'result/'+dataset+'/'+file_name)

    bars_detected.append(len(cnt_bars))
    leg_detected.append(len(cnt_legs))
    i += 1



# write python dict to a file
print('Getting some statistics...')
erro_list = [abs(x - g) for x,g in zip(bars_detected, bars_detected_gd)]

print('media: %f var: %f' %(np.mean(erro_list), np.std(erro_list)))

