# Backend — TreeSense API (FastAPI)

This folder contains the FastAPI backend for TreeSense. The backend receives uploaded aerial images, runs a YOLOv8 detection model to count trees, stores results in MongoDB, and exposes REST endpoints used by the frontend.

## Important files

- `main.py` — FastAPI application (endpoints: `/`, `/upload`, `/detections`, `/detections/{id}`, `/health`).
- `requirements.txt` — Python dependencies for the backend.
- `.env` — Environment variables (MongoDB connection string). **Do not commit sensitive credentials.**

## Quick start (local)

1. Create and activate a Python virtual environment (recommended):

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# or
.\venv\Scripts\activate.bat    # Windows cmd
# or on macOS / Linux:
# source venv/bin/activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create `.env` (example):

```properties
MONGO_URI=mongodb://localhost:27017
# or MongoDB Atlas connection string
```

4. Ensure you have a YOLO model file in `../models/` — supported filenames: `best.pt`, `hello.pt`, or `best.onnx`. The backend will try these in order. If you have an exported ONNX model, it will attempt to use that as well.

5. Run the server:

```powershell
uvicorn main:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoints

### GET `/`
Root endpoint — returns basic API info and whether the model loaded.

Example response:

```json
{
  "message": "TreeSense API is running",
  "model_loaded": true,
  "endpoints": ["/upload", "/detections", "/detections/{id}"]
}
```

### POST `/upload`
Upload an image for detection (multipart/form-data). The backend validates file type, runs the model, stores the detection in MongoDB and returns the detection record (with a string `id`).

Request:
- Form field `file`: binary image (jpeg/png)

Example curl:

```bash
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@/path/to/your/image.jpg"
```

Successful response:

```json
{
  "success": true,
  "message": "Detected 45 trees",
  "data": {
    "id": "650f1f77bcf86cd799439011",
    "filename": "image.jpg",
    "tree_count": 45,
    "avg_confidence": 0.87,
    "confidences": [0.92, 0.85, 0.90, ...],
    "image_size": {"width": 1920, "height": 1080},
    "timestamp": "2025-10-30T12:34:56.789"
  }
}
```

If the model file is missing or not loaded, the endpoint will return HTTP 500 with a helpful message.

### GET `/detections` (optional query param `limit`)
Return a list of recent detection records stored in MongoDB.

Example:

```
GET /detections?limit=50
```

Response shape:

```json
{
  "success": true,
  "count": 12,
  "data": [ { /* detection objects */ } ]
}
```

All `_id` values are converted to string `id` fields in responses to keep JSON serializable.

### GET `/detections/{id}`
Return a single detection record by its ID. Example:

```
GET /detections/650f1f77bcf86cd799439011
```

### GET `/health`
Health check: returns basic status about model loading and DB connectivity.

## Model loading behavior

- The backend attempts to load models in this order: `best.pt`, `hello.pt`, `best.onnx` (from the `models/` folder adjacent to the repository root).
- If no model is present the app will start but the `/upload` endpoint will return 500 until a model is available.
- If Ultralytics prints warnings about settings resetting after package upgrades, run `yolo settings` or review `%APPDATA%\Ultralytics\settings.json`.

## MongoDB notes

- Default DB: `tree_sense` and collection `detections`.
- We store detection metadata (filename, tree_count, avg_confidence, confidences[], image_size, timestamp).
- Backend converts MongoDB `_id` to string `id` for API responses. This avoids serialization errors (ObjectId is not JSON serializable).

## Common errors & troubleshooting

- Network Error in frontend:
  - Ensure backend is running and reachable at `NEXT_PUBLIC_API_URL` (frontend env).
  - Verify CORS: the backend includes CORS middleware; if you lock down origins ensure the frontend's origin is allowed.

- `Error loading model: No such file or directory`:
  - Place your `best.pt`, `hello.pt`, or `best.onnx` inside the `models/` folder. Restart the backend to pick it up.

- `ObjectId` serialization errors:
  - The backend already converts `_id` to string. If you still see serialization errors, ensure you aren't returning raw PyMongo cursors or documents containing `_id` in other custom responses.

- Ultralytics settings warnings:
  - These are informational. If you want to persist custom settings, run the `yolo settings` command per the ultralytics docs.

## Development notes

- The backend uses `python-dotenv` to load `.env`. Keep secrets out of version control.
- Use the included `requirements.txt` to install a compatible set of packages.
- If you're iterating on the ML model and want faster feedback, consider running model inference locally in a lightweight script before integrating into the server.

## Next steps / enhancements

- Add authentication to protect the upload endpoint.
- Add rate-limiting to avoid abuse when deployed publicly.
- Store original uploaded images (or thumbnails) in cloud storage (S3) and persist the URL in MongoDB.
- Add more rich metadata (GPS bounding box, georeferencing) when processing geospatial images.

---

If you'd like I can also add a minimal Postman collection or quick `httpie`/`curl` script for manual testing — tell me which one you prefer and I'll add it to the backend folder.