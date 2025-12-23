"""
Object Detector using YOLO
"""

import cv2
import numpy as np
from ultralytics import YOLO


class ObjectDetector:
    """
    Object detector using YOLOv8
    """

    def __init__(self, model_path='yolov8n.pt', conf_threshold=0.25):
        """
        Initialize the object detector
        
        Args:
            model_path: Path to YOLO model weights
            conf_threshold: Confidence threshold for detections
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.class_names = self.model.names

    def detect(self, image):
        """
        Detect objects in an image
        
        Args:
            image: Input image (numpy array)
            
        Returns:
            detections: numpy array of shape (N, 6) where each row is [x1, y1, x2, y2, conf, class_id]
            class_names: List of detected class names
        """
        results = self.model(image, conf=self.conf_threshold, verbose=False)
        
        detections = []
        detected_classes = []
        
        if len(results) > 0:
            result = results[0]
            if result.boxes is not None and len(result.boxes) > 0:
                boxes = result.boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
                confidences = result.boxes.conf.cpu().numpy()
                class_ids = result.boxes.cls.cpu().numpy()
                
                for box, conf, cls_id in zip(boxes, confidences, class_ids):
                    detections.append([
                        float(box[0]), float(box[1]), 
                        float(box[2]), float(box[3]), 
                        float(conf), int(cls_id)
                    ])
                    detected_classes.append(self.class_names[int(cls_id)])
        
        return np.array(detections) if detections else np.empty((0, 6)), detected_classes

    def get_class_name(self, class_id):
        """
        Get class name from class ID
        
        Args:
            class_id: Class ID
            
        Returns:
            Class name string
        """
        return self.class_names.get(class_id, 'unknown')
