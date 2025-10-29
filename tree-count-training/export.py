
import argparse
from ultralytics import YOLO

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--weights', required=True)
    p.add_argument('--format', default='onnx', choices=['onnx','torchscript','pb'])
    p.add_argument('--imgsz', type=int, default=640)
    args = p.parse_args()
    y = YOLO(args.weights)
    print("Exporting to", args.format)
    y.export(format=args.format, imgsz=args.imgsz)