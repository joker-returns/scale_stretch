import cv2
import numpy as np
import constants
from PIL import Image
import utils
import matlab_interactor
import matlab.engine
def setMesh(image, mesh_size):
    h = image.shape[0]
    w = image.shape[1]
    quad_num_h = h / mesh_size
    quad_num_w = w / mesh_size

    remaining_h = h - mesh_size*quad_num_h
    remaining_w = w - mesh_size*quad_num_w

    print "[+] vertex set function called and w,h,quad_num_w,quad_num_h,remaining_w,remaining_h are ",w,h,quad_num_w,quad_num_h,remaining_w,remaining_h
    vertex_set = np.zeros((quad_num_h+2,quad_num_w+2,2))
    start_point = 0
    for i in range(0,quad_num_h+2):
        for j in range(0,quad_num_w+2):
            if i == 0:
                vertex_set[i][j][0] = start_point
            else:
                vertex_set[i][j][0] = min(start_point+mesh_size*(i-1)+((i-1)/quad_num_h)*remaining_h,h)

            if j == 0:
                vertex_set[i][j][1] = start_point
            else:
                vertex_set[i][j][1] = min(start_point+mesh_size*(j-1)+((j-1)/quad_num_w)*remaining_w,w)
    return vertex_set

def importance_map_quad(importance_map, vertex_set_org):
    quad_num_h = vertex_set_org.shape[0]-1
    quad_num_w = vertex_set_org.shape[1]-1

    importance_quad = np.zeros((quad_num_h,quad_num_w))

    for i in range(quad_num_h):
        for j in range(quad_num_w):
            v1 = [vertex_set_org[i][j][1],vertex_set_org[i][j][0]]
            v2 = [vertex_set_org[i+1][j+1][1], vertex_set_org[i+1][j+1][0]]
            map = importance_map(max())
    print vertex_set_org.shape
    return vertex_set_org


image = cv2.imread("./images/asd.jpg")
image = cv2.resize(image,(0,0),None,0.5,0.5)
print len(image),len(image[0]),image[0][0]
ratio = 0.5
mesh_size = 20

importance_map = utils.importance_map(image)
print importance_map[0][0],image[0][0]
cv2.imwrite("./images/importance_maps/imp.jpg",importance_map)

# matlab_interactor.doDemo()