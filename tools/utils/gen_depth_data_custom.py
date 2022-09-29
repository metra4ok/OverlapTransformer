#!/usr/bin/env python3
# Developed by Xieyuanli Chen and Thomas Läbe
# This file is covered by the LICENSE file in the root of the project OverlapNet:
#https://github.com/PRBonn/OverlapNet

# Brief: кастомная версия скрипта для работы с данными от сканера Velodyne VLP-32C

import os
from utils import load_files
import numpy as np
import open3d as o3d
from utils import range_projection

import cv2
try:
    from utils import *
except:
    from utils import *

import scipy.linalg as linalg
def rotate_mat( axis, radian):
    rot_matrix = linalg.expm(np.cross(np.eye(3), axis / linalg.norm(axis) * radian))
    return rot_matrix
    # print(type(rot_matrix))



def gen_depth_data(scan_folder, dst_folder, normalize=False):
    """ Generate projected range data in the shape of (64, 900, 1).
      The input raw data are in the shape of (Num_points, 3).
  """
    # specify the goal folder
    try:
        os.stat(dst_folder)
        print('generating depth data in: ', dst_folder)
    except:
        print('creating new depth folder: ', dst_folder)
        os.mkdir(dst_folder)

    # load LiDAR scan files
    scan_paths_raw = load_files(scan_folder)
    scan_paths = []
    for filename in scan_paths_raw:
        if filename.endswith('.pcd'):
            scan_paths.append(filename)

    depths = []
    axis_x, axis_y, axis_z = [1,0,0], [0,1,0], [0, 0, 1]

    # iterate over all scan files
    for filename in scan_paths:
        # load a point cloud
        # экспортированные из cyber record файла данные имеют формат pcd
        pcd = o3d.io.read_point_cloud(filename)
        current_vertex = np.asarray(pcd.points)
        current_vertex = np.hstack([current_vertex, np.zeros_like(current_vertex)])

        # параметры лидара (найдены в интернете):
        # vertical FoV = 40 degree  TODO: how to split into FoV_up and FoV_down ???
        # channels = 32
        # max range = 200 m
        proj_range, _, _, _ = range_projection(current_vertex,
                                               fov_up=20, fov_down=20,
                                               proj_H=32,
                                               max_range=200)  # proj_ranges   from larger to smaller

        # normalize the image
        if normalize:
            proj_range = proj_range / np.max(proj_range)

        # generate the destination path
        num = int(filename.split('.')[0].split('/')[-1])
        new_name = str(num).zfill(6)
        dst_path = os.path.join(dst_folder, new_name)

        # np.save(dst_path, proj_range)
        png_filename = dst_path + ".png"
        cv2.imwrite(png_filename, proj_range)
        print('finished generating depth data at: ', png_filename)

    return depths


if __name__ == '__main__':
    scan_folder = '/home/docker_overlaptransformer/Datasets/Integrant_Apollo_CyberBags/2022-09-27_loosing_gps_pcds/02'
    dst_folder = '/home/docker_overlaptransformer/Datasets/Integrant_Apollo_CyberBags/2022-09-27_loosing_gps_pcds/02/range_images'

    depth_data = gen_depth_data(scan_folder, dst_folder)
