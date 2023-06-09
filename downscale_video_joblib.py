# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import argparse
import fnmatch
import glob
import json
import os
import shutil
import subprocess
# from tkinter import Frame
import uuid

from joblib import delayed
from joblib import Parallel
# import pandas as pd

file_src = '/mnt/lustreold/share_data/sunweixuan/video_data/kinect400/train.csv'
folder_path = '/mnt/lustreold/share_data/sunweixuan/video_data/kinect400/train/'
output_path = '/mnt/lustreold/share_data/sunweixuan/video_data/kinect400/train256/'


# file_src = '/vallist.txt'
# folder_path = 'YOUR_DATASET_FOLDER/val/'
# output_path = 'YOUR_DATASET_FOLDER/val_256/'


file_list = []

f = open(file_src, 'r')

for line in f:
    rows = line.split()
    fname = rows[0]
    file_list.append(fname)
    # print(fname)

f.close()


def downscale_clip(inname, outname):

    status = False
    inname = '"%s"' % inname
    outname = '"%s"' % outname
    command = "ffmpeg  -loglevel panic -i {} -filter:v scale=\"trunc(oh*a/2)*2:256\" -q:v 1 -c:a copy {}".format( inname, outname)
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        return status, err.output

    status = os.path.exists(outname)
    return status, 'Downscaled'


def downscale_clip_wrapper(row):
    print(row)
    name =  row.split('/')[-1]

    # nameset  = row.split('/')
    # videoname = nameset[-1]
    # classname = nameset[-2]

    # output_folder = 

    # output_folder = output_path + classname
    # if os.path.isdir(output_folder) is False:
    #     try:
    #         os.mkdir(output_folder)
    #     except:
    #         print(output_folder)
    output_folder = output_path

    inname = row
    outname = output_path + '/' + name

    downscaled, log = downscale_clip(inname, outname)
    return downscaled


status_lst = Parallel(n_jobs=16)(delayed(downscale_clip_wrapper)(row) for row in file_list)