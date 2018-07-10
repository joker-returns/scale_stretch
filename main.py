import cv2
import numpy as np
import utils
np.set_printoptions(threshold=np.nan)

def videoInfo(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    numberOfFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    print "Resolution {} * {}. FPS: {}, Number of frames: {}".format(int(width),int(height), fps, numberOfFrames)

def mark(contributors, img):
    # for i in range(len(contributors)):
    #     grad[i][contributors[i]] = 255
    # utils.showImage(grad,"after")
    rows = len(img)
    cols = len(img[0])
    newimg = np.zeros((rows,cols-1,3),dtype=np.uint8)
    print "Starting seam removal"
    for i in range(rows):
        for j in range(cols):
            if(j == contributors[i]):
                continue
            else:
                if(j > contributors[i]):
                    newimg[i][j-1] = img[i][j]
                else:
                    newimg[i][j] = img[i][j]
    print "Done with removing seam"
    return newimg

def remove(img, grad):
    rows = len(img)
    cols = len(img[0])
    print img[0][0],grad[0][0]
    final = []
    for i in range(rows):
        final.append([])
        for j in range(cols):
            if i == 0:
                final[i].append(int(grad[i][j]))
            else:
                if j == 0:
                    final[i].append(min(final[i-1][0],final[i-1][1])+int(grad[i][0]))
                elif j == cols-1:
                    final[i].append(min(final[i - 1][cols-1], final[i - 1][cols-2])+int(grad[i][cols-1]))
                else:
                    final[i].append(min(final[i - 1][j], final[i - 1][j-1], final[i - 1][j+1]) + int(grad[i][j]))
    contributors = []
    minEnergyINdex = final[rows-1].index(min(final[rows-1]))
    contributors.insert(0, minEnergyINdex)
    for i in range(1,rows):
        if minEnergyINdex == 0:
            if(final[rows-1-i][0] > final[rows-1-i][1]):
                contributors.insert(0,1)
            else:
                contributors.insert(0,0)
        elif minEnergyINdex == cols-1:
            if (final[rows - 1 - i][cols-1] > final[rows - 1 - i][cols-2]):
                contributors.insert(0,cols-2)
            else:
                contributors.insert(0,cols-1)
        else:
            j = contributors[0]
            l = final[rows-1-i][j-1]
            c = final[rows-1-i][j]
            r = final[rows-1-i][j+1]
            if(l < r):
                if(l < c):
                    contributors.insert(0,j-1)
                else:
                    contributors.insert(0, j)
            else:
                if(r < c):
                    contributors.insert(0, j +1)
                else:
                    contributors.insert(0, j )
    print min(final[rows-1]),len(contributors)
    # total = 0
    # for i in range(len(contributors)):
    #     total += grad[i][contributors[0]]
    # print total
    # mark(contributors,img,grad)
    return contributors

def total(x,y, fi,rc,m):
    print x,y,"IIIIII"
    fin = 0
    # print np.shape(fi[361])
    # print np.shape(rc[361])

    print imageInfo(fi)
    print imageInfo(rc)
    try:
        for i in range(x):
            fin += (fi[i][y]-rc[i][y])*(fi[i][y]-rc[i][y])
        if(x+1 < m):
            for i in range(x+1,m):
                fin += (fi[i][y] - rc[i-1][y])*(fi[i][y] - rc[i-1][y])
    except:
        print "Fucking exception God knows why"
    return fin

def compute_tcoherence(images):
    grad_images = []
    contributors = []
    coherences = []
    spatial_coherence = []
    # width = len(images[0][0])
    # height = len(images[0])
    rows,cols,ch = np.shape(images[0])
    print rows,cols
    print "Computing gradients of {} images".format(len(images))
    for image in images:
        grad_images.append(utils.gradient(image))
    print "Computed gradients of {} images".format(len(grad_images))
    first_frame = remove(images[0],grad_images[0])
    contributors.append(first_frame)
    coherences.append(grad_images[0])
    spatial_coherence.append()
    for i in range(1,len(images)):
        coherences.append([])
        spatial_coherence.append([])
        rc = mark(contributors[i - 1], images[i])
        rc_grad = utils.gradient(rc)
        for x in range(rows):
            coherences[i].append([])
            for y in range(cols):
                print "Computinf energy for {},{} of image number {}".format(x,y,i)
                coherences[i][x].append(total(x,y,grad_images[i],rc_grad,rows))
        print np.shape(coherences[i])




def imageInfo(img):
    return [len(img[0]), len(img)]

cap = cv2.VideoCapture("./videos/pit.mkv")
frameCTR= 0
images = []
numberOfFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
while True:
    ret, frame = cap.read()
    frameCTR += 1
    if not ret:
        break
    images.append(frame)
    print "Frame dims are {} * {} and frame number is {}/{}".format(imageInfo(frame)[0],imageInfo(frame)[1],frameCTR,numberOfFrames)
    if frameCTR%10 == 2:
        # saliency = utils.saliency(frame)
        grad = utils.gradient(frame)
        # utils.showImage(grad,"saliency")
        # remove(frame,grad)
        compute_tcoherence(images)
        break



print frameCTR