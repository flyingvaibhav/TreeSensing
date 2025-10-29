
import argparse, os, glob, time
from ultralytics import YOLO

def latest_checkpoint(experiments_dir):
    ckpts = glob.glob(os.path.join(experiments_dir, '**','*.pt'), recursive=True)
    if not ckpts: return None
    ckpts = sorted(ckpts, key=os.path.getmtime)
    return ckpts[-1]

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--data', required=True)
    p.add_argument('--model', default='yolov8n.pt', help='yolov8n/yolov8s/etc or path')
    p.add_argument('--epochs', type=int, default=50)
    p.add_argument('--batch', type=int, default=8)
    p.add_argument('--imgsz', type=int, default=640)
    p.add_argument('--project', default=None)
    p.add_argument('--save_period', type=int, default=5)
    p.add_argument('--resume', action='store_true')
    p.add_argument('--wandb', action='store_true')
    args = p.parse_args()

    project_dir = args.project or os.path.join(os.path.dirname(args.data), '..','experiments')
    os.makedirs(project_dir, exist_ok=True)

    # resume auto-detect
    ckpt = None
    if args.resume:
        ckpt = latest_checkpoint(project_dir)
        if ckpt:
            print("Resuming from", ckpt)

    y = YOLO(args.model)
    # training is passed as a dict to y.train
    train_params = dict(
        data=args.data,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        project=project_dir,
        name=f'train_{int(time.time())}',
        save_period=args.save_period,
        device='0',
        workers=4,
    )
    # optionally pass resume ckpt
    if ckpt:
        train_params['resume'] = ckpt

    # Optional W&B: ultralytics supports using env WANDB_MODE or API key.
    if args.wandb:
        os.environ['WANDB_MODE'] = 'online'

    print("Starting training with params:", train_params)
    y.train(**train_params)