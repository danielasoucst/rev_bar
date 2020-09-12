import sys
import cv2
import pandas as pd

def show_boundingBoxes(image, bb_info_dir):
    col_names = ['id','x','y','width','height','text','type']

    legend_bbs = []
    legend_txts = []
    x_labels = []
    y_labels = []
    # image = cv2.imread(image_dir)
    bb_data = pd.read_csv(bb_info_dir, names=col_names)
    # print(bb_data.values)
    for i in range(1,bb_data.values.shape[0]):
        values = []
        for k in range(1, bb_data.values.shape[1]-2):
            # print(bb_data.values[i])
            values.append(float(bb_data.values[i][k]))

        start_point = (int(values[0]), int(values[1]))
        end_point = (int(values[0]+values[2]),
                     int(values[1]+values[3]))
        # image = cv2.rectangle(image, start_point, end_point, (255,0,0), 2)
        # Preenche os bbs de texto com branco

        cv2.rectangle(image, start_point, end_point, (255, 255, 255), -1)

        if(bb_data.at[i,'type']=='x-axis-label'):
            a = bb_data.at[i, 'x']
            x_labels.append({'x':float(bb_data.at[i,'x']) ,'y': float(bb_data.at[i,'y']),
                             'width':float(bb_data.at[i,'width']),'height':float(bb_data.at[i,'height']),
                             'text': bb_data.at[i,'text']})
        if (bb_data.at[i, 'type'] == 'y-axis-label'):
            y_labels.append({'x': float(bb_data.at[i,'x']), 'y': float(bb_data.at[i,'y']),
                             'width': float(bb_data.at[i,'width']), 'height': float(bb_data.at[i,'height']),
                             'text': bb_data.at[i,'text']})

        # Se existir legenda, pegamos os pontos referentes a bounding box dela...
        if(bb_data.at[i,'type']=='legend-label'):
            legend_bbs.append([start_point,end_point])
            legend_txts.append(bb_data.at[i,'text'])
        # else:
        #     cv2.rectangle(image, start_point, end_point, (255, 255, 255), -1)
    #
    # cv2.imshow('com BB info', image)
    # cv2.waitKey(0)
    return image,legend_bbs,legend_txts,x_labels,y_labels

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print ('Missing arguments...')
    exit(-1)

  image = sys.argv[1] #imagem
  bb_info = sys.argv[2] #bounding boxes .csv
  show_boundingBoxes(image, bb_info)
