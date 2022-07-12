import os
import sys
import cv2, time, torch
import numpy as np
import colorsys
import random
from PIL import Image
from draw import draw_bbox

class detector:
    def __init__(slef):
        pass
    def readClasses(self, classesFilePath):
        with open(classesFilePath, 'r') as f:
            self.classesList = f.read().splitlines()          
            print("Read classes is Done!")

    def name_of_models(self, pathOF):
        self.modelName = pathOF # name of folder
        self.cacheDir = './per-trained-models/'
        print(f"\nPath of Your Model --> {self.cacheDir}{self.modelName}")


    def loadModel(self):
        print("loading Model ")
        if self.modelName:
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=f"{self.cacheDir}{self.modelName}" , force_reload=True)
        else:
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

        print("Model, loaded successfully..!")


    def createBondingBoxes(self, image, thickness, confidens):
        img_draw = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
        img1,img2,_ = img_draw.shape
        shape = (img1,img2)

        if shape > (1080,1900):
          img_draw = cv2.resize(img_draw, (0,0), fx=0.5, fy=0.5) 
          print("Image Resize it!: ",img_draw.shape)
        if shape < (1080,1900) and shape > (800,1400):
          img_draw = cv2.resize(img_draw, (0,0), fx=0.7, fy=0.7) 
          print("Image Resize it!: ",img_draw.shape)


        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB) 
        names = self.model.names
        results = self.model(image)     
        # image = plot_boxes(results, image.copy())
        image = draw_bbox(img_draw, results,names, confidens, thickness)

        return image


    def predict_Image(self, imagePath, thickness, confidens):
        image = cv2.imread(imagePath)     
        bboxImage = self.createBondingBoxes(image, thickness, confidens)
        
        image = Image.fromarray(bboxImage.astype(np.uint8))
        image.show()

        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        cv2.imwrite('yolov5.jpg', image)

        print("\nResult Path: yolov5.jpg")
        # cv2.imshow("Result", bboxImage)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    
    def predict_Video(self, videoPath, thickness, confidens):
        cap = cv2.VideoCapture(videoPath)
        if (cap.isOpened == False):
            print("Error cap not readed!")
#*-*
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*'XVID')
        result = cv2.VideoWriter('video.avi', codec, fps,(frame_width, frame_height))
#*-*
        
        (value, frame) = cap.read()
        StartTime = 0
        while value:
            currentTime = time.time()
            fps = (1/currentTime - StartTime)
            StartTime = currentTime

            bboxImage = self.createBondingBoxes(frame,thickness,confidens)
            cv2.putText(bboxImage, "FPS: " + str(int(fps)), (15,20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            img = cv2.cvtColor(bboxImage, cv2.COLOR_BGR2RGB)
            result.write(img)
            # cv2.imshow("Result",img)
            # key = cv2.waitKey(1) & 0xFF 
            # if key == ord("q"):
            #     break
            (value, frame) = cap.read()

            if value == False:
                print("break")
                break
        cv2.destroyAllWindows()



        
