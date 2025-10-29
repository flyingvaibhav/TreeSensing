# 🌳 TreeImagining - Automated Tree Detection & Counting System

## 📋 Project Overview

**TreeImagining** is an advanced computer vision project that leverages YOLOv8 deep learning models to automatically detect and count trees in aerial imagery. This system is designed to support forest management, environmental conservation, and developmental projects requiring accurate tree enumeration.

### 🎯 Project Objectives

1. **Automate Tree Counting**: Replace manual tree counting methods with AI-powered automation
2. **Improve Accuracy**: Reduce human error in tree enumeration using object detection
3. **Scale Forest Management**: Enable rapid processing of large forest areas through aerial imagery
4. **Support Decision Making**: Provide quantitative data for forest conservation and development planning

---

## 🏗️ Project Structure

```
TreeImagining/
├── models/                          # Production inference models
│   ├── app.py                      # Main inference application
│   ├── best.pt                     # Trained YOLOv8 model (PyTorch)
│   ├── best.onnx                   # Exported ONNX model for deployment
│   ├── hello.pt                    # Additional model checkpoint
│   ├── sample/                     # Sample test images
│   │   ├── image1.jpeg
│   │   └── image2.jpeg
│   └── results/                    # Detection results with bounding boxes
│       ├── result_image1.jpg
│       └── result_image2.jpg
│
├── tree-count-training/            # Model training pipeline
│   ├── data/                       # Training dataset
│   │   ├── data.yaml              # Dataset configuration
│   │   ├── train/                 # Training images & labels
│   │   ├── valid/                 # Validation images & labels
│   │   └── test/                  # Testing images & labels
│   ├── model-training.ipynb       # Interactive training notebook
│   ├── train.py                   # Training script with CLI
│   ├── data_prep.py               # Dataset preparation utilities
│   ├── evaluate.py                # Model evaluation metrics
│   ├── visualize.py               # Visualization utilities
│   ├── export.py                  # Model export (ONNX, TorchScript)
│   ├── notebooks/                 # Experimental notebooks
│   └── reports/                   # Training reports & visualizations
│       ├── predictions.html
│       └── viz/
│
├── env/                            # Python virtual environment
├── requirements.txt                # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

---

## 🔬 Technical Architecture

### Data Pipeline

1. **Data Acquisition**: Aerial/satellite imagery from Roboflow (CC BY 4.0 license)
2. **Data Preparation**: COCO/VOC format conversion to YOLO format
3. **Data Augmentation**: Albumentations library for image transformations
4. **Dataset Split**: 80% train, 10% validation, 10% test

### Model Architecture

- **Base Model**: YOLOv8 (You Only Look Once v8)
- **Task**: Object Detection (Single class: 'tree')
- **Input Size**: 640x640 pixels
- **Confidence Threshold**: 0.25
- **IoU Threshold**: 0.45

### Training Process

```python
# Key Training Parameters
- Model: yolov8n.pt (nano) / yolov8s.pt (small)
- Epochs: 50 (configurable)
- Batch Size: 8
- Image Size: 640x640
- Optimizer: AdamW
- Device: GPU (CUDA) / CPU fallback
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ (Tested on Python 3.13)
- CUDA-capable GPU (optional, but recommended)
- 8GB+ RAM
- Windows/Linux/macOS

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/flyingvaibhav/TreeSensing.git
cd TreeImagining
```

2. **Create virtual environment**
```bash
python -m venv env
# Windows
.\env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Quick Start - Run Inference

```bash
cd models
python app.py
```

This will:
- Load the trained `best.pt` model
- Process images in the `sample/` folder
- Display detection results
- Save annotated images to `results/`
- Print tree counts and confidence scores

---

## 📊 Model Training

### Option 1: Using Training Script

```bash
cd tree-count-training
python train.py --data data/data.yaml --model yolov8n.pt --epochs 50 --batch 8
```

**Training Arguments:**
- `--data`: Path to data.yaml configuration
- `--model`: Pretrained model (yolov8n/s/m/l/x.pt)
- `--epochs`: Number of training epochs
- `--batch`: Batch size
- `--imgsz`: Image size (default: 640)
- `--resume`: Resume from checkpoint
- `--wandb`: Enable Weights & Biases logging

### Option 2: Using Jupyter Notebook

```bash
cd tree-count-training
jupyter notebook model-training.ipynb
```

The notebook includes:
- Dataset exploration and visualization
- Model training with progress tracking
- Validation metrics and graphs
- Result analysis and predictions

---

## 📈 Model Evaluation

### Evaluate Model Performance

```bash
cd tree-count-training
python evaluate.py --model ../models/best.pt --data data/data.yaml
```

**Metrics Generated:**
- **MAE** (Mean Absolute Error): Average counting error
- **RMSE** (Root Mean Squared Error): Prediction accuracy
- **R²** (R-squared): Model fit quality
- **mAP50**: Mean Average Precision at IoU=0.50
- **mAP50-95**: Mean Average Precision at IoU=0.50:0.95
- **Precision**: True positive rate
- **Recall**: Detection completeness

Output saved to: `counting_report.json`

---

## 🎨 Visualization

### Generate Prediction Visualizations

```bash
cd tree-count-training
python visualize.py --model ../models/best.pt --data data/data.yaml --out viz_out
```

Creates annotated images with:
- Bounding boxes around detected trees
- Confidence scores for each detection
- Saved to `viz_out/` directory

---

## 📦 Model Export

### Export to ONNX Format

```bash
cd tree-count-training
python export.py --weights ../models/best.pt --format onnx --imgsz 640
```

