import argparse, os, json, glob, yaml
from ultralytics import YOLO
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tqdm import tqdm

def load_yaml(p):
    with open(p, 'r') as f:
        return yaml.safe_load(f)

def gt_counts_from_labels(label_dir):
    counts = {}
    for f in glob.glob(os.path.join(label_dir, '*.txt')):
        imgname = os.path.splitext(os.path.basename(f))[0]
        with open(f, 'r') as lf:
            lines = [l.strip() for l in lf.readlines() if l.strip()]
        counts[imgname] = len(lines)
    return counts

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--data', required=True)
    p.add_argument('--conf_thres', type=float, default=0.25)
    p.add_argument('--iou_thres', type=float, default=0.45)
    args = p.parse_args()

    y = YOLO(args.model, task='detect')
    data = load_yaml(args.data)

    # Auto-detect dataset directory (same folder as data.yaml)
    data_dir = os.path.dirname(os.path.abspath(args.data))

    # Some YAMLs define relative paths like "../train/images"
    def resolve_path(rel_path):
        path = os.path.normpath(os.path.join(data_dir, rel_path))
        if not os.path.exists(path):
            # Try if nested inside "data" folder
            alt_path = os.path.join(data_dir, "data", rel_path)
            if os.path.exists(alt_path):
                return alt_path
        return path

    test_images_root = resolve_path(data.get('test', 'test/images'))
    test_labels_root = test_images_root.replace('images', 'labels')

    print(f"🗂 Using test images from: {test_images_root}")
    print(f"🗂 Using test labels from: {test_labels_root}")

    imgs = glob.glob(os.path.join(test_images_root, '*'))
    gt_counts = gt_counts_from_labels(test_labels_root)
    preds_counts = {}

    if not imgs:
        raise FileNotFoundError(f"No images found in {test_images_root}")
    if not gt_counts:
        raise FileNotFoundError(f"No label files found in {test_labels_root}")

    for im in tqdm(imgs, desc='Predicting'):
        res = y.predict(source=im, conf=args.conf_thres, iou=args.iou_thres, verbose=False)
        boxes = []
        for r in res:
            for b in r.boxes:
                boxes.append(b)
        imgname = os.path.splitext(os.path.basename(im))[0]
        preds_counts[imgname] = len(boxes)

    common = set(gt_counts.keys()) & set(preds_counts.keys())
    print(f"✅ Found {len(common)} matching images between ground truth and predictions.")

    if len(common) == 0:
        print("⚠️ No matching image names found — check image/label filenames or extensions.")
        print(f"Example GT files: {list(gt_counts.keys())[:5]}")
        print(f"Example Pred files: {list(preds_counts.keys())[:5]}")
        exit()

    y_gt = [gt_counts[k] for k in common]
    y_pred = [preds_counts[k] for k in common]

 
    # 🔧 Convert all counts to plain floats to avoid type issues
    y_gt = [float(v) for v in y_gt]
    y_pred = [float(v) for v in y_pred]

    # 🧮 Compute metrics safely
    try:
        mae = mean_absolute_error(y_gt, y_pred)
        mse = mean_squared_error(y_gt, y_pred)
        rmse = mse ** 0.5
        r2 = r2_score(y_gt, y_pred) if len(y_gt) > 1 else 0.0
    except Exception as e:
        print(f"⚠️ Metric computation failed: {e}")
        print(f"y_gt: {y_gt}")
        print(f"y_pred: {y_pred}")
        mae = rmse = r2 = 0.0

    out = {'mae': float(mae), 'rmse': float(rmse), 'r2': float(r2), 'n_images': len(common)}
    print("📊 Counting metrics:", out)

    with open('counting_report.json', 'w') as f:
        json.dump(out, f, indent=2)

    print("⚙️ Running detection validation...")
    y.val(data=args.data, conf=args.conf_thres, iou=args.iou_thres)
