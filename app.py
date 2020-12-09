"""
Moduł zawierający operację związane z ekstrakcją cech odcisku palca
"""
from image_enhance import image_enhance
import numpy as np
from skimage.morphology import skeletonize
import skimage
import numpy 
import math

def imagepreproces(img):
    """ Funkcja umożliwiająca przetworzenie dostarczonego obrazu.
    
    Funkcja imagepreprocess wywołuje funkcję image_enhace dokonującą 
    preprocesingu obrazu odcisku palca. Przeetworzony obraz poddawany 
    jest szkieletyzacji oraz wywoływana jest funkcja wykrywająca minucje.
    :param img: array
    :returns: Obraz odcisku ze wskazanymi miejscami minucji i wektor cech.
    :rtype: array, String
    """
    image = image_enhance(img)
    imageSkel = skeletonize(image)
    returnImg, vetorFeatures = minutiaesRadar(imageSkel)
    return returnImg, vetorFeatures

def minutiaesRadar(img):
    """ Funkcja umożliwiająca lokalizację minuncji.
    
    Funkcja minutiaesRadar przekazuje do funkcji ekstrahującej minucji 
    maciesz 3x3 z obrazu, zwrócone dane zapisuje do listy. Wywołuje funkcję 
    usuwającą fałszywe minucje, okrelającą orientację, tworzącą obraz 
    w rozrysowanymi wykrytymi minucjami oraz tworzącą wektor cech
    :param img: array
    :returns: Obraz odcisku palca ze wskazanymi miejscami minucji 
    i wektor cech.
    :rtype: array, String
    """
    width,height = img.shape
    img = np.array(img,dtype=np.int)
    xPosition = []
    yPosition = []
    typeMinutiaes = []
    for i in range(1,width-1):
        for j in range(1,height-1):
            minutiae = matrix_search(img,i,j)
            if minutiae != 2:
                xPosition.append(i)
                yPosition.append(j)
                typeMinutiaes.append(minutiae)
    xCorr,yCorr,typeMi = removeMisguided(img, xPosition, 
                                            yPosition,typeMinutiaes)
    orientationT, orientationB = getOrient(img,xCorr,yCorr,typeMi)
    returnImg = drawPoint(img,xCorr,yCorr,typeMi)
    vetorFeatures = getVectors(xCorr,yCorr,typeMi,orientationT, 
                                 orientationB)
    return returnImg, vetorFeatures

def getVectors(xCorr,yCorr,typeMi,T, B):
    """ Funkcja tworząca wektor cech odcisku palca.
    
    Funkcja getVectors tworzy ciąg z dostarczonych danych.
    :param xCorr: List
    :param yCorr: List
    :param typeMi: List
    :param T: List
    :param B: List
    :returns: Ciąg danych opisujących punkty szczególne odcisku palca.
    :rtype: String
    """
    vector = ("Wyniki są przedstawione w wektorze,\n który zawiera"+ 
              "informacje:\n- współrzędna x\n- współrzędna y\n- typ:"+
              " 0 - zakończenie; 1 - rozwidlenie\n- orientacja punktu \n\n")
    indexT = 0
    indexB = 0
    for i in range(len(xCorr)):
        if typeMi[i] == 0:
            vector+=("["+str(xCorr[i])+","+str(yCorr[i])+","+str(typeMi[i])+
                     ","+str(T[indexT])+"]"+"\n")
            indexT+=1
        elif typeMi[i] == 1:
            vector+=("["+str(xCorr[i])+","+str(yCorr[i])+","+str(typeMi[i])+
                     ","+str(B[indexB])+"]"+"\n")
            indexB+=1
    return vector

def getOrient(img,x,y,typeM):
    """ Funkcja określająca orientacje minucji.
    
    Funkcja getOrient dzieli współrzędne na położenie zakończeń i rozwidleń.
    Wywołuje funkcję obliczającą kąty dla każdego z typów minucji oddzielnie.
    :param img: array
    :param x: List
    :param y: List
    :param typeM: List
    :returns: Listę kątów obu typów minucji.
    :rtype: List, List 
    """
    BCorr = []
    TCorr = []
    for i in range(len(typeM)):
        if typeM[i] == 0:
            TCorr.append([x[i],y[i]])
        else:
            BCorr.append([x[i],y[i]])
    angleT = getAngle(img,TCorr,0)
    angleB = getAngle(img,BCorr,1)
    return angleT, angleB

def getAngle(img,corr,T):
    """ Funkcja wyznaczająca kąt.
    
    Funkcja getAngle wywołuje dla każdego zestawu współrzędnych 
    funkcję obliczającą kąt.
    :param img: array
    :param corr: List
    :param T: int
    :returns: Listę kątów jednego typu minucji.
    :rtype: List
    """
    angleList = []
    for i in corr:
       angleList.append(count(img[i[0]-1:i[0]+2, i[1]-1:i[1]+2],T))
    return angleList

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

def drawPoint(img,x,y,t):
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

def removeMisguided(img,x,y,typeM):
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
