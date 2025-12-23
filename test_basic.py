#!/usr/bin/env python3
"""
Basic test script for Multi-Object Tracking Dashboard
Tests the core components without requiring models or video files
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask imported")
        
        import flask_cors
        print("✓ Flask-CORS imported")
        
        from backend.utils.sort import Sort, KalmanBoxTracker
        print("✓ SORT modules imported")
        
        import numpy as np
        print("✓ NumPy imported (if available)")
        
        print("\nBasic imports successful!")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("\nNote: Some imports may fail if dependencies aren't installed yet.")
        print("Run: pip install -r requirements.txt")
        return False


def test_sort_basic():
    """Test basic SORT functionality without actual data"""
    print("\nTesting SORT algorithm structure...")
    try:
        from backend.utils.sort import Sort
        tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)
        print(f"✓ SORT tracker created with {len(tracker.trackers)} trackers")
        print(f"✓ Frame count: {tracker.frame_count}")
        print(f"✓ Parameters: max_age={tracker.max_age}, min_hits={tracker.min_hits}, iou={tracker.iou_threshold}")
        return True
    except Exception as e:
        print(f"✗ SORT test failed: {e}")
        return False


def test_flask_app():
    """Test Flask app structure"""
    print("\nTesting Flask application structure...")
    try:
        from app import app
        print(f"✓ Flask app loaded: {app.name}")
        
        # Get registered routes
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        print(f"✓ Registered routes ({len(routes)}):")
        for route in sorted(routes):
            if not route.startswith('/static'):
                print(f"  - {route}")
        
        return True
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        return False


def test_config():
    """Test configuration module"""
    print("\nTesting configuration...")
    try:
        from config import Config, config
        print(f"✓ Config loaded")
        print(f"  - Default model: {Config.DEFAULT_MODEL}")
        print(f"  - Confidence threshold: {Config.CONFIDENCE_THRESHOLD}")
        print(f"  - Max content length: {Config.MAX_CONTENT_LENGTH / (1024*1024):.0f} MB")
        print(f"  - Upload folder: {Config.UPLOAD_FOLDER}")
        print(f"  - Output folder: {Config.OUTPUT_FOLDER}")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


def test_directory_structure():
    """Test that required directories exist or can be created"""
    print("\nTesting directory structure...")
    try:
        dirs = ['uploads', 'outputs', 'backend', 'backend/utils', 'templates']
        for dir_name in dirs:
            exists = os.path.exists(dir_name)
            if exists:
                print(f"✓ {dir_name}/ exists")
            else:
                print(f"! {dir_name}/ will be created on first run")
        
        # Check for key files
        files = ['app.py', 'requirements.txt', 'README.md', 'templates/index.html']
        for file_name in files:
            if os.path.exists(file_name):
                print(f"✓ {file_name} exists")
            else:
                print(f"✗ {file_name} missing")
        
        return True
    except Exception as e:
        print(f"✗ Directory test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Multi-Object Tracking Dashboard - Basic Tests")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Configuration", test_config()))
    results.append(("Imports", test_imports()))
    results.append(("SORT Algorithm", test_sort_basic()))
    results.append(("Flask App", test_flask_app()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All basic tests passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the server: python app.py")
        print("3. Open browser: http://localhost:5000")
    else:
        print("\n! Some tests failed. Check the output above.")
        print("Make sure to install dependencies: pip install -r requirements.txt")
    
    print("=" * 60)
    
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
