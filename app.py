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
    wstępnego przetwarzania obrazu odcisku palca. Przetworzony obraz poddawany 
    jest szkieletyzacji oraz wywoływana jest funkcja wykrywająca minucje.
    :param img: Obraz odcisku palca.
    :type img: numpy.ndarray
    :returns: Obraz odcisku ze wskazanymi miejscami minucji, wektor cech.
    :rtype: numpy.ndarray, String
    """
    image = image_enhance(img)
    imageSkel = skeletonize(image)
    returnImg, vetorFeatures = minutiaesRadar(imageSkel)
    return returnImg, vetorFeatures

def minutiaesRadar(img):
    """ Funkcja umożliwiająca lokalizacje minuncji.
    
    Funkcja minutiaesRadar przekazuje do funkcji ekstrahującej minucje 
    maciesz 3x3 z obrazu, a zwrócone dane zapisuje do listy. Wywołuje funkcje: 
    usuwania fałszywych minucji, okrelania orientacji, tworzenia obrazu 
    z rozrysowanymi wykrytymi minucjami oraz tworzenia wektora cech
    :param img: Obraz odcisku palca.
    :type img: numpy.ndarray
    :returns: Obraz odcisku palca ze wskazanymi miejscami minucji, wektor cech.
    :rtype: numpy.ndarray, str
    """
    width,height = img.shape
    img = np.array(img,dtype=np.int)
    xPosition = []
    yPosition = []
    typeMinutiaes = []
    for i in range(1,width-1):
        for j in range(1,height-1):
            minutiae = matrixSearch(img,i,j)
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
    :param xCorr: Lista współrzędnych x minucji.
    :type xCorr: list
    :param yCorr: Lista współrzędnych y minucji.
    :type yCorr: list
    :param typeMi: Lista zawierająca określenie typu danej minucji.
    :type typeMi: list
    :param T: List zawierająca obliczony kąt dla zakończenia.
    :type T: list
    :param B: List zawierająca obliczony kąt dla rozwidlenia.
    :type B: list
    :returns: Ciąg danych opisujących punkty szczególne odcisku palca.
    :rtype: String
    """
    vector = ("Wyniki są przedstawione w wektorze,\n który zawiera"+ 
              "informacje:\n- współrzędna x\n- współrzędna y\n- typ:"+
              " 0 - zakończenie; 1 - rozwidlenie\n- orientacja punktu (1-3 wartości)\n\n")
    indexT = 0
    indexB = 0
    for i in range(len(xCorr)):
        if typeMi[i] == 0:
            vector+=("["+str(xCorr[i])+","+str(yCorr[i])+","+str(typeMi[i])+
                     ", "+str(T[indexT]).strip(", ")+"]"+"\n")
            indexT+=1
        elif typeMi[i] == 1 and indexB<len(B):
            vector+=("["+str(xCorr[i])+","+str(yCorr[i])+","+str(typeMi[i])+
                     ", "+str(B[indexB]).strip(", ")+"]"+"\n")
            indexB+=1
    return vector

