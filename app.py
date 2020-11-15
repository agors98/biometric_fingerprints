from image_enhance import image_enhance
import numpy as np
from skimage.morphology import skeletonize
import skimage
import numpy 
import math

def imagepreproces(img):
    image = image_enhance(img)
    image_skel = skeletonize(image)
    return_img, vetor_features = minutiaes_radar(image_skel)
    return return_img, vetor_features

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
    orientation_T, orientation_B = get_orient(img,x_corr,y_corr,typeMi)
    return_img = draw_point(img,x_corr,y_corr,typeMi)
    vetor_features = get_vectors(x_corr,y_corr,typeMi,orientation_T, orientation_B)
    return return_img, vetor_features

def get_vectors(x_corr,y_corr,typeMi,T, B):
    vector = "Wyniki są przedstawione w wektorze,\n który zawiera informacje:\n- współrzędna x\n- współrzędna y\n- typ: 0 - zakończenie; 1 - rozwidlenie\n- orientacja punktu \n\n"
    indexT = 0
    indexB = 0
    for i in range(len(x_corr)):
        if typeMi[i] == 0:
            vector+="["+str(x_corr[i])+","+str(y_corr[i])+","+str(typeMi[i])+","+str(T[indexT])+"]"+"\n"
            indexT+=1
        elif typeMi[i] == 1:
            vector+="["+str(x_corr[i])+","+str(y_corr[i])+","+str(typeMi[i])+","+str(B[indexB])+"]"+"\n"
            indexB+=1
    return vector

def get_orient(img,x,y,typeM):
    B_corr = []
    T_corr = []
    for i in range(len(typeM)):
        if typeM[i] == 0:
            T_corr.append([x[i],y[i]])
        else:
            B_corr.append([x[i],y[i]])
    angle_T = get_angle(img,T_corr,0)
    angle_B = get_angle(img,B_corr,1)
    return angle_T, angle_B

def get_angle(img,corr,T):
     angle_list = []
     for i in corr:
        angle_list.append(count(img[i[0]-1:i[0]+2, i[1]-1:i[1]+2],T))
     return angle_list

def count(extract, minutiaeType):
    angle = []
    index = 0
    if minutiaeType == 0:
        for i in range(3):
            for j in range(3):
                if((i == 0 or i == 2 or j == 0 or j == 2) and extract[i][j] != 0):
                    angle = math.degrees(math.atan2(i-1, j-1))
                    if index > 1:
                        angle = 'nan'
    elif minutiaeType == 1:
        for i in range(3):
            for j in range(3):
                if ((i == 0 or i == 2 or j == 0 or j == 2) and extract[i][j] != 0):
                    angle = math.degrees(math.atan2(i - 1, j -1))
                    index+=1
        if(index != 3):
            angle = 'nan'
    if angle == 0.0 or angle == 'nan':
        return angle
    else:
        return -angle

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
    return Img_show

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
            if typeM[i] == 0:
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
