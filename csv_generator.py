import pandas as pd
import cv2



def gen_bars_descriptors(cnt_bars, cnt_legs, name_file):

    # attr
    id = []
    cnt = []
    center = []
    bar_class = []
    fill = []
    nearest_x_label = []
    nearest_y_label = []

    text = []
    type = []

    i=0
    for bar in cnt_bars:
        id.append(i)
        cnt.append(bar['cnt'])
        center.append(bar['center'])
        if(len(cnt_legs)>0):
            bar_class.append(bar['bar_class'])
            fill.append(bar['fill'])
        else:
            bar_class.append('-')
            fill.append('-')
        nearest_x_label.append(bar['nearest_x_label'])
        nearest_y_label.append(bar['nearest_y_label'])
        text.append('-')
        type.append('bar')
        i += 1

    for leg in cnt_legs:
        id.append(i)
        cnt.append(leg['cnt'])
        center.append(leg['center'])
        bar_class.append('-')
        fill.append(leg['fill'])
        nearest_x_label.append('-')
        nearest_y_label.append('-')
        text.append(leg['text'])
        type.append('legend')
        i += 1
    # dictionary of lists
    dict = {'id': id, 'cnt': cnt, 'center': center, 'bar_class': bar_class,
            'fill': fill, 'nearest_x_label': nearest_x_label, 'nearest_y_label': nearest_y_label,
            'text': text, 'type': type}

    df = pd.DataFrame(dict)

    # saving the dataframe
    df.to_csv(name_file+'-bars-features.csv', columns = ['id', 'cnt', 'center', 'bar_class',
            'fill', 'nearest_x_label', 'nearest_y_label', 'text', 'type'] ,header=True, index=False)
