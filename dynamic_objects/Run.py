"""
Images must be in ./Kitti/testing/image_2/ and camera matricies in ./Kitti/testing/calib/

Uses YOLO to obtain 2D box, PyTorch to get 3D box, plots both

SPACE bar for next image, any other key to exit
"""
import json
from torch_lib.Dataset import *
from library.Math import *
from library.Plotting import *
from torch_lib import Model, ClassAverages
from yolo.yolo import cv_Yolo

import os
import time

import numpy as np
import cv2

import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision.models import vgg

import argparse
torch.device('cpu')

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser()

parser.add_argument("--image-dir", default="eval/image_2/",
                    help="Relative path to the directory containing images to detect. Default \
                    is eval/image_2/")

# TODO: support multiple cal matrix input types
parser.add_argument("--cal-dir", default="camera_cal/",
                    help="Relative path to the directory containing camera calibration form KITTI. \
                    Default is camera_cal/")

parser.add_argument("--video", action="store_true",
                    help="Weather or not to advance frame-by-frame as fast as possible. \
                    By default, this will pull images from ./eval/video")

parser.add_argument("--show-yolo", action="store_true",
                    help="Show the 2D BoundingBox detecions on a separate image")

parser.add_argument("--hide-debug", action="store_true",
                    help="Supress the printing of each 3d location")


def plot_regressed_3d_bbox(img, cam_to_img, box_2d, dimensions, alpha, theta_ray, img_2d=None):

    # the math! returns X, the corners used for constraint
    location, X = calc_location(dimensions, cam_to_img, box_2d, alpha, theta_ray)

    orient = alpha + theta_ray

    if img_2d is not None:
        plot_2d_box(img_2d, box_2d)

    plot_3d_box(img, cam_to_img, orient, dimensions, location) # 3d boxes

    return location

