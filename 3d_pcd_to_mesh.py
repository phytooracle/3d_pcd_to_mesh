#!/usr/bin/env python3
"""
Author : Emmanuel Gonzalez
Date   : 2020-12-08
Purpose: Convert point cloud (PLY format) to mesh
"""

import argparse
import os
import sys
import open3d as o3d
import numpy as np
import multiprocessing


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Point cloud to mesh',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        nargs='+',
                        metavar='file',
                        help='Point cloud file (PLY format only)')

    parser.add_argument('-a',
                        '--alpha',
                        help='Alpha for Poisson surface reconstruction',
                        metavar='alpha',
                        type=float,
                        default=0.01)

    parser.add_argument('-v',
                        '--voxel_size',
                        help='Voxel size for downsampling',
                        metavar='voxel_size',
                        type=float,
                        default=0.05)

    parser.add_argument('-sc',
                        '--surface_color',
                        help='Surface color',
                        metavar='color',
                        type=str,
                        choices=['R', 'G', 'B'])

    parser.add_argument('-d',
                        '--depth',
                        help='Depth of the octree, i.e. resolution',
                        metavar='depth',
                        default=9)

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        default='pcd_to_mesh_out')

    parser.add_argument('-c',
                        '--cpu',
                        help='CPU number for multiprocessing',
                        type=int,
                        required=True)

    return parser.parse_args()


# --------------------------------------------------
def open_downsample_pcd(pcd_path):
    args = get_args()

    pcd = o3d.io.read_point_cloud(pcd_path)
    pcd.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
    pcd.estimate_normals()

    downpcd = pcd.voxel_down_sample(voxel_size=args.voxel_size)

    return downpcd


def surface_reconstruction(downpcd):
    args = get_args()

    print(f'Running Poisson surface reconstruction for {args.file}.')

    colors = {
            'R': [255, 0, 0],
            'G': [0, 255, 0],
            'B': [0, 0, 255]
            }

    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            downpcd, depth=args.depth)

    print(colors.get(args.surface_color))
    mesh = mesh.paint_uniform_color(str(colors.get(args.surface_color)))
    #o3d.visualization.draw_geometries([mesh])

    return mesh


# --------------------------------------------------
def process_pcd(pcd_path):
    args = get_args()

    f_name = os.path.basename(pcd_path)
    out_path = os.path.join(args.outdir, f_name).replace('.ply', '_mesh.ply')

    downpcd = open_downsample_pcd(pcd_path)
    mesh = surface_reconstruction(downpcd)
    o3d.io.write_triangle_mesh(out_path, mesh)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    with multiprocessing.Pool(args.cpu) as p:
        p.map(process_pcd, args.file)


# --------------------------------------------------
if __name__ == '__main__':
    main()
