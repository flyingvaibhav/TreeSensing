
import os, argparse, json, shutil, math
from glob import glob
from pathlib import Path
import cv2
import numpy as np
import random
from collections import defaultdict
from xml.etree import ElementTree as ET

def ensure_dirs(dst):
    for d in ['train/images','train/labels','val/images','val/labels','test/images','test/labels']:
        os.makedirs(os.path.join(dst,d), exist_ok=True)

def copy_files(file_list, dst_images, dst_labels, src_labels_ext='.txt'):
    for img in file_list:
        name = os.path.basename(img)
        base, _ = os.path.splitext(name)
        dst_img = os.path.join(dst_images, name)
        shutil.copy(img, dst_img)
        src_label = os.path.join(os.path.dirname(img), base + src_labels_ext)
        if os.path.exists(src_label):
            shutil.copy(src_label, os.path.join(dst_labels, base + '.txt'))
        else:
            # create empty label file so trainer knows no objects
            open(os.path.join(dst_labels, base + '.txt'), 'w').close()

def coco_to_yolo(src_coco_json, images_dir, dst_dir, val_split=0.1, test_split=0.1):
    """
   
    """
    with open(src_coco_json, 'r') as f:
        coco = json.load(f)
    id2name = {c['id']:c['name'] for c in coco['categories']}
    name2id = {v:k for k,v in id2name.items()}
    ann_by_img = defaultdict(list)
    for a in coco['annotations']:
        ann_by_img[a['image_id']].append(a)
    imgid2f = {i['id']: i for i in coco['images']}
    ensure_dirs(dst_dir)
    all_images = []
    for img_id, imginfo in imgid2f.items():
        fname = imginfo['file_name']
        src_img = os.path.join(images_dir, fname)
        if not os.path.exists(src_img):
            print("Skipping missing", src_img); continue
        base = os.path.splitext(fname)[0]
        dst_img = os.path.join(dst_dir, 'train','images', fname)  # temporary: move later to split
        shutil.copy(src_img, dst_img)
        # write label
        h,w = imginfo['height'], imginfo['width']
        ann_list = ann_by_img.get(img_id, [])
        with open(os.path.join(dst_dir,'train','labels', base + '.txt'), 'w') as lf:
            for a in ann_list:
                bbox = a['bbox']  # COCO: x,y,w,h
                x,y,bw,bh = bbox
                x_c = x + bw/2
                y_c = y + bh/2
                # normalize
                xc, yc, nw, nh = x_c/w, y_c/h, bw/w, bh/h
                cls = a['category_id']-1 if a['category_id']>0 else 0
                lf.write(f"{cls} {xc:.6f} {yc:.6f} {nw:.6f} {nh:.6f}\\n")
        all_images.append(dst_img)
    # split
    random.shuffle(all_images)
    N = len(all_images)
    ntest = int(N*0.1)
    nval = int(N*0.1)
    train = all_images[ntest+nval:]
    val = all_images[:nval]
    test = all_images[nval: nval+ntest]
    # move files to respective folders
    for src in train:
        base = os.path.basename(src)
        shutil.move(src, os.path.join(dst_dir,'train','images', base))
    for src in val:
        base = os.path.basename(src)
        shutil.move(src, os.path.join(dst_dir,'val','images', base))
        # move corresponding label file
        base_noext = os.path.splitext(base)[0]
        lbl = os.path.join(dst_dir,'train','labels', base_noext + '.txt')
        if os.path.exists(lbl):
            shutil.move(lbl, os.path.join(dst_dir,'val','labels', base_noext + '.txt'))
    for src in test:
        base = os.path.basename(src)
        shutil.move(src, os.path.join(dst_dir,'test','images', base))
        base_noext = os.path.splitext(base)[0]
        lbl = os.path.join(dst_dir,'train','labels', base_noext + '.txt')
        if os.path.exists(lbl):
            shutil.move(lbl, os.path.join(dst_dir,'test','labels', base_noext + '.txt'))
    print("COCO -> YOLO structure created at", dst_dir)

def voc_to_yolo(voc_images_dir, voc_anno_dir, dst_dir):
    ensure_dirs(dst_dir)
    imfiles = glob(os.path.join(voc_images_dir, '*'))
    for img in imfiles:
        name = os.path.basename(img)
        base = os.path.splitext(name)[0]
        annf = os.path.join(voc_anno_dir, base + '.xml')
        dst_img = os.path.join(dst_dir, 'train','images', name)
        shutil.copy(img, dst_img)
        h,w = 0,0
        if os.path.exists(annf):
            tree = ET.parse(annf)
            root = tree.getroot()
            size = root.find('size')
            w = int(size.find('width').text); h = int(size.find('height').text)
            with open(os.path.join(dst_dir,'train','labels', base + '.txt'),'w') as lf:
                for obj in root.findall('object'):
                    cls = obj.find('name').text
                    bnd = obj.find('bndbox')
                    xmin = float(bnd.find('xmin').text)
                    ymin = float(bnd.find('ymin').text)
                    xmax = float(bnd.find('xmax').text)
                    ymax = float(bnd.find('ymax').text)
                    bw = xmax - xmin; bh = ymax - ymin
                    xc = xmin + bw/2; yc = ymin + bh/2
                    lf.write(f"0 {xc/w:.6f} {yc/h:.6f} {bw/w:.6f} {bh/h:.6f}\\n")
    print("VOC -> YOLO minimal conversion done.")

def tile_image(img_path, out_dir, tile_size=512, stride=512, min_area_frac=0.001):
    os.makedirs(out_dir, exist_ok=True)
    im = cv2.imread(img_path)
    h,w = im.shape[:2]
    tile_id = 0
    for y in range(0, h, stride):
        for x in range(0, w, stride):
            x2 = min(w, x + tile_size)
            y2 = min(h, y + tile_size)
            tile = im[y:y2, x:x2]
            if tile.size == 0: continue
            # skip mostly empty tiles
            if (tile.mean() < 240):  # heuristic: not all-white
                out_path = os.path.join(out_dir, f"{Path(img_path).stem}_tile_{tile_id}.jpg")
                cv2.imwrite(out_path, tile)
                tile_id += 1
    return tile_id

def sample_data_yaml(dst_dir, nc=1, names=['tree']):
    content = {
        'path': dst_dir,
        'train': 'data/train/images',
        'val': 'data/val/images',
        'test': 'data/test/images',
        'nc': nc,
        'names': names
    }
    import yaml
    with open(os.path.join(dst_dir, 'data.yaml'), 'w') as f:
        yaml.dump(content, f)
    print("Wrote", os.path.join(dst_dir,'data.yaml'))

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--mode', default='sample_yaml', choices=['sample_yaml','coco_to_yolo','voc_to_yolo','tile'])
    p.add_argument('--src', type=str, help='source path or json')
    p.add_argument('--images', type=str, help='images dir')
    p.add_argument('--dst', default='./data', type=str)
    p.add_argument('--tile_size', default=512, type=int)
    p.add_argument('--stride', default=512, type=int)
    args = p.parse_args()
    if args.mode == 'sample_yaml':
        sample_data_yaml(args.dst)
    elif args.mode == 'coco_to_yolo':
        coco_to_yolo(args.src, args.images, args.dst)
    elif args.mode == 'voc_to_yolo':
        voc_to_yolo(args.images, args.src, args.dst)
    elif args.mode == 'tile':
        print(tile_image(args.src, args.dst, tile_size=args.tile_size, stride=args.stride))