import glob
import pymysql

def convertToBinary(filepath):
    with open(filepath, 'rb') as file:
       db_image = file.read()
    return db_image

def findIndexes(name, character):
    indexes = []
    for i, n in enumerate(name):
        if n==character:
            indexes.append(i)
    return indexes

def changeLanguage(x):
    return {
        'Left': 'lewa',
        'Right': 'prawa',
        'index': 'wskazujący',
        'little': 'mały',
        'middle': 'środkowy',
        'ring': 'serdeczny',
        'thumb': 'kciuk',       
    }[x]            

def getData(filename):
    indexes = findIndexes(filename, '_')
    id_person = filename[1:indexes[0]]
    hand = filename[indexes[2]+1:indexes[3]]
    finger = filename[indexes[3]+1:indexes[4]]
    hand = changeLanguage(hand)
    finger = changeLanguage(finger)
    print(id_person, hand, finger)
    return id_person, hand, finger

def forAllFiles(): 
    for filepath in glob.iglob(filespath, recursive=True):
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="fingerprint_data")
        cursor = connection.cursor()
        save_sql = 'INSERT INTO fingerprint (id_person, hand, finger, image) VALUES (%s,%s,%s,%s)'
        db_image = convertToBinary(filepath)
        cut = filepath.rfind("\\")
        filename = filepath[cut:]
        id_person, hand, finger = getData(filename)
        db_tuple = (id_person, hand, finger, db_image)
        cursor.execute(save_sql, db_tuple)
        connection.commit()

filespath = "c:/Users/agors/Desktop/Studia/Podstawy biometrii/Projekt/Mój/Dane/*.png"
    
forAllFiles()