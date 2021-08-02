import cv2 
import numpy as np
from scipy.spatial import distance 
import imutils
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import sys

file = r"/home/kunika/Downloads/kitti_deeplab-master/image_2segmented_images/000022_10.png"
# file = r"/home/kunika/Downloads/kitti_deeplab-master/test_final/straight_roadssegmented_images"
# segmented_dir = sys.argv[1]
font = cv2.FONT_HERSHEY_COMPLEX 

image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

# image = cv2.imshow("op", image)
# cv2.waitKey(100000)
# # print(image)

image[np.where((image == [0]))] = [255]
image[np.where((image != [255]))] = [0]
# image[np.where((image != [128,64,128]))] = [255]
# cv2.imshow("op",image)
# cv2.waitKey(10000)


# cv2.imshow("op", image)
# cv2.waitKey(10000)




# mask = image == 0
# image[mask] = 0
# image[np.logical_not(mask)] = 255
# cv2.imshow("op", image)
# cv2.waitKey(10000)

_, threshold = cv2.threshold(image, 110, 255, cv2.THRESH_BINARY) 

# cv2.imshow("op", threshold)

# cv2.waitKey(100000)

# D = ndimage.distance_transform_edt(threshold)
# print(D)
# localMax = peak_local_max(D, indices=False, min_distance=20,
# 	labels=threshold)
# print(localMax)
# markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
# labels = watershed(-D, markers, mask=threshold)
# print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))


# for label in np.unique(labels):
# 	# if the label is zero, we are examining the 'background'
# 	# so simply ignore it
# 	# if label == 0:
# 	# 	continue
# 	# otherwise, allocate memory for the label region and draw
# 	# it on the mask
# 	mask = np.zeros(gray.shape, dtype="uint8")
# 	mask[labels == label] = 255

	# contours, _= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# contours = imutils.grab_contours(contours)
	# c = max(contours, key=cv2.contourArea)

	# extLeft = tuple(c[c[:, :,0].argmin()][0])
	# extRight = tuple(c[c[:, :,0].argmax()][0])
	# extTop = tuple(c[c[:, :,1].argmin()][0])
	# extBot = tuple(c[c[:, :,1].argmax()][0])

	# cv2.drawContours(image, [c], -1, (128, 128, 128), 2)
	# cv2.circle(image, extLeft, 8, (128, 64, 128), -1)
	# cv2.circle(image, extRight, 8, (128, 64, 128), -1)
	# cv2.circle(image, extTop, 8, (128, 64, 128), -1)
	# cv2.circle(image, extBot, 8, (128, 64, 128), -1)

	# cv2.imshow("Image", image)
	# cv2.waitKey(100000000)




# print (threshold)
# cv2.imshow("op", threshold)

contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

# items = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# cnts = contours[0] 
# print(cnts)

# cnts = imutils.grab_contours(contours)
c = max(contours, key=cv2.contourArea)
# print(c)



# print(c)

arr = []
coor_x =[]
coor_y = []

# for cnt in contours : 
# 	# print(cnt)
  
#     approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 
#     print(len(cnt))
  
#     # draws boundary of contours. 
#     cv2.drawContours(image, [approx], 0, (0, 0, 255), 5)  
  
#     # Used to flatted the array containing 
#     # the co-ordinates of the vertices. 
#     n = approx.ravel()  
#     i = 0
  
#     for j in n : 
#         if(i % 2 == 0): 
#             x = n[i] 
#             y = n[i + 1] 

#             coor_x.append(x)
#             coor_y.append(y)
  
#             # String containing the co-ordinates. 
#             string = str(x) + " " + str(y)
#             arr.append(string)  

  
#             if(i == 0): 
#                 # text on topmost co-ordinate. 
#                 cv2.putText(image, "Arrow tip", (x, y), 
#                                 font, 0.5, (255, 0, 0))  
#             else: 
#                 # text on remaining co-ordinates. 
#                 cv2.putText(image, string, (x, y),  
#                           font, 0.5, (0, 255, 0)) 
             
             

#         i = i + 1
# extLeft = tuple(cnts[cnts[:, :,0].argmin()][0])
# extRight = tuple(cnts[cnts[:, :,0].argmax()][0])
# extTop = tuple(cnts[cnts[:, :,1].argmin()][0])
# extBot = tuple(cnts[cnts[:, :,1].argmax()][0])
# print(extLeft)
# print(extRight)
# print(extTop)
# print(extBot)

extLeft = tuple(c[c[:, :,0].argmin()][0])
extRight = tuple(c[c[:, :,0].argmax()][0])
extTop = tuple(c[c[:, :,1].argmin()][0])
extBot = tuple(c[c[:, :,1].argmax()][0])
print(extLeft)
print(extRight)
print(extTop)
print(extBot)

dist = distance.euclidean(extLeft, extRight)
print(dist)


# cv2.drawContours(image, [cnts], -1, (128, 128, 128), 2)
cv2.drawContours(image, [c], -1, (128, 128, 128), 2)
# cv2.circle(image, extLeft, 8, (128, 64, 128), -1)
# cv2.circle(image, extRight, 8, (128, 64, 128), -1)
# cv2.circle(image, extTop, 8, (128, 64, 128), -1)
# cv2.circle(image, extBot, 8, (128, 64, 128), -1)

cv2.imshow("Image", image)
cv2.waitKey(100000000)

# print(arr)
# print(coor_x)
# print(coor_y)


# distances = []



# cv2.imshow("op", image)
# cv2.waitKey(100000)

# # for i in range(coor_x):
# # 	for j in coor_y:
# # 		# dist = np.sqrt((coor_x[i+1]-coor_x[i])**2)

# # 		dist = distance.euclidean(i, j)
# # 		distances.append(dist)

# for i in range arr 

# print(distances)
# max = np.max(distances)
# print(max)



# # print(image)