def getOrient(img,x,y,typeM):
    """ Funkcja określająca orientacje minucji.
    
    Funkcja getOrient dzieli współrzędne na położenie zakończeń i rozwidleń.
    Wywołuje funkcję obliczającą kąty dla każdego z typów minucji oddzielnie.
    :param img: Obraz odcisku palca.
    :type img: numpy.ndarray
    :param x: Lista współrzędnych x minucji.
    :type x: list
    :param y: Lista współrzędnych y minucji.
    :type y: list
    :param typeM: Lista zawierająca określenie typu danej minucji.
    :type typeM: list
    :returns: Lista kątów dla zakończenia, lista minuncji dla rozwidlenia.
    :rtype: list, list 
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
    """ Funkcja pośrednicząca w obliczaniu kątów.
    
    Funkcja getAngle wywołuje dla każdego zestawu współrzędnych 
    funkcję obliczającą kąt.
    :param img: Obraz odcisku palca.
    :type img: numpy.ndarray
    :param corr: Lista współrzędnych y minucji.
    :type corr: list
    :param T: Okrelenie typu minucji.
    :type T: int
    :returns: Lista kątów danego typu minucji.
    :rtype: list
    """
    angleList = []
    for i in corr:
       angleList.append(count(img[i[0]-1:i[0]+2, i[1]-1:i[1]+2],T))
    return angleList

def count(extract, minutiaeType):
    """ Funkcja wyznaczająca kąt.
    
    Funkcja count oblicza kąt w zależności od typu minucji: 
    jeśli zakończenie jeden, jeśli rozwidlenie trzy.
    :param extract: Fragment obrazu odcisku palca.
    :type extract: numpy.ndarray
    :param minutiaeType: Okrelenie typu minucji
    :type minutiaeType: int
    :returns: Lista kątów danego typu minucji.
    :rtype: list
    """
    angle = []
    index = 0
    index2 = 0
    values = [0,2]
    if minutiaeType == 0:
        for i in range(3):
            for j in range(3):
                if(((i in values) == True or (j in values) == True) and extract[i][j] != 0):
                    angle.append(math.degrees(math.atan2(i-1, j-1)))
                    if index > 1:
                        angle = "n"
    elif minutiaeType == 1:
        for i in range(3):
            for j in range(3):
                if (((i in values) == True or (j in values) == True) and extract[i][j] != 0):
                    angle.append(math.degrees(math.atan2(i - 1, j -1)))
                    index+=1
        if(index != 3):
            angle = "n"
    angleProperty = " "
    for k in angle:
         if angle[index2] == 0.0:
             angleProperty += str(angle[index2])+", "
         elif angle[index2] == "n":
             angleProperty += "nan"+", "
         else:
             angleProperty += str(-angle[index2])+", "
         index+=1
    return angleProperty

def drawPoint(img,x,y,t):
    """ Funkcja zaznaczająca wykryte minucje na obrazie.
    
    Funkcja drawPoint wyrysowuje na obrazie okręgi w miejscu wystąpienia 
    minucji. W zależnoci od typu okręg ma kolor zielony lub czerwony.
    :param img: Obraz odcisku palca.
    :type img: numpy.ndarray
    :param x: Lista współrzędnych x minucji.
    :type x: list
    :param y: Lista współrzędnych y minucji.
    :type y: list
    :param t: Lista zawierająca określenie typu danej minucji.
    :type t: list
    :returns: Obraz odcisku palca ze wskazanymi miejscami minucji.
    :rtype: numpy.ndarray
    """
    width,height = img.shape
    img = img*255
    colorCircle = " "
    imgM = np.zeros((width,height, 3), np.uint8)
    imgM[:, :, 0] = img
    imgM[:, :, 1] = img
    imgM[:, :, 2] = img
    for i in range(len(x)):
        if t[i] ==0:
            colorCircle = (189,236,182)
        else:
            colorCircle = (254,0,0)
        (rr, cc) = skimage.draw.circle_perimeter(x[i], y[i],4)
        skimage.draw.set_color(imgM, (rr, cc), colorCircle)
    return imgM


def matrixSearch(img,i,j):
    """ Funkcja sprawdzająca wystąpienie minucji.
    
    Funkcja matrixSearch wyznacza czy w danej macierzy 3x3 występuje minucja.
    W przypadku wystąpienia rozwidlenia wynik działania jest równy trzy, a 
    w przypadku zakończenia jeden.
    :param img: Obraz odcisku palca.
    :type img: numpy.ndarray
    :param i: Współrzędna x.
    :type i: int
    :param j: Współrzędna y.
    :type j: int
    :returns: Typ minucji: jeśli 0 jest to zakończeni, jeśli 1 jest to 
    rozwidlenie, a jeśli zwracane jest 2 minucja nie występuje w macierzy.
    :rtype: int
    """
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
    """ Funkcja usuwająca fałszywe minucje.
    
    Funkcja removeMisguided odrzuca fałszywe minucje na podstawie tego czy 
    odległość od najbliższej minucji jest większa niż średnia odległość między 
    grzbietami.
    :param img: Obraz odcisku palca.
    :type img: numpy.ndarray
    :param x: Lista współrzędnych x minucji.
    :type x: list
    :param y: Lista współrzędnych y minucji.
    :type y: list
    :param typeM: Lista zawierająca określenie typu danej minucji.
    :type typeM: list
    :returns: Współrzędne x, współrzędne y, typ minucji.
    :rtype: list, list, list
    """
    remNum = []
    xCorr = []
    yCorr = []
    typeMi = []
    treshold = tresholdSearch(img)
    for i in range(len(x)-1):
        for j in range(i):
            if typeM[i] == 0:
                distanse = np.sqrt((x[j]-x[i])**2+(y[j]-y[i])**2)
                if distanse< treshold:
                    remNum.append(i)
                    remNum.append(j)
    remNum = list(tuple(remNum))
    for k in range(len(x)):
        if not k in remNum:
            xCorr.append(x[k])
            yCorr.append(y[k])
            typeMi.append(typeM[k])
    return xCorr,yCorr,typeMi
                    
def tresholdSearch(img):
    """ Funkcja wyliczającająca średnią odległość między grzbietami.
    
    Funkcja tresholdSearch wylicza odległości między grzbietami, a następnie 
    oblicza średnią wartości.
    :param img: Obraz odcisku palca.
    :type img: numpy.ndarray
    :returns: Średnia odległość między grzbietami.
    :rtype: float
    """
    width,height = img.shape
    nearPoint = []
    for i in range(int(width/10),int(width-width/10)):
        for j in range(int(width/10),int(height-width/10)):
            if img[i][j]==1:
                for k in range(1,int(width/10)):
                    if img[i+k][j]==1:
                        nearPoint.append(k)
                        break
                    elif img[i-k][j]==1:
                        nearPoint.append(k)
                        break
    treshold = np.mean(nearPoint)
    return treshold
