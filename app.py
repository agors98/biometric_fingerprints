from image_enhance import image_enhance
from matplotlib import pyplot as plt
import numpy as np
from skimage.morphology import skeletonize
import skimage
data_vector = []

def imagepreproces(img):
    image = image_enhance(img)
    image_skel = skeletonize(image)
    minutiaes_radar(image_skel)

def minutiaes_radar(img):
    width,height = img.shape
    img = np.array(img,dtype=np.int)
    x_position = []
    y_position = []
    type_minutiaes = []
    for i in range(1,width-1):
        for j in range(1,height-1):
            minutiae = matrix_search(img,i,j)
            if minutiae != 2:
                x_position.append(i)
                y_position.append(j)
                type_minutiaes.append(minutiae)
    x_corr,y_corr,typeMi = remove_misguided(img, x_position, y_position,type_minutiaes)
    draw_point(img,x_corr,y_corr,typeMi)
    
def draw_point(img,x,y,t):
    width,height = img.shape
    img = img*255
    color_circle = " "
    Img_show = np.zeros((width,height, 3), np.uint8)
    Img_show[:, :, 0] = img
    Img_show[:, :, 1] = img
    Img_show[:, :, 2] = img
    for i in range(len(x)):
        if t[i] ==0:
            color_circle = (189,236,182)
        else:
            color_circle = (254,0,0)
        (rr, cc) = skimage.draw.circle_perimeter(x[i], y[i],4)
        skimage.draw.set_color(Img_show, (rr, cc), color_circle)
    plt.imshow(Img_show,'gray')
    plt.show()

def matrix_search(img,i,j):
    coordinates = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    extract = [img[i + k][j + l] for k, l in coordinates]
    proceedings = 0
    for k in range(len(extract)-1):
        proceedings += abs(extract[k] - extract[k + 1])
    if img[i][j] == 1:
        if proceedings / 2 == 1:
            return 0
        if proceedings / 2 == 3:
            return 1
    return 2

def remove_misguided(img,x,y,typeM):
    rem_num = []
    x_corr = []
    y_corr = []
    typeMi = []
    treshold = treshold_search(img)
    for i in range(len(x)-1):
        for j in range(i):
            distanse = np.sqrt((x[j]-x[i])**2+(y[j]-y[i])**2)
            if distanse< treshold:
                rem_num.append(i)
                rem_num.append(j)
    rem_num = list(tuple(rem_num))
    for k in range(len(x)):
        if not k in rem_num:
            x_corr.append(x[k])
            y_corr.append(y[k])
            typeMi.append(typeM[k])
            data_vector.extend([typeM[k],x[k],y[k]])
    return x_corr,y_corr,typeMi
            
            
    
def treshold_search(img):
    width,height = img.shape
    near_point = []
    for i in range(int(width/10),int(width-width/10)):
        for j in range(int(width/10),int(height-width/10)):
            if img[i][j]==1:
                for k in range(1,int(width/10)):
                    if img[i+k][j]==1:
                        near_point.append(k)
                        break
                    elif img[i-k][j]==1:
                        near_point.append(k)
                        break
    treshold = np.mean(near_point)
    return treshold
    


