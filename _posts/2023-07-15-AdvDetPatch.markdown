---
layout: post
title:  AdvDetPatch
date:   2023-07-15 00:08:01 +0300
image:  2023-07-15-friendship.jpg
tags:   [ctf,misc,AdversarialExamples]
---

# AdvDetPatch

目标检测技术广泛应用于视频监控、智能驾驶等安全关键型领域，因此检验目标检测模型的脆弱性至关重要。对抗补丁攻击通过修改图像的局部区域来达到欺骗目标检测模型的目的，是最实用的攻击方法之一。在现实世界中，攻击者可以在路牌上贴上精心设计的贴纸或者制作具有补丁图案的衣服来欺骗目标检测器。本题目考虑针对目标检测模型的对抗补丁攻击，要求选手通过添加补丁使检测框消失，避开检测，同时要求修改的图像区域尽可能小。为实现这一目标，补丁的形状、位置、纹理等都是需要考虑的因素。

### 题目要求

本次竞赛要求选手针对目标检测模型进行对抗攻击。题目提供了1张样例图片（/home/adv/images/stop.png），要求选手在给定的图片中添加一些对抗性补丁，上传带有补丁的图片和代表补丁位置的mask，要求：

1. 使得模型无法正确地检测出图片中的所有物体
2. 并且补丁的面积不能超过图像面积的5%（例如对于640 * 640的图像，patch面积不超过20480 ），就能得到flag。

- 图像的尺寸、命名、文件格式（`.png`）和原始图像保持一致。
- mask图像只存在0或255两种像素值，其中255代表patch像素占据的位置。文件名保存为`mask.png`，mask的白色部分代表补丁部分，黑色是未修改部分。

### 选手的操作过程

1. 使用ctf账号通过ssh连接进来
2. 分析`/home/adv/`的题目，并自行训练出对抗样本
3. 选手上传2个图片，分别是`stop.png`和`mask.png`，放置在`/home/adv/adv_images/`文件夹中里
4. 测试能否得到flag

```sh
# 以下命令的文件路径必须写对
sudo python3 /home/adv/fool_me.py
# 若是符合题目要求，执行后就会得到flag
# 执行前/home/adv/adv_images/必须有stop.png和mask.png，否则会报错
```

5. 容器里提供了`sz`、`rz`等命令。

### 解法

题目的模型是白盒，因此我们可以采用一个经典方法：冻结神经网络的参数，而去对input图片进行梯度下降，迭代到模型认为input里面不包含目标为止。

第一个问题是如何选择loss函数。yolov5首先产生25200个候选bbox，经过NMS流程之后选出最终结果。最理想的情况是直接使得最终预测结果为空集，但无法实现，因为不可导。

我们退而求其次，考虑尽量使得那25200个候选bbox的置信度变低。我们简单地选择loss为这25200个 bbox 的置信度之和。对原始图片，这个值大约是 71.7。

第二个问题是，题目只允许修改20480个像素，因此我们必须选择那些“更容易影响模型预测结果”的像素。我们的解决方式是：首先用原图跑一遍模型，进行反向传播，保留图像中梯度绝对值最大的20480个像素，认为这些像素对答案影响最大，以后就只修改这些像素。

细节上，我们使用了Adam优化器以期快速收敛，最终在第14轮迭代时成功欺骗了神经网络。另外，我们最后修改完的input是一个3×640×640浮点数矩阵，它每个元素不一定在 `[0, 1]`之间，我们要把它限制在`[0, 1]`范围内，再乘以255转uint8。

### job.py

```assembly
import argparse
import cv2
import torch
import numpy as np
from models.common import DetectMultiBackend
from utils.datasets import LoadImages
from utils.general import non_max_suppression, check_patchsize
from utils.torch_utils import select_device, time_sync
import matplotlib.pyplot as plt
import matplotlib
import pickle
from PIL import Image

matplotlib.use('TkAgg')


# @torch.no_grad()
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

    model.requires_grad_(False)

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

    dataset = LoadImages(clean_path, img_size=imgsz, stride=stride, auto=pt and not jit)

    # Run inference

    for path, im, im0s, vid_cap, s in dataset:
        im = torch.from_numpy(im).to(device)
        im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0

        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        im.requires_grad_(True)

        assert im.shape == clean_img.shape, "Image shapes must match."

        # im = im * mask + clean_img * (1 - mask) # eval patch
        # Inference
        print('---------------------Start detecting----------------------')

        # 首次运行，选择梯度绝对值最大的 20480 个像素

        # pred = model(im, augment=augment, visualize=visualize)
        # conf = pred[0, :, 4].sum()
        # print('box置信度总和', conf.detach())

        # conf.backward()
        # print(im.grad)

        # t = [
        #     (im.grad[0, :, x, y].abs().sum(), x, y) 
        #         for x in range(640) 
        #             for y in range(640)]
        # t.sort(reverse=True)

        # print(t)

        # pixels = [x[1:] for x in t[:20480]]
        # pickle.dump(pixels, open('pixels.pkl', 'wb'))

        pixels = pickle.load(open('pixels.pkl', 'rb'))
        
        mask = torch.zeros_like(im)
        for x, y in pixels:
            mask[0, :, x, y] = 1
        

        img = mask.detach().permute(0,2,3,1).numpy()[0] * 255
        img = img.round().astype(np.uint8)
        # print(img)
        Image.fromarray(img).save(f'out/mask.png')

        opti = torch.optim.Adam([im], lr=.1)

        for epoch in range(100):
            pred = model(im, augment=augment, visualize=visualize)
            conf = pred[0, :, 4].sum()

            
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

            pr = pred[0].cpu()
            
            print(f'epoch #{epoch}','box置信度总和', conf.detach(), '预测 box 个数', len(pr))

            conf.backward()
            opti.step()

            
            im.data = torch.clamp(im.data, min=0.0, max=1.0)
            im.data = im * mask + clean_img * (1 - mask)
            im.grad.zero_()

            # print(im.detach())
            pickle.dump(im.detach(), open(f'out/im{epoch}.pkl', 'wb'))
            
            img = im.detach().permute(0,2,3,1).numpy()[0] * 255
            img = img.round().astype(np.uint8)
            # print(img)
            Image.fromarray(img).save(f'out/{epoch}.png')


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
```

