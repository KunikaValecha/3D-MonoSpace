import cv2
#import matplotlib.pyplot as plt
import numpy as np
img = "/home/kunika/Downloads/000010.png"

img_mat = cv2.imread(img)
mask = cv2.cvtColor(img_mat, cv2.COLOR_BGR2GRAY)
# mask = cv2.resize(mask, (500, 400))

mask[np.where((mask == [16]))] = [255]
mask[np.where((mask != [255]))] = [0]
mask = cv2.resize(mask, (img_mat.shape[1], img_mat.shape[0]))
# _, mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
# output1 = cv2.inpaint(img_matimg_mat, mask, 3, cv2.INPAINT_NS)
# output2 = cv2.inpaint(img_mat, mask, 3, cv2.INPAINT_TELEA)
# # cv2.imshow("o", mask)
# # # print(img_mat.shape)
# # img_mat[np.where((img_mat == [0,0,142]).all(axis=2))] = [0,0,0]
# # # img_mat = cv2.resize(img_mat, (500, 400))

# # # # plt.show()
# cv2.waitKey()

# res_NS = cv2.inpaint(img_mat, mask, 3, cv2.INPAINT_NS)
# res_TELEA = cv2.inpaint(img_mat, mask, 3, cv2.INPAINT_TELEA)
# res_FSRFAST = img_mat.copy()
# res_FSRBEST = img_mat.copy()
# mask1 = cv2.bitwise_not(mask)
# distort = cv2.bitwise_and(img_mat, img_mat, mask=mask1)
# cv2.xphoto.inpaint(distort, mask1, res_FSRFAST,        cv2.xphoto.INPAINT_FSR_FAST)
# cv2.xphoto.inpaint(distort, mask1, res_FSRBEST, cv2.xphoto.INPAINT_FSR_BEST)
# mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
_, mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
mask1 = cv2.bitwise_not(mask)
distort = cv2.bitwise_and(img_mat, img_mat, mask=mask1)

output1 = cv2.inpaint(distort, mask, 3, cv2.INPAINT_NS)
output2 = cv2.inpaint(distort, mask, 3, cv2.INPAINT_TELEA)

restored1 = img_mat.copy()
restored2 = img_mat.copy()
cv2.xphoto.inpaint(distort, mask1, restored1, cv2.xphoto.INPAINT_FSR_FAST)
cv2.xphoto.inpaint(distort, mask1, restored2, cv2.xphoto.INPAINT_FSR_BEST)

dst3 = cv2.cvtColor(restored1, cv2.COLOR_BGR2RGB)
dst4 = cv2.cvtColor(restored2, cv2.COLOR_BGR2RGB)
dst1 = cv2.cvtColor(output1, cv2.COLOR_BGR2RGB)
dst2 = cv2.cvtColor(output2, cv2.COLOR_BGR2RGB)
dst = cv2.cvtColor(distort, cv2.COLOR_BGR2RGB)
img1 = cv2.cvtColor(img_mat, cv2.COLOR_BGR2RGB)

# plt.figure(figsize=(15, 20))
# plt.subplot(2, 3, 1)
# plt.imshow(img1)
# plt.subplot(2, 3, 2)
# plt.imshow(dst)
# plt.subplot(2, 3, 3)
cv2.imwrite("/home/kunika/Downloads/dst1.png", dst1)
cv2.imwrite("/home/kunika/Downloads/dst2.png", dst2)
# plt.subplot(2, 3, 4)
# cv2.imshow("o", dst2)
cv2.waitKey()
# plt.subplot(2, 3, 5)
# plt.imshow(dst3)
# plt.subplot(2, 3, 6)
# plt.imshow(dst4)