**Supported Formats:**
- `onnx`: ONNX Runtime (cross-platform deployment)
- `torchscript`: TorchScript (PyTorch production)
- `pb`: TensorFlow format

---

## 🔧 Dataset Preparation

### Convert Custom Dataset to YOLO Format

```bash
cd tree-count-training
# From COCO format
python data_prep.py --coco-json path/to/annotations.json --images path/to/images --dst prepared_data

# From VOC format
python data_prep.py --voc-images path/to/images --voc-anno path/to/annotations --dst prepared_data
```

Creates YOLO-compatible structure:
```
prepared_data/
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

---

## 📋 Dataset Information

**Source**: Roboflow Universe - Tree Counting Dataset  
**License**: CC BY 4.0  
**Classes**: 1 (tree)  
**Format**: YOLO v8  
**Split Ratio**: 80/10/10 (train/valid/test)

Dataset YAML Configuration:
```yaml
train: ../train/images
val: ../valid/images
test: ../test/images
nc: 1
names: ['tree']
```

---

## 🌐 Related Projects

This project is part of the **TreeSense Imaging** ecosystem - a comprehensive Smart India Hackathon solution for forest management:

### TreeSense Features:
- **Tree Count**: Automated tree enumeration (this project)
- **Green Cover Estimator**: Calculate vegetation percentage
- **Tree Species Identifier**: ML-based species classification
- **Optimal Pathing**: Route planning through forest areas
- **Historical Data**: Time-series analysis of forest changes

🔗 Full Project: [treesense-imaging/](../treesense-imaging/)

---

## 🛠️ Technology Stack

### Core Libraries
- **ultralytics**: YOLOv8 implementation
- **torch**: PyTorch deep learning framework
- **opencv-python**: Image processing
- **numpy**: Numerical computations
- **pandas**: Data manipulation

### Computer Vision & ML
- **torchvision**: Vision utilities
- **scikit-learn**: Evaluation metrics
- **albumentations**: Data augmentation
- **matplotlib**: Visualization

### Geospatial (Future Integration)
- **rasterio**: Geospatial raster processing
- **geopandas**: Geospatial data frames
- **shapely**: Geometric operations

### Backend (Optional)
- **fastapi**: REST API framework
- **uvicorn**: ASGI server
- **celery**: Distributed task queue

---

## 📊 Results & Performance

### Model Performance Metrics
*(Update after training completion)*

| Metric | Value |
|--------|-------|
| mAP50 | TBD |
| mAP50-95 | TBD |
| Precision | TBD |
| Recall | TBD |
| MAE (Count) | TBD |
| RMSE (Count) | TBD |

### Sample Predictions

- **Image 1**: Detection with bounding boxes saved to `models/results/result_image1.jpg`
- **Image 2**: Detection with bounding boxes saved to `models/results/result_image2.jpg`

---

## 🔍 Use Cases

1. **Forest Conservation**: Monitor tree population in protected areas
2. **Urban Planning**: Count trees in city planning projects
3. **Environmental Impact Assessment**: Quantify deforestation/reforestation
4. **Agricultural Management**: Inventory orchard trees
5. **Carbon Credit Verification**: Validate carbon sequestration claims
6. **Research**: Biodiversity and ecosystem studies

---

## 🐛 Troubleshooting

### Common Issues

**1. CUDA Out of Memory**
```bash
# Reduce batch size
python train.py --batch 4 --imgsz 416
```

**2. Model Not Found**
```bash
# Ensure you're in the correct directory
cd models
ls best.pt  # Should exist
```

**3. Dataset Path Errors**
- Check `data.yaml` paths are relative to the YAML file location
- Verify images and labels folders exist

**4. Dependencies Issues**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under **GNU AGPLv3**

Dataset is licensed under **CC BY 4.0** (Roboflow)

---

## 👥 Authors & Contributors

- **Vaibhav** - [@flyingvaibhav](https://github.com/flyingvaibhav)
- TreeSense Team - Smart India Hackathon 2023

---

## 📞 Contact & Support

- **Repository**: [github.com/flyingvaibhav/TreeSensing](https://github.com/flyingvaibhav/TreeSensing)
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Website**: [treesense.vipulchaturvedi.com](https://treesense.vipulchaturvedi.com/predict)

---

## 🙏 Acknowledgments

- **Ultralytics** for YOLOv8 implementation
- **Roboflow** for dataset hosting and annotation tools
- **Smart India Hackathon** for project inspiration
- **Open Source Community** for excellent ML libraries

---

## 🗺️ Roadmap

### Current Features ✅
- [x] YOLOv8 object detection model
- [x] Training pipeline with CLI
- [x] Jupyter notebook training
- [x] Model evaluation metrics
- [x] ONNX export for deployment
- [x] Basic inference application

### Planned Features 🚧
- [ ] Web API with FastAPI
- [ ] Real-time video processing
- [ ] Multi-model ensemble
- [ ] Geospatial coordinate mapping
- [ ] Integration with GIS systems
- [ ] Mobile app deployment
- [ ] Cloud deployment (AWS/Azure)
- [ ] Tree species classification
- [ ] Tree health assessment

---

## 📚 Documentation

### Additional Resources
- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Dataset on Roboflow](https://universe.roboflow.com/project-s402o/tree-counting-qiw3h/dataset/1)
- [Training Best Practices](https://github.com/ultralytics/ultralytics/wiki)

---

**⭐ If you find this project useful, please consider giving it a star!**

Last Updated: October 30, 2025
