#!/usr/bin/env python 
import sys
import os
import time
import subprocess as sp
import itertools
## CV
import cv2
## Model
import numpy as np
import tensorflow as tf
## Tools
import utils
## Parameters
import params ## you can modify the content of params.py

## Test epoch
epoch_ids = [10]
## Load model
model = utils.get_model()

## Preprocess
def img_pre_process(img):
    """
    Processes the image and returns it
    :param img: The image to be processed
    :return: Returns the processed image
    """
    ## Chop off 1/3 from the top and cut bottom 150px(which contains the head of car)
   # shape = img.shape
   # img = img[-350:-180,200:-200]
    ## Resize the image
   # img = cv2.resize(img, (params.FLAGS.img_w, params.FLAGS.img_h), interpolation=cv2.INTER_AREA)
    ## Return the image sized as a 4D array
    # return img[80:-30,30:-30]
 
    return cv2.resize(img[350:-50],(224,64),interpolation=cv2.INTER_CUBIC)


## Process video
for epoch_id in epoch_ids:
    print('---------- processing video for epoch {} ----------'.format(epoch_id))
    vid_path = utils.join_dir(params.data_dir, 'epoch{:0>2}_front.mkv'.format(epoch_id))
    assert os.path.isfile(vid_path)
    frame_count = utils.frame_count(vid_path)
    cap = cv2.VideoCapture(vid_path)

    machine_steering = []

    print('performing inference...')
    time_start = time.time()

    image = []
    for frame_id in range(frame_count):
        ret, img = cap.read()
        assert ret
        ## you can modify here based on your model
        img = img_pre_process(img)
        image.append(img)
    cap.release()  

    image = np.array(image)
    # deg = float(model.predict(np.array([img]), batch_size=1))
    print('image shape is {}'.format(image.shape))
    machine_steering = model.predict(image)

    

    fps = frame_count / (time.time() - time_start)
    
    print('completed inference, total frames: {}, average fps: {} Hz'.format(frame_count, round(fps, 1)))
    
    print('performing visualization...')
    utils.visualize(epoch_id, machine_steering, params.out_dir,
                        verbose=True, frame_count_limit=None)