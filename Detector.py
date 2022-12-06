from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo

import cv2
import numpy as np


class Detector:
    
    def __init__(self):
        self.cfg = get_cfg()
        
        
        # load model config and pretrained model
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")
        
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        self.cfg.MODEL.DEVICE = "cpu" #cpu or cuda
        
        self.predictor = DefaultPredictor(self.cfg)
        

    def onImage(self, imagePath):
        image = cv2.imread(imagePath)
        #predictions = self.predictor(image)
        
        predictions, segments_info = self.predictor(image)["panoptic_seg"]
        
        viz = Visualizer(image[:,:,::-1], metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
        
        output = viz.draw_panoptic_seg_predictions(predictions.to("cpu"), segments_info)
        
        cv2.imshow("Result", output.get_image()[:,:,::-1])
        cv2.waitKey(0)
        
    def onVideo(self):
        cap = cv2.VideoCapture(0)
        
        (success, image) = cap.read()
        
        while success:
            predictions, segments_info = self.predictor(image)["panoptic_seg"]
            viz = Visualizer(image[:,:,::-1], metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
            output = viz.draw_panoptic_seg_predictions(predictions.to("cpu"), segments_info)
            
            cv2.imshow("Result", output.get_image()[:,:,::-1])
            k = cv2.waitKey(1)
            if k == 27:
                break