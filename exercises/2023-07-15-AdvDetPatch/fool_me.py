import argparse
import cv2
import torch
import numpy as np
from models.common import DetectMultiBackend
from utils.datasets import LoadImages
from utils.general import non_max_suppression, check_patchsize
from utils.torch_utils import select_device, time_sync


@torch.no_grad()
def run(weights='yolov5l.pt',  
        source='adv_images/stop.png',  # adversarial image path
        clean_path='images/stop.png',
        mask_path='adv_images/mask.png',
        imgsz=640,  # inference size (pixels)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='cpu',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        ):
    source = str(source)
    if not source.endswith(clean_path.split(".")[-1]):
        raise ValueError("File must have same format as clean image!")

    # Load model
    device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn)
    stride, pt, jit = model.stride, model.pt, model.jit

    # Half
    half &= pt and device.type != 'cpu'  # half precision only supported by PyTorch on CUDA
    if pt:
        model.model.half() if half else model.model.float()

    clean_img = cv2.imread(clean_path)
    clean_img = cv2.cvtColor(clean_img, cv2.COLOR_BGR2RGB)
    clean_img = torch.from_numpy(clean_img).to(device)
    clean_img = clean_img.float() / 255
    clean_img = clean_img[None].permute(0,3,1,2)
    mask = cv2.imread(mask_path)
    if len(mask.shape) == 2: 
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    else:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    unique_pixels = np.unique(mask)
    valid_pixels = [0, 255]
    invalid_pixels = set(unique_pixels) - set(valid_pixels)
    if invalid_pixels:
        raise ValueError("The mask must be a binary image.")
    if not((mask[:, :, 0] == mask[:, :, 1]).all() and (mask[:, :, 1] == mask[:, :, 2]).all()):
        raise ValueError("Mask channels are not the same.")    
    mask = torch.from_numpy(mask).to(device)
    mask = mask.float() / 255
    mask = mask[None].permute(0,3,1,2)
    assert mask.shape == clean_img.shape, "Image shapes must match."
        

    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt and not jit)

    # Run inference

    dt = [0.0, 0.0, 0.0]
    for path, im, im0s, vid_cap, s in dataset:
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1
        assert im.shape == clean_img.shape, "Image shapes must match."
        im = im * mask + clean_img * (1 - mask) # eval patch
        # Inference
        print('---------------------Start detecting----------------------')
        pred = model(im, augment=augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3
        if len(pred[0].cpu().numpy()) == 0 and check_patchsize(mask):
            print("[*]I see nothing!")
            print("[*]Give you the flag")
            print(getflag())
        elif not check_patchsize(mask):
            print("[*]Too many adversarial pixels!")
        else:
            print("[*]Please remove the object!")


def getflag():
    fd = open("/home/adv/flag")
    flag = fd.readline()
    fd.close()
    return flag


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='yolov5l.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default='adv_images/stop.png', help='file/dir/URL/glob')
    parser.add_argument('--clean_path', type=str, default='images/stop.png', help='clean_img')
    parser.add_argument('--mask_path', type=str, default='adv_images/mask.png', help='mask_img')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='cpu', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    # print_args(FILE.stem, opt)
    return opt


def main(opt):
    run(**vars(opt))
    

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