## 官方解法

AdvDetPatch题目要求选手针对目标检测模型进行对抗攻击，要求模型无法正确地检测出给定图片中的所有物体，并且对抗性补丁的面积不能超过图像面积的5%。

题目考察的是较为基础的针对深度学习任务的对抗性攻击知识。设计攻击方法的关键是设计损失函数与对抗性补丁模板。为了简化流程，题目仅约束补丁面积大小，对补丁的数量不作要求。题目中给出了补丁设计的相关提示即需要考虑补丁的形状、位置、纹理等因素。

首先是用于攻击的损失函数设计。从推理代码中可知预测的输出包含了图像中所有检测框的左上角和左下角的坐标、为物体的概率以及类别的概率向量。为了使得模型检测不到图片中的物体，损失函数可以设计为最小化所有检测框的判断为物体的概率。损失函数的设计需要对预测结果的组成有基本的了解。

损失函数示例如下：

```assembly
def attack_loss(preds):
    """
    Computes the attack loss for object detection.

    Args:
        preds (List[Tensor[N, :]]): List of detection results.

    Returns:
        Tuple[float, int]: Tuple containing the object probability loss and the number of detected objects.
    """
    conf_thres = 0.25
    obj_prob_loss = 0
    objects_num = 0
    for i, pred in enumerate(preds):
        conf_mask = (pred[:, 4] >= conf_thres).squeeze()
        pred = pred[conf_mask]
        obj_prob_loss += (pred[:, 4].sum() / conf_mask.sum())
        objects_num = conf_mask.sum()
    return obj_prob_loss, objects_num
```

其次考虑补丁的位置和形状。对于扰动位置， 与分类模型不同，当扰动处处在图片中的物体区域时对此目标的检测影响最大，而在背景区域时影响很小。因此，扰动可以放置在可能的检测框中心。对于形状，需要保证补丁面积大小不超过全图的5%，因此无法直接添加全局扰动。题目不对补丁数量做要求，因此可选项很多，例如方形、圆形、随机点、网格、星形等等，只要在给定扰动像素数量内尽可能的覆盖物体都可以。

以创建网格形mask为例（即只包含横线和竖线）：

```assembly
def create_patch_mask(detections=None, width=1, line_distance=50, shape=(640,640)):
    """
    Creates a mask over the image where detections are located, with lines drawn at regular intervals.

    Args:
        detections (List[[N, 4]]): List of detections returned by non-maximum suppression, (int).
        width (int): Width of the lines.
        line_distance (int): Distance between the lines.
        shape (Tuple[int, int]): Shape of the output mask.

    Returns:
        Tensor containing the binary mask of the patches.
    """
    mask = torch.zeros(*shape, 3)
    for _, (x1, y1, x2, y2) in enumerate(detections):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        for i in range(1, 100):
            if mask.sum() > 20480*3: break
            if y1 + i*line_distance > y2: break
            tmp_mask = torch.zeros(*shape, 3)
            tmp_mask[np.clip(y1+i*line_distance, 0, shape[1]):np.clip(y1+i*line_distance+width, 0, shape[1]), x1:x2, :]=1
            mask = mask + tmp_mask
        for i in range(1,100):
            if mask.sum() > 20480*3: break
            if x1 + i*line_distance > x2: break
            tmp_mask = torch.zeros(*shape, 3)
            tmp_mask[y1:y2, np.clip(x1+i*line_distance, 0, shape[1]):np.clip(x1+i*line_distance+width, 0, shape[1]), :]=1
            mask = mask + tmp_mask
            
    mask = np.clip(mask,0,1)
    return mask
```

最后可以使用常见的梯度攻击方法如PGD优化补丁的纹理，直到目标检测模型检测不到物体为止。一次循环中的攻击示例如下：

```assembly
# initialize the patch
patch = torch.randn(input_tensor.shape).float() + 127/255  #大初始值加速收敛
patch = patch.to(input_tensor.device)
patch.requires_grad = True
# apply the patch to the image
patch_img = input_tensor * (1-mask) + patch * mask
patch_img = torch.clamp(patch_img,0,1)
patch_img = patch_img.to(device)
# attack
preds = model(patch_img, augment=opt.augment, visualize=opt.visualize)
attack_loss, obj_num = attack_loss(preds)
attack_loss.backward()
patch.data = patch - eps * patch.grad.sign()
```

如果熟悉常见的攻击算法和图像处理能够比较快速地攻击成功，否则补丁的创建和损失的设计都可能会花费较多的时间。补丁的限制只有面积大小，因此补丁的形式非常多，只要能够最大限度地覆盖物体，都能较快的生成扰动。因为只有一张图片，因此肉眼选择补丁的位置并且手工设计mask也能快速确定mask。