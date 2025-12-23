"""
Flask Backend API for Multi-Object Tracking Dashboard
"""

import os
import cv2
import base64
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from backend.utils.video_processor import VideoProcessor

app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max file size

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize video processor
video_processor = VideoProcessor()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main dashboard page"""
    return send_from_directory(app.template_folder, 'index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Multi-Object Tracking API is running'})


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload video or image file for processing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'filepath': filepath
        })
    
    return jsonify({'error': 'File type not allowed'}), 400


@app.route('/api/process-image', methods=['POST'])
def process_image():
    """Process a single image"""
    data = request.get_json()
    
    if not data or 'filename' not in data:
        return jsonify({'error': 'No filename provided'}), 400
    
    filename = data['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Read image
        image = cv2.imread(filepath)
        if image is None:
            return jsonify({'error': 'Failed to read image'}), 400
        
        # Process image
        video_processor.reset()
        annotated_image, stats = video_processor.process_frame(image)
        
        # Save output image
        output_filename = f'output_{filename}'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        cv2.imwrite(output_path, annotated_image)
        
        # Convert to base64 for frontend display
        _, buffer = cv2.imencode('.jpg', annotated_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'message': 'Image processed successfully',
            'output_filename': output_filename,
            'image_data': f'data:image/jpeg;base64,{image_base64}',
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process-video', methods=['POST'])
def process_video():
    """Process a video file"""
    data = request.get_json()
    
    if not data or 'filename' not in data:
        return jsonify({'error': 'No filename provided'}), 400
    
    filename = data['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Process video
        output_filename = f'output_{filename}'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        video_processor.reset()
        stats_history = video_processor.process_video(filepath, output_path)
        
        # Calculate summary statistics
        total_frames = len(stats_history)
        max_simultaneous_objects = max([s['total_tracks'] for s in stats_history]) if stats_history else 0
        
        # Get final class counts
        final_stats = stats_history[-1] if stats_history else {}
        
        return jsonify({
            'message': 'Video processed successfully',
            'output_filename': output_filename,
            'total_frames': total_frames,
            'max_simultaneous_objects': max_simultaneous_objects,
            'final_stats': final_stats,
            'stats_summary': {
                'total_frames_processed': total_frames,
                'max_objects_detected': max_simultaneous_objects
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process-webcam', methods=['POST'])
def process_webcam():
    """Process a frame from webcam"""
    data = request.get_json()
    
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400
    
    try:
        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Failed to decode image'}), 400
        
        # Process frame
        annotated_frame, stats = video_processor.process_frame(frame)
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'image_data': f'data:image/jpeg;base64,{image_base64}',
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_tracker():
    """Reset the tracker state"""
    try:
        video_processor.reset()
        return jsonify({'message': 'Tracker reset successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/outputs/<filename>')
def serve_output(filename):
    """Serve processed output files"""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available YOLO models"""
    return jsonify({
        'models': [
            {'name': 'YOLOv8 Nano', 'value': 'yolov8n.pt', 'description': 'Fastest, least accurate'},
            {'name': 'YOLOv8 Small', 'value': 'yolov8s.pt', 'description': 'Balanced speed and accuracy'},
            {'name': 'YOLOv8 Medium', 'value': 'yolov8m.pt', 'description': 'More accurate, slower'},
            {'name': 'YOLOv8 Large', 'value': 'yolov8l.pt', 'description': 'Most accurate, slowest'}
        ]
    })


if __name__ == '__main__':
    print("Starting Multi-Object Tracking Dashboard...")
    print("Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
