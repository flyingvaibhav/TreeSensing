# Tree Imagining Application - Tree Detection using YOLOv8 Counts the Trees in Aerial Images

from ultralytics import YOLO
import os
from pathlib import Path

# Load your trained model
model = YOLO("best.pt")

# Define image paths
image_paths = ["sample/image1.jpeg", "sample/image2.jpeg"]

# Check if images exist
existing_images = [img for img in image_paths if os.path.exists(img)]

if not existing_images:
    print("Images not found in current directory!")
    print("Please ensure image1.jpg and image2.jpg are in the models folder")
else:
    print(f"Found {len(existing_images)} images\n")
    
    # Run inference
    results = model(existing_images, conf=0.25)
    
    total_trees = 0
    
    # Process results
    for i, result in enumerate(results):
        boxes = result.boxes
        tree_count = len(boxes)
        total_trees += tree_count
        
        print(f"{'='*60}")
        print(f"Image: {existing_images[i]}")
        print(f"Trees detected: {tree_count}")
        
        if tree_count > 0:
            confidences = boxes.conf.tolist()
            print(f"Confidence scores: {[f'{conf:.2f}' for conf in confidences]}")
            print(f"Average confidence: {sum(confidences)/len(confidences):.2f}")
        
        # Display result
        result.show()
        
        # Save result with detected boxes
        output_name = f"result_{Path(existing_images[i]).stem}.jpg"
        result.save(filename=output_name)
        print(f"Saved result to: {output_name}")
        print(f"{'='*60}\n")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total images processed: {len(existing_images)}")
    print(f"Total trees detected: {total_trees}")
    print(f"Average trees per image: {total_trees/len(existing_images):.2f}")
    print(f"{'='*60}")