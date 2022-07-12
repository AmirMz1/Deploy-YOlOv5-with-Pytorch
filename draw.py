import colorsys
import random
from PIL import Image    
import cv2
import numpy as np

def draw_bbox(image, model,names, confidens, thickness, show_label=True, fill=True):
    num_classes = len(names)
    image_h, image_w, _ = image.shape
    # some custom color and one generator color
    # colors = [(71, 64, 66),(112, 100, 104),(138, 124, 129),(101, 114, 109),(64, 71, 69)] 
    # ------
    # colors = [(98, 32, 55),(140, 46, 79),(183, 61, 103),(225, 75, 126),(13, 4, 7)] 
    # ------
    # hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)] 
    # print(hsv_tuples)

    # colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    # colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    #random.seed(0)
    #random.shuffle(colors)
    #random.seed(None)
    # -----
    colors = []
    for i in range(80):
        color = [(207, 184, 199),(237, 229, 235),(255, 255, 255),(231, 238, 233),(184, 207, 191)]
        for ii in color:
            colors.append(ii)

    labels, cord = model.xyxyn[0][:, -1], model.xyxyn[0][:, :-1]
    num = len(labels)
    for i in range(num):    
        coor = cord[i]  # [x_min, y_min, x_max, y_max , confidens]
        if coor[4] >= confidens:
            coor[1] = int(coor[1] * image_h)
            coor[3] = int(coor[3] * image_h)
            coor[0] = int(coor[0] * image_w)
            coor[2] = int(coor[2] * image_w)

        fontScale = 0.5
        # score = out_scores[0][i]
        class_ind = int(labels[i])
        bbox_color = colors[class_ind]
        bbox_thick = int(0.6 * (image_h + image_w) / 600)

        c1, c2 = (int(coor[0]), int(coor[1])), (int(coor[2]), int(coor[3]))
        cv2.rectangle(image, c1, c2, bbox_color, thickness)

        if show_label:
          overlay = image.copy()
          bbox_mess = '%s' % (names[class_ind])
          t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=bbox_thick // 2)[0]
          c3 = (int((c1[0] + t_size[0] * 2) - 5) , c1[1] - t_size[1] - 9)
          cv2.rectangle(overlay, (int(c1[0]), int(c1[1])), (int(c3[0]), int(c3[1])), bbox_color, -1) #filled
          alpha = 0.8
          image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

          cv2.putText(image, bbox_mess, (int(c1[0] + 5), int(c1[1] - 7)), cv2.FONT_HERSHEY_SIMPLEX,
                      fontScale, (26, 26, 26), bbox_thick // 2, lineType=cv2.LINE_AA)
        if fill:
            overlay2 = image.copy()
            cv2.rectangle(overlay2, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])), bbox_color, -1)
            alpha2 = 0.2
            image = cv2.addWeighted(overlay2, alpha2, image, 1 - alpha2, 0)

    return image