
import os, argparse, yaml, json
import cv2, numpy as np, matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, mean_absolute_error
from ultralytics import YOLO

def draw_boxes(img_path, boxes, scores=None, labels=None, out_path=None):
    im = cv2.imread(img_path)
    for i,box in enumerate(boxes):
        x1,y1,x2,y2 = map(int, box)
        cv2.rectangle(im, (x1,y1), (x2,y2), (0,255,0), 2)
        caption = f"{scores[i]:.2f}" if scores is not None else ""
        cv2.putText(im, caption, (x1, max(0,y1-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    if out_path:
        cv2.imwrite(out_path, im)
    return im

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--data', required=True)
    p.add_argument('--out', default='viz_out')
    args = p.parse_args()
    os.makedirs(args.out, exist_ok=True)
    y = YOLO(args.model)
    with open(args.data, 'r') as f:
        data = yaml.safe_load(f)
    test_images_root = os.path.join(data['path'], data['test'])
    import glob
    imgs = glob.glob(os.path.join(test_images_root, '*'))[:50]
    for im in imgs:
        res = y.predict(source=im, conf=0.25, verbose=False)
        boxes=[]
        scores=[]
        for r in res:
            for b in r.boxes:
                xyxy = b.xyxy[0].cpu().numpy()
                conf = float(b.conf[0].cpu().numpy())
                boxes.append(xyxy)
                scores.append(conf)
        outp = os.path.join(args.out, os.path.basename(im))
        draw_boxes(im, boxes, scores, out_path=outp)
    print("Saved visualizations to", args.out)