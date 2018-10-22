import pyyolo
import numpy as np
import sys
import cv2


darknet_path = '/home/ubuntu/pyyolo/darknet'

"""
datacfg = '/home/ubuntu/madYolo/coco.data'
cfgfile = '/home/ubuntu/madYolo/darknet/cfg/yolov3-tiny.cfg'
weightfile = '/home/ubuntu/madYolo/darknet/yolov3-tiny.weights'


datacfg = '/home/ubuntu/trained_file/obj.data'
cfgfile = '/home/ubuntu/trained_file/yolov3-tiny-training.cfg'
weightfile = '/home/ubuntu/trained_file/yolov3-tiny-training_30000.weights'

"""

datacfg = '/home/ubuntu/trained_file/obj.data'
cfgfile = '/home/ubuntu/trained_file/yolov3-tiny-training.cfg'
weightfile = '/home/ubuntu/trained_file/yolov3-tiny-training_10000.weights'
#"""

filename = darknet_path + '/data/dog.jpg'
thresh = 0.45
hier_thresh = 0.5

pyyolo.init(darknet_path, datacfg, cfgfile, weightfile)

def detect_image(filepath):
    img = cv2.imread(filepath)
    img = img.transpose(2,0,1)
    c, h, w = img.shape[0], img.shape[1], img.shape[2]

    data = img.ravel()/255.0
    data = np.ascontiguousarray(data, dtype=np.float32)
    return pyyolo.detect(w, h, c, data, thresh, hier_thresh)
