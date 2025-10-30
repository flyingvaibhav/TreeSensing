from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import os
import io
from PIL import Image
from ultralytics import YOLO

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="TreeSense API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["tree_sense"]

# Load YOLO model
# Try multiple possible model paths
MODEL_PATHS = [
    Path(__file__).parent.parent / "models" / "best.pt",
    Path(__file__).parent.parent / "models" / "hello.pt",
    Path(__file__).parent.parent / "models" / "best.onnx",
]

model = None
for model_path in MODEL_PATHS:
    if model_path.exists():
        try:
            print(f"🔍 Attempting to load model from {model_path}")
            model = YOLO(str(model_path))
            print(f"✅ Model loaded successfully from {model_path}")
            break
        except Exception as e:
            print(f"⚠️ Error loading {model_path}: {e}")
            continue

if model is None:
    print("❌ No valid model found. Please ensure a trained YOLO model exists in the models folder.")
    print("   Supported: best.pt, hello.pt, best.onnx")

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "TreeSense API is running",
        "model_loaded": model is not None,
        "endpoints": ["/upload", "/detections", "/detections/{id}"]
    }

# Tree detection endpoint
@app.post("/upload")
async def detect_trees(file: UploadFile = File(...)):
    """Upload an image and detect trees"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(400, "File must be an image")
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Check if model is loaded
        if model is None:
            raise HTTPException(500, "ML model not loaded")
        
        # Run detection
        results = model(image, conf=0.25)
        
        # Extract results
        boxes = results[0].boxes
        tree_count = len(boxes)
        confidences = boxes.conf.tolist() if tree_count > 0 else []
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Prepare detection data
        detection_data = {
            "filename": file.filename,
            "tree_count": tree_count,
            "avg_confidence": round(avg_confidence, 2),
            "confidences": [round(c, 2) for c in confidences],
            "image_size": {
                "width": image.width,
                "height": image.height
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to MongoDB
        result = db.detections.insert_one(detection_data)
        
        # Create response data (without _id, add string id)
        response_data = {
            "id": str(result.inserted_id),
            "filename": detection_data["filename"],
            "tree_count": detection_data["tree_count"],
            "avg_confidence": detection_data["avg_confidence"],
            "confidences": detection_data["confidences"],
            "image_size": detection_data["image_size"],
            "timestamp": detection_data["timestamp"]
        }
        
        return {
            "success": True,
            "message": f"Detected {tree_count} trees",
            "data": response_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error processing image: {str(e)}")

# Get all detections
@app.get("/detections")
def get_detections(limit: int = 50):
    """Fetch all detection records"""
    try:
        detections = list(
            db.detections.find()
            .sort("timestamp", -1)
            .limit(limit)
        )
        
        # Convert ObjectId to string for JSON serialization
        for detection in detections:
            detection["id"] = str(detection.pop("_id"))
        
        return {
            "success": True,
            "count": len(detections),
            "data": detections
        }
    except Exception as e:
        raise HTTPException(500, f"Error fetching detections: {str(e)}")

# Get detection by ID
@app.get("/detections/{detection_id}")
def get_detection(detection_id: str):
    """Fetch a specific detection record"""
    try:
        from bson import ObjectId
        detection = db.detections.find_one({"_id": ObjectId(detection_id)})
        
        if not detection:
            raise HTTPException(404, "Detection not found")
        
        # Convert ObjectId to string
        detection["id"] = str(detection.pop("_id"))
        
        return {
            "success": True,
            "data": detection
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error fetching detection: {str(e)}")

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "database_connected": client.server_info() is not None
    }
