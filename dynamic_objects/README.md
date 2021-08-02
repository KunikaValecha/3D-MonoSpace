## Requirements
- PyTorch
- Cuda
- OpenCV >= 3.4.3

## Usage
In order to download the weights:
```
cd weights/
./get_weights.sh
```
This will download pre-trained weights for the 3D BoundingBox net and also YOLOv3 weights from the
official yolo [source](https://pjreddie.com/darknet/yolo/).

>If script is not working: [pre trained weights](https://drive.google.com/open?id=1yEiquJg9inIFgR3F-N5Z3DbFnXJ0aXmA) and 
[YOLO weights](https://pjreddie.com/media/files/yolov3.weights)

To see all the options:
```
python Run.py --help

