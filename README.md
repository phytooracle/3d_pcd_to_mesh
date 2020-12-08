# 3D PCD to Mesh

Takes in a point cloud data set (PCD), and outputs a single mesh connecting all vertices from the PCD.

## Inputs

One or more PCD's.

## Outputs

One or more meshes.

## Arguments and Flags
* **Positional Arguments:**
    * **Point cloud file (PLY format only):** 'file', nargs= '+'
* **Required Arguments:**
    * **CPU number for multiprocessing:** '-c'
* **Optional Arguments:**
    * **Alpha for Poisson surface reconstruction:** '-a', default = 0.01
    * **Voxel size for downsampling:** '-v', default = 0.05
    * **Surface color:** '-sc', choices= ['R','G', 'B']
    * **Depth of the octree, i.e. resolution:** '-d', default = 9
    * **Output directory:** '-o', default = 'pcd_to_mesh_out'
