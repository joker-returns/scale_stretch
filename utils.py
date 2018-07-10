import cv2
import numpy as np
from deepgaze.saliency_map import FasaSaliencyMapping


def showImage(image, name):
    cv2.imshow(name,image)
    cv2.waitKey(0)

def gradient(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(image, cv2.CV_64F,1,0,ksize=1)
    sx = cv2.convertScaleAbs(sobelx)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=1)
    sy = cv2.convertScaleAbs(sobely)
    sx2y2 = cv2.addWeighted(sx,0.5,sy,0.5,0)
    #cv2.addWeighted()
    return sx2y2

def saliency(image):
    saliency_map = FasaSaliencyMapping(image.shape[0],image.shape[1])
    image_salient_1 = saliency_map.returnMask(image,tot_bins=8, format='BGR2LAB')
    image_salient = cv2.GaussianBlur(image_salient_1,(3,3),1)
    image_salient = cv2.convertScaleAbs(image_salient)
    return image_salient

def importance_map(image):
    gra_img = gradient(image)
    # showImage(gra_img,"grad")
    sal_img = saliency(image)
    # showImage(sal_img,"sal")
    final_img = cv2.convertScaleAbs(gra_img*sal_img)
    return final_img

def main():
    img = cv2.imread("./images/asd.jpg")
    img = cv2.resize(img,(0,0),None,.45,0.45)

    gra_img = gradient(img)
    sal_img = saliency(img)

    final_img = cv2.convertScaleAbs(gra_img*sal_img)
    print "[+] Shape of the image is {} * {}".format(final_img.shape[0],final_img.shape[1])
    numpy_harizontal = np.hstack((gra_img,sal_img))

    cv2.imshow("asd",numpy_harizontal)
    cv2.waitKey(0)
    print "done"

if __name__ == "__main__":
    main()