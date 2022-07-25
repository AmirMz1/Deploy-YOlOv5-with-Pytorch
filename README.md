# Deploy-YOlOv5-with-Pytorch
![This is an image](https://drive.google.com/file/d/1ZdnFAS5-SE32qXT7TPOwQBx7uaPJQYAB/view?usp=sharing)

your can run model one image, video and webcam

## Installation
```
pip install pytorch
pip install opencv-python
```

## RUN
> Yolov5 weights (It downloads the weights itself)

> you can run this for deffirnt yolov5 version, change it in detector.py -> def loadModel()
```
# On image
python main.py --img_path data\your name img --thickness 1 --confidens 0.3 
                 in colab use /
# On video
python main.py --vid_path data\your name video --thickness 1 --confidens 0.3

# On webcam 
python main.py --vid_path 0 --thickness 1 --confidens 0.3
```


> Custom YOLOv5 weights
```
# On image
python main.py --img_path data\your name img --thickness 1 --confidens 0.3 -name 'name of your .pt file'
                 in colab use /
# On video
python main.py --vid_path data\your name video --thickness 1 --confidens 0.3 -name 'name of your .pt file'

# On webcam 
python main.py --vid_path 0 --thickness 1 --confidens 0.3 -name 'name of your .pt file'
```

