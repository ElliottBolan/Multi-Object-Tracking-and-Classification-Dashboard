#!/usr/bin/env python3
"""
Command-line interface for Multi-Object Tracking
Process videos or images from the command line
"""

import argparse
import sys
import os
from backend.utils.video_processor import VideoProcessor


def main():
    parser = argparse.ArgumentParser(
        description='Multi-Object Tracking and Classification CLI'
    )
    parser.add_argument(
        'input',
        help='Path to input video or image file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Path to output file (default: output_<input>)',
        default=None
    )
    parser.add_argument(
        '-m', '--model',
        help='YOLO model to use (default: yolov8n.pt)',
        default='yolov8n.pt'
    )
    parser.add_argument(
        '-c', '--confidence',
        help='Confidence threshold (default: 0.25)',
        type=float,
        default=0.25
    )
    parser.add_argument(
        '--max-age',
        help='Max frames to keep track alive (default: 30)',
        type=int,
        default=30
    )
    parser.add_argument(
        '--min-hits',
        help='Min detections before track is confirmed (default: 3)',
        type=int,
        default=3
    )
    parser.add_argument(
        '--iou-threshold',
        help='IoU threshold for matching (default: 0.3)',
        type=float,
        default=0.3
    )
    
    args = parser.parse_args()
    
    # Check input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Determine output path
    if args.output is None:
        base_name = os.path.basename(args.input)
        args.output = f'output_{base_name}'
    
    print(f"Processing: {args.input}")
    print(f"Output: {args.output}")
    print(f"Model: {args.model}")
    print(f"Confidence: {args.confidence}")
    print("-" * 50)
    
    # Initialize processor
    processor = VideoProcessor(
        model_path=args.model,
        conf_threshold=args.confidence
    )
    
    # Update tracker parameters
    from backend.utils.sort import Sort
    processor.tracker = Sort(
        max_age=args.max_age,
        min_hits=args.min_hits,
        iou_threshold=args.iou_threshold
    )
    
    try:
        # Check if input is image or video
        is_image = args.input.lower().endswith(('.jpg', '.jpeg', '.png'))
        
        if is_image:
            import cv2
            print("Processing image...")
            image = cv2.imread(args.input)
            if image is None:
                print(f"Error: Could not read image '{args.input}'")
                sys.exit(1)
            
            annotated_image, stats = processor.process_frame(image)
            cv2.imwrite(args.output, annotated_image)
            
            print("\nResults:")
            print(f"  Total tracks: {stats['total_tracks']}")
            print(f"  Detected objects: {stats['current_objects']}")
            
        else:
            print("Processing video...")
            stats_history = processor.process_video(args.input, args.output)
            
            # Print summary
            total_frames = len(stats_history)
            max_tracks = max([s['total_tracks'] for s in stats_history]) if stats_history else 0
            
            print("\nResults:")
            print(f"  Total frames: {total_frames}")
            print(f"  Max simultaneous tracks: {max_tracks}")
            if stats_history:
                final_objects = stats_history[-1].get('max_objects', {})
                print(f"  Object classes detected: {list(final_objects.keys())}")
        
        print(f"\nOutput saved to: {args.output}")
        print("Done!")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
