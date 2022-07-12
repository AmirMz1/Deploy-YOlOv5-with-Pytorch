from detector import * 
detector = detector()
classFile = 'coco.names'


import argparse

parser = argparse.ArgumentParser(description="URL")
parser.add_argument("--img_path", help="Path to the folder where the image",
                    type=str)
parser.add_argument("--thickness", help="thickness of linees",
                    type=int)
parser.add_argument("--confidens", help="Scour confidens between 0-1",
                    type=float)
parser.add_argument("--name", help="name of your model",
                    type=str)
parser.add_argument("--vid_path", help="Path to the folder where the image",
                    type=str)

args = parser.parse_args()
nameOFmodel = args.name
numberOFconf = args.confidens
pathOFimage = args.img_path
pathOFvid = args.vid_path



thickness = args.thickness

detector.name_of_models(nameOFmodel)
#-----------------------
detector.readClasses(classFile)
#-----------------------
detector.loadModel()

#-----------------------
# !python mian.py --img "path" --vid "path"
if pathOFimage:
  detector.predict_Image(pathOFimage, thickness, numberOFconf)
elif pathOFvid:
  detector.predict_Video(pathOFvid, thickness, numberOFconf)



