"""
Video Processor for Multi-Object Tracking
"""

import cv2
import numpy as np
from collections import defaultdict
from backend.utils.detector import ObjectDetector
from backend.utils.sort import Sort


class VideoProcessor:
    """
    Process video frames for object detection and tracking
    """

    def __init__(self, model_path='yolov8n.pt', conf_threshold=0.25):
        """
        Initialize the video processor
        
        Args:
            model_path: Path to YOLO model
            conf_threshold: Confidence threshold for detections
        """
        self.detector = ObjectDetector(model_path, conf_threshold)
        self.tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)
        self.track_history = defaultdict(list)
        self.class_counts = defaultdict(int)
        self.colors = self._generate_colors(100)

    def process_frame(self, frame):
        """
        Process a single frame
        
        Args:
            frame: Input frame (numpy array)
            
        Returns:
            annotated_frame: Frame with annotations
            stats: Dictionary with tracking statistics
        """
        # Detect objects
        detections, detected_classes = self.detector.detect(frame)
        
        # Update tracker
        if len(detections) > 0:
            # SORT expects [x1, y1, x2, y2, conf]
            dets_for_sort = detections[:, :5]
            tracked_objects = self.tracker.update(dets_for_sort)
        else:
            tracked_objects = self.tracker.update(np.empty((0, 5)))
        
        # Update class counts
        current_objects = defaultdict(int)
        
        # Annotate frame
        annotated_frame = frame.copy()
        track_data = []
        
        for tracked_obj in tracked_objects:
            x1, y1, x2, y2, track_id = tracked_obj
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            track_id = int(track_id)
            
            # Find corresponding class
            class_name = 'unknown'
            confidence = 0.0
            for i, det in enumerate(detections):
                det_box = det[:4]
                # Check if this detection matches this track (using IoU)
                iou = self._calculate_iou([x1, y1, x2, y2], det_box)
                if iou > 0.3:  # Threshold for matching
                    class_id = int(det[5])
                    class_name = self.detector.get_class_name(class_id)
                    confidence = det[4]
                    break
            
            # Update counts
            current_objects[class_name] += 1
            
            # Draw bounding box
            color = self.colors[track_id % len(self.colors)]
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f'ID:{track_id} {class_name} {confidence:.2f}'
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            y1_label = max(y1, label_size[1] + 10)
            cv2.rectangle(annotated_frame, (x1, y1_label - label_size[1] - 10),
                         (x1 + label_size[0], y1_label), color, -1)
            cv2.putText(annotated_frame, label, (x1, y1_label - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Store track history
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            self.track_history[track_id].append((center_x, center_y))
            
            # Keep only last 30 points
            if len(self.track_history[track_id]) > 30:
                self.track_history[track_id].pop(0)
            
            # Draw track
            points = np.array(self.track_history[track_id], dtype=np.int32).reshape((-1, 1, 2))
            if len(points) > 1:
                cv2.polylines(annotated_frame, [points], False, color, 2)
            
            track_data.append({
                'id': track_id,
                'class': class_name,
                'confidence': float(confidence),
                'bbox': [x1, y1, x2, y2],
                'center': [center_x, center_y]
            })
        
        # Update global class counts
        for class_name, count in current_objects.items():
            if count > self.class_counts[class_name]:
                self.class_counts[class_name] = count
        
        # Prepare statistics
        stats = {
            'total_tracks': len(tracked_objects),
            'current_objects': dict(current_objects),
            'max_objects': dict(self.class_counts),
            'active_trackers': len(self.tracker.trackers),
            'tracks': track_data
        }
        
        return annotated_frame, stats

    def process_video(self, video_path, output_path=None):
        """
        Process entire video file
        
        Args:
            video_path: Path to input video
            output_path: Path to save output video (optional)
            
        Returns:
            stats_history: List of statistics for each frame
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Setup video writer if output path provided
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        stats_history = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            annotated_frame, stats = self.process_frame(frame)
            stats['frame_number'] = frame_count
            stats['total_frames'] = total_frames
            stats_history.append(stats)
            
            # Write frame
            if writer:
                writer.write(annotated_frame)
            
            frame_count += 1
        
        # Cleanup
        cap.release()
        if writer:
            writer.release()
        
        return stats_history

    def reset(self):
        """
        Reset tracker state
        """
        self.tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)
        self.track_history.clear()
        self.class_counts.clear()

    @staticmethod
    def _generate_colors(num_colors):
        """
        Generate distinct colors for visualization
        """
        np.random.seed(42)
        colors = []
        for i in range(num_colors):
            hue = i / num_colors
            # Convert HSV to RGB
            rgb = cv2.cvtColor(np.uint8([[[hue * 180, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
            colors.append((int(rgb[0]), int(rgb[1]), int(rgb[2])))
        return colors

    @staticmethod
    def _calculate_iou(box1, box2):
        """
        Calculate IoU between two boxes
        """
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2
        
        # Calculate intersection area
        x1_i = max(x1_1, x1_2)
        y1_i = max(y1_1, y1_2)
        x2_i = min(x2_1, x2_2)
        y2_i = min(y2_1, y2_2)
        
        if x2_i < x1_i or y2_i < y1_i:
            return 0.0
        
        intersection = (x2_i - x1_i) * (y2_i - y1_i)
        
        # Calculate union area
        area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0
