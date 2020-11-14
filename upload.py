import glob
import pymysql

#konwersja obrazu na dane binarne
def convertToBinary(filepath):
    with open(filepath, 'rb') as file:
       db_image = file.read()
    return db_image         

#wyciąganie danych z nazwy pliku
def getData(filename):
    id_person = filename[-8:-6]
    #id_person = int(id_person)+10
    nr = filename[-5]
    print(id_person, nr)
    return id_person, nr

#wykonanie operacji zapisywania w bazie dla wszystkich plików
def forAllFiles(): 
    for filepath in glob.iglob(filespath, recursive=True):
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="fingerprint_data")
        cursor = connection.cursor()
        save_sql = 'INSERT INTO fingerprint (id_person, nr, image) VALUES (%s,%s,%s)'
        db_image = convertToBinary(filepath)
        cut = filepath.rfind("\\")
        filename = filepath[cut:]
        id_person, nr = getData(filename)
        db_tuple = (id_person, nr, db_image)
        cursor.execute(save_sql, db_tuple)
        connection.commit()

#scieżka do pliku
filespath = "c:/Users/agors/Desktop/Studia/Podstawy biometrii/Projekt/Mój/Dane/DB2/*.png"
    
forAllFiles()