def main():


    FLAGS = parser.parse_args()

    # load torch
    weights_path = os.path.abspath(os.path.dirname(__file__)) + '/weights'
    model_lst = [x for x in sorted(os.listdir(weights_path)) if x.endswith('.pkl')]
    if len(model_lst) == 0:
        print('No previous model found, please train first!')
        exit()
    else:
        print('Using previous model %s'%model_lst[-1])
        my_vgg = vgg.vgg19_bn(pretrained=True)
        # TODO: load bins from file or something
        model = Model.Model(features=my_vgg.features, bins=2) #.cuda()
        checkpoint = torch.load(weights_path + '/%s'%model_lst[-1], map_location=torch.device('cpu'))
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()

    # load yolo
    yolo_path = os.path.abspath(os.path.dirname(__file__)) + '/weights'
    yolo = cv_Yolo(yolo_path)

    averages = ClassAverages.ClassAverages()

    # TODO: clean up how this is done. flag?
    angle_bins = generate_bins(2)

    image_dir = FLAGS.image_dir
    # out_dir = 
    cal_dir = FLAGS.cal_dir
    if FLAGS.video:
        if FLAGS.image_dir == "eval/image_2/" and FLAGS.cal_dir == "camera_cal/":
            image_dir = "eval/video/2011_09_26/image_2/"
            cal_dir = "eval/video/2011_09_26/"


    img_path = os.path.abspath(os.path.dirname(__file__)) + "/" + image_dir
    # using P_rect from global calibration file
    calib_path = os.path.abspath(os.path.dirname(__file__)) + "/" + cal_dir
    calib_file = calib_path + "calib_cam_to_cam.txt"

    # using P from each frame
    # calib_path = os.path.abspath(os.path.dirname(__file__)) + '/Kitti/testing/calib/'

    try:
        ids = [x.split('.')[0] for x in sorted(os.listdir(img_path))]
    except:
        print("\nError: no images in %s"%img_path)
        exit()

    for img_id in ids:

        start_time = time.time()

        img_file = img_path + img_id + ".png"

        # P for each frame
        # calib_file = calib_path + id + ".txt"
        # dim = (2048, 1024)

        truth_img = cv2.imread(img_file)
        # truth_img = cv2.resize(truth_img, dim, interpolation = cv2.INTER_AREA)
        img = np.copy(truth_img)
        yolo_img = np.copy(truth_img)

        detections = yolo.detect(yolo_img)
        locations = []
        # print(detections.box_2d)

        for detection in detections:
            # print(detection.box_2d[1][0])


            if not averages.recognized_class(detection.detected_class):
                continue

            # this is throwing when the 2d bbox is invalid
            # TODO: better check
            try:
                detectedObject = DetectedObject(img, detection.detected_class, detection.box_2d, calib_file)
            except:
                continue

            theta_ray = detectedObject.theta_ray
            input_img = detectedObject.img
            proj_matrix = detectedObject.proj_matrix
            box_2d = detection.box_2d
            detected_class = detection.detected_class

            input_tensor = torch.zeros([1,3,224,224]) #.cuda()
            input_tensor[0,:,:,:] = input_img

            [orient, conf, dim] = model(input_tensor)
            orient = orient.cpu().data.numpy()[0, :, :]
            conf = conf.cpu().data.numpy()[0, :]
            # print(conf.shape[0])
            dim = dim.cpu().data.numpy()[0, :]

            dim += averages.get_item(detected_class)

            argmax = np.argmax(conf)
            orient = orient[argmax, :]

            cos = orient[0]
            sin = orient[1]
            alpha = np.arctan2(sin, cos)
            alpha += angle_bins[argmax]
            # alpha = np.radtodeg(alpha)
            # print(alpha)
            cam_to_img = proj_matrix
            fx = cam_to_img[0][0]
            u0 = cam_to_img[0][2]
            v0 = cam_to_img[1][2]


            alpha -= np.pi
            print(alpha)
        #     xmin = detection.box_2d[0][0]
        #     xmax = detection.box_2d[1][0]
        #     box2d_center_x = (xmin + xmax) / 2.0
        # # Transfer arctan() from (-pi/2,pi/2) to (0,pi)
        #     theta_ray = np.arctan(fx /(box2d_center_x - u0))
        #     if theta_ray<0:
        #         theta_ray = theta_ray+np.pi

        #     # max_anc = np.argmax(prediction[2][0])
        #     # anchors = prediction[1][0][max_anc]


        #     if orient[1] > 0:
        #         angle_offset = np.arccos(orient[0])
        #     else:
        #         angle_offset = -np.arccos(orient[0])

        #     bin_num = conf.shape[0]
        #     wedge = 2. * np.pi / bin_num
        #     theta_loc = angle_offset + argmax * wedge

        #     theta = theta_loc + theta_ray
        #     # object's yaw angle
        #     yaw = np.pi/2 - theta
        #     print(yaw)

            if FLAGS.show_yolo:
                location = plot_regressed_3d_bbox(img, proj_matrix, box_2d, dim, alpha, theta_ray, truth_img)
            else:
                location = plot_regressed_3d_bbox(img, proj_matrix, box_2d, dim, alpha, theta_ray)

            def float_toint(lis):
                for item in range(len(lis)):
                    
                    lis[item] = lis[item]
                return(lis)


            # if not FLAGS.hide_debug:
                # print('Estimated pose: %s'%location)
            location = float_toint(location) 
            dim = float_toint(dim)
            location = np.append(location, dim)
            location = location.tolist()

            
            # location.append(theta_ray)
            
            location.insert(0, detection.detected_class)
            if location[0] == "pedestrian":
                location[0] = "person"

                zrot = 0
                xrot = 0
                location.append(xrot)

                location.append(np.rad2deg(alpha + theta_ray))
                

                location.append(zrot)
            elif location[0] == "car":
                yrot = 0
                xrot = -90
                location.append(xrot)

                location.append(yrot)
                location.append(np.rad2deg(-(alpha + theta_ray))- 270)

            print(location)
            location[3] = -location[3]
            location[2] = 1.2
            locations.append(location)


        if os.path.exists( image_dir + '../Results'):
            pass
        else:
            os.makedirs(image_dir + '../Results')

        results_dir = image_dir + '../Results/'

        fname = img_id + '.txt'

        file = os.path.join(results_dir, fname)

        textfile = open(file, "a")
        textfile.seek(0)
        textfile.truncate(0)
        textfile.write(json.dumps("label x y z xscale yscale zscale xrot yrot zrot").replace('"', ''))
        textfile.write("\n")
            
        
        for location in locations:

            if (location == None):
                pass
            
            # item = 0
            # while item in range(len(location)):
            else :
                for item in range(len(location)) :
            
                
                    textfile.write(json.dumps(location [item]).replace('"', ''))
                    if(item < (len(location)-1)):
                        textfile.write(" ")
                    else:
                        break

            # textfile.write(" ")

            textfile.write("\n")
        # with open(file, 'w') as f:
        #     for loc in locations:
        #         string = " %s %f %f %f %f %f %f %f %f %f %f %f %f" % \
        #             (loc[0], loc[1] ,loc[2], loc[3], loc[4], loc[5], loc[7] )
        #         print(string, file=f)
        # import json
        # for line in locations:
        #     for item in line:
        #     # outgroup.write(item)
        #         appendEOL = False
        #         json.dump(item + ' ', open(file,"a+"))
    #     def format(value):
    #         return "%.3f" % value
    #     def append_multiple_lines(file_name, lines_to_append):
    # # Open the file in append & read mode ('a+')
    #         with open(file_name, "a+") as file_object:
    #             appendEOL = False
    #             # Move read cursor to the start of file.
    #             file_object.seek(0)
    #             # Check if file is not empty
    #             data = file_object.read(100)
    #             if len(data) > 0:
    #                 appendEOL = True
    #             # Iterate over each string in the list
    #             for line in lines_to_append:
    #                 # If file is not empty then append '\n' before first line for
    #                 # other lines always append '\n' before appending line
    #                 if appendEOL == True:
    #                     file_object.write("\n")
    #                 else:
    #                     appendEOL = True
    #                 # Append element at the end of file
    #                 file_object.write(str(locations))

    #                 file_object.close()
    #     append_multiple_lines(file, locations)



            

            # print(theta_ray, alpha)
        # new_file=open("newfile.txt",mode="a+",encoding="utf-8")
        # new_file.writelines(fruits)
        # for line in new_file:
        #     print(line)
        # new_file.close()
        height = 1024
        width = 2048
        bin_h = 512//1024
        bin_w = 1024//2048

        # truth_img = cv2.resize(truth_img, dim, interpolation = cv2.INTER_AREA)
        # img = img.reshape((height,
        #                            width, 3)).max(3).max(1)

        if FLAGS.show_yolo:
            numpy_vertical = np.concatenate((truth_img, img), axis=0)
            cv2.imshow('SPACE for next image, any other key to exit', numpy_vertical)
        else:
            cv2.imshow('3D detections', img)

        if not FLAGS.hide_debug:
            print("\n")
            print('Got %s poses in %.3f seconds'%(len(detections), time.time() - start_time))
            print('-------------')

        if FLAGS.video:
            cv2.waitKey(1)
        else:
            if cv2.waitKey(0) != 32: # space bar
                exit()

if __name__ == '__main__':
    main()
