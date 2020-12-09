"""
Moduł wgrywający początkowe dane do bazy
"""
import glob
import pymysql

def convertToBytes(filepath):
    ''' Funkcja konwertująca obraz na bajty.
    
    Funkcja convertToBytes przeprowadza konwersję obrazu na bajty. 
    :param filepath: Ścieżka do pliku z obrazem.
    :type filepath: str
    :returns: Plik obrazu przekonwertowany na bajty.
    :rtype: bytes
    '''
    with open(filepath, 'rb') as file:
       db_image = file.read()
    return db_image         

def getData(filename):
    ''' Funkcja pobierająca dane na temat obrazu.
    
    Funkcja getData pobiera dane na teamt obrazu
    z nazwy pliku przeznaczonego do wgrania, w celu wgrania ich do bazy. 
    Uzyskiwane wartoci to ID osoby oraz numer zdjęcia.
    :param filename: Nazwa pliku z obrazem.
    :type filename: str
    :returns: ID osoby, numer zdjęcia.
    :rtype: str, str
    '''
    id_person = filename[-8:-6]
    #id_person = int(id_person)+10
    nr = filename[-5]
    print(id_person, nr)
    return id_person, nr

def forAllFiles(filespath): 
    ''' Funkcja wgrywająca wszytkie pliki z folderu do bazy.
    
    Funkcja forAllFiles łączy się z bazą danych. Następnie uzyskuje odpowiednie
    dane z funkcji: convertToBytes oraz getData. Takie informacje są wgrywane
    do bazy danych. Operacja jest przeprowadzana dla wszytskich plików w folderze.
    :param filespath: Ścieżka do folderu z obrazami.
    :type filespath: str
    :returns: None
    '''
    for filepath in glob.iglob(filespath, recursive=True):
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="fingerprint_data")
        cursor = connection.cursor()
        save_sql = 'INSERT INTO fingerprint (id_person, nr, image) VALUES (%s,%s,%s)'
        db_image = convertToBytes(filepath)
        cut = filepath.rfind("\\")
        filename = filepath[cut:]
        id_person, nr = getData(filename)
        db_tuple = (id_person, nr, db_image)
        cursor.execute(save_sql, db_tuple)
        connection.commit()

filespath = "c:/Users/agors/Desktop/Studia/Podstawy biometrii/Projekt/Mój/Dane/DB1/*.png" 
forAllFiles(filespath)