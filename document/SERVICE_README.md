# 🌳 TreeSense - Complete Tree Detection Service

## System Overview

A full-stack tree detection service that uses AI/ML to automatically detect and count trees in aerial images.

### Architecture Flow

```
[Frontend: Next.js]
       ↓ (upload image)
[Backend: FastAPI (Python)]
       ↓ (send to ML Model)
[ML Model: YOLOv8 Tree Detection]
       ↓ (detection results)
[Database: MongoDB]
       ↓ (store metadata + results)
[Frontend]
       ↑ (fetch and display info)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- MongoDB (local or Atlas)
- YOLO model file (`best.pt` in `/models` folder)

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "MONGO_URI=your_mongodb_connection_string" > .env

# Run server
uvicorn main:app --reload
```

Backend will run on: `http://127.0.0.1:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install
# or
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > .env.local

# Run development server
pnpm dev
# or
npm run dev
```

Frontend will run on: `http://localhost:3000`

---

## 📁 Project Structure

```
TreeImagining/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # MongoDB connection
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx           # Home page
│   │   │   ├── upload/page.tsx    # Upload & detect
│   │   │   └── trees/page.tsx     # Detection history
│   │   ├── constants/
│   │   │   ├── types.ts           # TypeScript interfaces
│   │   │   └── config.ts          # API endpoints & config
│   │   ├── utils/
│   │   │   └── api.ts             # API client functions
│   │   └── lib/
│   │       └── config.ts          # Axios setup
│   └── package.json
│
└── models/
    └── best.pt              # Trained YOLO model
```

---

## 🔌 API Endpoints

### Backend (FastAPI)

#### `GET /`
Root endpoint - API info
```json
{
  "message": "TreeSense API is running",
  "model_loaded": true,
  "endpoints": ["/upload", "/detections", "/detections/{id}"]
}
```

#### `POST /upload`
Upload image for tree detection

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "success": true,
  "message": "Detected 45 trees",
  "data": {
    "filename": "aerial_image.jpg",
    "tree_count": 45,
    "avg_confidence": 0.87,
    "confidences": [0.92, 0.85, 0.90, ...],
    "image_size": {
      "width": 1920,
      "height": 1080
    },
    "timestamp": "2025-10-30T12:34:56.789"
  }
}
```

#### `GET /detections`
Get all detection records

**Query Parameters:**
- `limit` (optional, default: 50)

**Response:**
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "filename": "image1.jpg",
      "tree_count": 45,
      "avg_confidence": 0.87,
      "timestamp": "2025-10-30T12:34:56.789"
    }
  ]
}
```

#### `GET /detections/{id}`
Get specific detection by ID

#### `GET /health`
Health check endpoint

---

## 🎨 Frontend Pages

### 1. Home Page (`/`)
- Landing page with navigation cards
- Links to Upload and History
- Feature showcase

### 2. Upload Page (`/upload`)
- Image upload interface
- Real-time preview
- Detection results display
- Shows: tree count, confidence, image details

### 3. History Page (`/trees`)
- Table view of all detections
- Statistics dashboard
- Sortable and filterable results

---

## 💾 Database Schema

### MongoDB Collection: `detections`

```javascript
{
  "_id": ObjectId("..."),
  "filename": "aerial_photo.jpg",
  "tree_count": 45,
  "avg_confidence": 0.87,
  "confidences": [0.92, 0.85, 0.90, ...],
  "image_size": {
    "width": 1920,
    "height": 1080
  },
  "timestamp": "2025-10-30T12:34:56.789"
}
```

---

## 🧪 Testing the Service

### 1. Test Backend Health
```bash
curl http://127.0.0.1:8000/health
```

### 2. Upload Test Image
```bash
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@/path/to/image.jpg"
```

### 3. Get Detections
```bash
curl http://127.0.0.1:8000/detections
```

---

## 🔧 Configuration

### Backend `.env`
```properties
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/treesense
```

### Frontend `.env.local`
```properties
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

---

## 📊 ML Model

- **Model**: YOLOv8 (Ultralytics)
- **Task**: Object Detection
- **Classes**: 1 (tree)
- **Confidence Threshold**: 0.25
- **Location**: `models/best.pt`

---

## 🎯 Features

✅ **Upload & Detect** - Upload aerial images for tree detection  
✅ **Real-time Results** - Instant detection with confidence scores  
✅ **History Tracking** - View all previous detections  
✅ **MongoDB Storage** - Persistent data storage  
✅ **Type-Safe** - Full TypeScript support  
✅ **Clean UI** - Modern, responsive interface  
✅ **RESTful API** - Well-documented endpoints  

---

## 🛠️ Tech Stack

**Frontend:**
- Next.js 14 (React 18)
- TypeScript
- Tailwind CSS
- Axios

**Backend:**
- FastAPI (Python)
- Ultralytics YOLOv8
- PyMongo
- Pillow (PIL)

**Database:**
- MongoDB (Atlas or Local)

**ML:**
- YOLOv8 (Object Detection)
- PyTorch (Backend)

---

## 🐛 Troubleshooting

### Backend won't start
- Check if MongoDB is running
- Verify `best.pt` model exists in `/models` folder
- Install all requirements: `pip install -r requirements.txt`

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Check CORS settings in `main.py`

### Model not loading
- Ensure `best.pt` is in the correct path
- Check file permissions
- Verify ultralytics is installed: `pip install ultralytics`

---

## 📝 Development

### Adding New Endpoints

1. Add to `backend/main.py`
2. Update `frontend/src/constants/config.ts`
3. Create API function in `frontend/src/utils/api.ts`
4. Use in components

### Adding New Types

1. Define in `frontend/src/constants/types.ts`
2. Use throughout the application

---

## 📈 Future Enhancements

- [ ] User authentication
- [ ] Image annotation viewer
- [ ] Export results (CSV, PDF)
- [ ] Batch processing
- [ ] Species classification
- [ ] Health assessment
- [ ] GIS integration
- [ ] Mobile app

---

## 📄 License

GNU AGPLv3

---

## 👥 Contributors

- Vaibhav - [@flyingvaibhav](https://github.com/flyingvaibhav)

---

## 🙏 Acknowledgments

- Ultralytics YOLOv8
- Roboflow for dataset
- Smart India Hackathon

---

**Built with ❤️ for TreeSense Imaging**
