import numpy as np

calib_f = "/home/kunika/3D-BoundingBox/eval/calib/calib_cam_to_cam.txt"

depth = "/home/kunika/Downloads/3D-BoundingBox/eval/image_2/000000_dep.txt"
inp = np.array(np.loadtxt(depth, skiprows = 0)).astype(float)



print(inp.shape)

def get_P(cab_f):
    for line in open(cab_f):
        if 'P_rect_02' in line:
            cam_P = line.strip().split(' ')
            cam_P = np.asarray([float(cam_P) for cam_P in cam_P[1:]])
            return_matrix = np.zeros((3,4))
            return_matrix = cam_P.reshape((3,4))
            return return_matrix

c = get_P(calib_f)
print(c)


pts_2d = [761,198]
pts_depth = inp[int(pts_2d[1]), int(pts_2d[0])]
print(pts_depth)

x = -pts_depth / 707.53 * (pts_2d[0] - c[0,2]) 
print(x)
y = -pts_depth / 707.53 * (pts_2d[1] - c[1,2]) 
print(y)
# z = depth(x_d,y_d)

# w = np.dot(inv(c), np.array([[pts_2d[0]*pts_depth], [pts_2d[1]*pts_depth], [pts_depth]]))

# print(w)


