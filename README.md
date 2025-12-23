# Multi-Object Tracking and Classification Dashboard

A real-time web-based dashboard for multi-object tracking and classification using YOLOv8 for object detection and SORT (Simple Online and Realtime Tracking) for tracking.

## Features

- 🎯 **Real-time Object Detection** - Powered by YOLOv8
- 🔄 **Multi-Object Tracking** - SORT algorithm for robust tracking
- 📊 **Live Dashboard** - Interactive web interface with real-time statistics
- 📹 **Multiple Input Sources** - Support for images, videos, and webcam
- 🎨 **Visual Tracking** - Colored bounding boxes and trajectory trails
- 📈 **Statistics & Metrics** - Real-time tracking statistics and object counts

## Architecture

### Backend
- **Flask** - Web server and API
- **YOLOv8** - Object detection (Ultralytics)
- **SORT** - Multi-object tracking algorithm
- **OpenCV** - Image and video processing
- **Kalman Filter** - Motion prediction for tracking

### Frontend
- **HTML/CSS/JavaScript** - Interactive dashboard
- **Canvas API** - Real-time webcam processing
- **Responsive Design** - Modern, gradient-based UI

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Webcam (optional, for webcam mode)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/ElliottBolan/Multi-Object-Tracking-and-Classification-Dashboard.git
cd Multi-Object-Tracking-and-Classification-Dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download YOLO model** (optional - will auto-download on first run)
```bash
# The YOLOv8 nano model will be automatically downloaded when you first run the app
# You can also manually download other models:
# yolov8n.pt - Nano (fastest)
# yolov8s.pt - Small
# yolov8m.pt - Medium
# yolov8l.pt - Large (most accurate)
```

## Usage

### Starting the Server

```bash
python app.py
```

The dashboard will be available at: `http://localhost:5000`

### Using the Dashboard

#### 1. Upload Mode
- Click or drag & drop an image/video file
- Supported formats: MP4, AVI, MOV, MKV, JPG, PNG
- Click "Process File" to run detection and tracking
- View results in the output display

#### 2. Webcam Mode
- Click "Webcam" mode button
- Click "Start Webcam" to begin real-time tracking
- The system will process frames at ~10 FPS
- Click "Stop Webcam" to end the session

#### 3. Statistics
- **Active Tracks** - Current number of tracked objects
- **Max Objects** - Maximum objects detected simultaneously
- **Frames Processed** - Total frames analyzed

## API Endpoints

### Health Check
```
GET /api/health
```

### Upload File
```
POST /api/upload
Content-Type: multipart/form-data
Body: file
```

### Process Image
```
POST /api/process-image
Content-Type: application/json
Body: {"filename": "image.jpg"}
```

### Process Video
```
POST /api/process-video
Content-Type: application/json
Body: {"filename": "video.mp4"}
```

### Process Webcam Frame
```
POST /api/process-webcam
Content-Type: application/json
Body: {"image": "base64_encoded_image"}
```

### Reset Tracker
```
POST /api/reset
```

### Get Available Models
```
GET /api/models
```

## How It Works

### Detection Pipeline
1. **Input** - Image, video frame, or webcam capture
2. **Detection** - YOLOv8 detects objects and returns bounding boxes
3. **Tracking** - SORT algorithm assigns unique IDs and tracks objects across frames
4. **Visualization** - Bounding boxes, IDs, and trajectories are drawn
5. **Output** - Annotated frame with statistics

### SORT Tracking Algorithm
- Uses Kalman Filter for motion prediction
- Hungarian algorithm for data association (matching detections to tracks)
- IoU (Intersection over Union) for similarity measurement
- Track management (creation, update, deletion)

### YOLOv8 Detection
- Pre-trained on COCO dataset (80 object classes)
- Real-time inference
- Confidence threshold filtering (default: 0.25)

## Configuration

### Tracking Parameters
Edit in `backend/utils/video_processor.py`:
```python
self.tracker = Sort(
    max_age=30,      # Frames to keep alive without detection
    min_hits=3,      # Minimum detections before track is confirmed
    iou_threshold=0.3 # IoU threshold for matching
)
```

### Detection Parameters
Edit in `app.py`:
```python
video_processor = VideoProcessor(
    model_path='yolov8n.pt',  # Model size
    conf_threshold=0.25        # Confidence threshold
)
```

## Project Structure

```
Multi-Object-Tracking-and-Classification-Dashboard/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── .gitignore                      # Git ignore rules
├── backend/
│   └── utils/
│       ├── detector.py             # YOLOv8 detector
│       ├── sort.py                 # SORT tracking algorithm
│       └── video_processor.py      # Video processing pipeline
├── templates/
│   └── index.html                  # Dashboard UI
├── uploads/                        # Uploaded files (created on first run)
├── outputs/                        # Processed outputs (created on first run)
└── models/                         # YOLO models (auto-downloaded)
```

## Supported Object Classes

The system can detect and track 80 different object classes from the COCO dataset, including:
- People
- Vehicles (car, truck, bus, motorcycle, bicycle)
- Animals (dog, cat, bird, horse, etc.)
- Common objects (chair, bottle, laptop, phone, etc.)
- And many more!

## Performance Tips

1. **For faster processing**: Use `yolov8n.pt` (nano model)
2. **For better accuracy**: Use `yolov8l.pt` (large model)
3. **For webcam**: Reduce FPS in the frontend (adjust interval in `processWebcamFrame`)
4. **For videos**: Process offline and view results after completion

## Troubleshooting

### Model download issues
If the model doesn't auto-download, manually download from:
```
https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

### Webcam not working
- Check browser permissions for camera access
- Ensure no other application is using the webcam
- Try a different browser (Chrome/Firefox recommended)

### Memory issues with large videos
- Process shorter video segments
- Use a smaller YOLO model (yolov8n.pt)
- Reduce video resolution before processing

## Technologies Used

- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **OpenCV 4.8.1** - Computer vision
- **Ultralytics YOLOv8** - Object detection
- **NumPy** - Numerical computing
- **SciPy** - Linear assignment
- **FilterPy** - Kalman filtering

## License

This project is open source and available for educational and research purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Acknowledgments

- YOLOv8 by Ultralytics
- SORT tracking algorithm by Alex Bewley
- COCO dataset for object classes

## Future Enhancements

- [ ] Support for custom trained models
- [ ] Object re-identification
- [ ] Multi-camera support
- [ ] Export tracking data to CSV/JSON
- [ ] Heatmap visualization
- [ ] Speed and trajectory analysis
- [ ] Alert system for specific objects
- [ ] Cloud deployment support