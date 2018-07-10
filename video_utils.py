import numpy as np
import cv2
import utils
import matlab_interactor

cap = cv2.VideoCapture("./videos/bob_360p.mkv")
frameNum = 0
frames = []


fps = cap.get(cv2.CAP_PROP_FPS)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
numberOfFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
max_Frames = 1800

height_red = 1.0
width_red = 0.7

final_width = int(width_red*width)
final_height = int(height_red*height)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter("out.avi",fourcc,30.0 ,(final_width,final_height))

print fps,width,height,numberOfFrames,final_width,final_height
videoWriter = cv2.VideoWriter()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    if(frameNum == max_Frames):
        break
    frameNum+=1
    # if(frameNum<1578):
    #     continue

    print "[+] Working with Frame number: {}/{}".format(frameNum, max_Frames)
    # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # utils.showImage(gray,"asd")
    cv2.imwrite("./images/graph/in.jpg", frame)
    matlab_interactor.doDemo(height_red, width_red)
    ip = cv2.imread("./images/graph/out.jpg")
    # print len(ip),len(ip[0]),final_height,final_width


    if len(ip[0]) != final_width or len(ip) != int(height_red*height):
        print "[-]INCORRECT RESOLUTION DETECTED SKIPPING FRAME : Frame Params: {} % {} and Actual Params should be {} and {}".format(len(ip),len(ip[0]), final_height,final_width)
        if(len(ip[0]) != final_width):
            difference = len(ip[0]) - final_width
            print "[-] extra cols {}".format(difference)
            while(difference > 0):
                print "[*] Deleting column"
                ip = np.delete(ip, (len(ip[0]) - 1), axis=1)
                difference = difference-1
        if (len(ip) != final_height):
            difference = len(ip) - final_height
            print "[-] extra cols {}".format(difference)
            while (difference > 0):
                print "[*] Deleting row"
                ip = np.delete(ip, (len(ip) - 1), axis=0)
                difference = difference - 1
        print len(ip), len(ip[0])
        print len(ip), len(ip[0])
    out.write(ip)
    # if(frameNum%50 == 0):
        # print "Saving frame"
        # cv2.imwrite("./useless/frame_"+str(frameNum)+".jpg",frame)
        # break
    # Display the resulting frame
    # cv2.imshow('frame',gray)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break


# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
