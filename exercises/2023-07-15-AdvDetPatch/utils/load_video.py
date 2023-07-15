import cv2
import os
import numpy as np 
from tqdm import tqdm


def video2frame(videos_path,frames_save_path,time_interval):
 
  '''
  :param videos_path: 视频的存放路径
  :param frames_save_path: 视频切分成帧之后图片的保存路径
  :param time_interval: 保存间隔
  :return:
  '''
  vidcap = cv2.VideoCapture(videos_path)
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  print(fps)
  success, image = vidcap.read() # success当image无时返回false
  
  count = 0
  while success:
    count += 1
    # if count % time_interval == 0:
    #   cv2.imencode('.png', image)[1].tofile(frames_save_path + "/frame%d.jpg" % count)
    cv2.imwrite(frames_save_path + "/frame%d.png" % count,image)
    success, image = vidcap.read()
    
    # if count == 20:
    #   break
  print(count)
 
if __name__ == '__main__':
    videos_path = "/public/zhangkui/challenge/aisec/ad_attack/video/town05_none01.mp4"
    frames_save_path = 'frame/person/'+videos_path[:-4].split('/')[-1]
    os.makedirs(frames_save_path,exist_ok=True)
    time_interval = 1#隔一帧保存一次
    video2frame(videos_path, frames_save_path, time_interval)