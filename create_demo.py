"""
Demo script to show the dashboard structure
Creates a simple test HTML page to demonstrate the UI
"""

import os


def create_demo_page():
    """Create a standalone demo HTML page"""
    
    demo_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Object Tracking Dashboard - Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .content {
            padding: 30px;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .feature-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        .feature-title {
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 10px;
        }
        .demo-image {
            background: #f0f0f0;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
            border: 2px dashed #667eea;
        }
        .tech-stack {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .tech-badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Multi-Object Tracking & Classification Dashboard</h1>
            <p style="font-size: 1.2em; margin-top: 10px;">
                Real-time object detection, tracking, and classification
            </p>
        </header>
        
        <div class="content">
            <h2 style="color: #667eea; margin-bottom: 20px;">Key Features</h2>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <div class="feature-title">Object Detection</div>
                    <p>Powered by YOLOv8 for accurate and fast object detection across 80+ classes</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔄</div>
                    <div class="feature-title">Multi-Object Tracking</div>
                    <p>SORT algorithm with Kalman filtering for robust object tracking across frames</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Live Dashboard</div>
                    <p>Interactive web interface with real-time statistics and visualizations</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📹</div>
                    <div class="feature-title">Multiple Inputs</div>
                    <p>Support for images, videos, and live webcam streaming</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🎨</div>
                    <div class="feature-title">Visual Tracking</div>
                    <p>Colored bounding boxes with trajectory trails and unique IDs</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <div class="feature-title">Analytics</div>
                    <p>Real-time statistics, object counts, and tracking metrics</p>
                </div>
            </div>
            
            <h2 style="color: #667eea; margin: 30px 0 20px 0;">How It Works</h2>
            
            <div class="demo-image">
                <div style="font-size: 4em; margin-bottom: 20px;">🎬 ➔ 🎯 ➔ 🔄 ➔ 📊</div>
                <p style="font-size: 1.2em; color: #666;">
                    <strong>Input</strong> → <strong>Detect</strong> → <strong>Track</strong> → <strong>Display</strong>
                </p>
                <p style="margin-top: 15px; color: #666;">
                    Video frames are processed through YOLOv8 for detection, 
                    then SORT assigns unique IDs and tracks objects across frames
                </p>
            </div>
            
            <h2 style="color: #667eea; margin: 30px 0 20px 0;">Technology Stack</h2>
            
            <div class="tech-stack">
                <span class="tech-badge">Python 3.8+</span>
                <span class="tech-badge">Flask</span>
                <span class="tech-badge">YOLOv8</span>
                <span class="tech-badge">OpenCV</span>
                <span class="tech-badge">NumPy</span>
                <span class="tech-badge">SciPy</span>
                <span class="tech-badge">Kalman Filter</span>
                <span class="tech-badge">SORT Algorithm</span>
                <span class="tech-badge">HTML5 Canvas</span>
                <span class="tech-badge">JavaScript</span>
            </div>
            
            <h2 style="color: #667eea; margin: 30px 0 20px 0;">Getting Started</h2>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                <h3 style="margin-bottom: 15px;">Quick Start Guide</h3>
                <ol style="line-height: 2; margin-left: 20px;">
                    <li><strong>Install dependencies:</strong> <code style="background: white; padding: 5px 10px; border-radius: 5px;">pip install -r requirements.txt</code></li>
                    <li><strong>Start the server:</strong> <code style="background: white; padding: 5px 10px; border-radius: 5px;">python app.py</code></li>
                    <li><strong>Open browser:</strong> Navigate to <code style="background: white; padding: 5px 10px; border-radius: 5px;">http://localhost:5000</code></li>
                    <li><strong>Upload & Track:</strong> Upload a video/image or use your webcam!</li>
                </ol>
            </div>
            
            <h2 style="color: #667eea; margin: 30px 0 20px 0;">Use Cases</h2>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🚗</div>
                    <div class="feature-title">Traffic Monitoring</div>
                    <p>Track vehicles and analyze traffic patterns</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🏃</div>
                    <div class="feature-title">Sports Analytics</div>
                    <p>Track players and analyze game dynamics</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🛒</div>
                    <div class="feature-title">Retail Analytics</div>
                    <p>Monitor customer behavior in stores</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <div class="feature-title">Security Systems</div>
                    <p>Detect and track objects for surveillance</p>
                </div>
            </div>
            
            <div style="text-align: center; margin: 40px 0; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
                <h2 style="margin-bottom: 15px;">Ready to Get Started?</h2>
                <p style="font-size: 1.1em;">
                    Install the dependencies and launch the full dashboard to start tracking objects in real-time!
                </p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # Save demo page
    with open('demo.html', 'w') as f:
        f.write(demo_html)
    
    print("✓ Demo page created: demo.html")
    print("\nTo view the demo:")
    print("  Open demo.html in your browser")
    print("\nTo run the full application:")
    print("  1. pip install -r requirements.txt")
    print("  2. python app.py")
    print("  3. Open http://localhost:5000")


if __name__ == '__main__':
    create_demo_page()
