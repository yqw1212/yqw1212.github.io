
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