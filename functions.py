"""
Moduł zawierający funkcje związane z pracą z interfejsem
"""
import tkinter as tk
from PIL import Image, ImageTk
import io
import style as s
import windows as w
import app as a
import cv2
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror
import pymysql
import numpy as np 
       
def openCF(self):
    ''' Funkcja wczytująca obraz z plików komputera.
    
    Funkcja openCF otwiera okno dialogowe
    i pozwala na wgranie obrazu z plików komputera.
    :returns: None
    '''
    global filepath, image, inCF, imageprep
    for widget in self.resultsFrame.winfo_children():
        widget.destroy()
    filepath=askopenfilename(title='Wybierz plik', filetypes=(('Pliki obrazów', '*.jpg *.jpeg *.png'),))
    if len(filepath)!=0:
        image = Image.open(filepath)
        imageprep = cv2.imread(filepath,0)
        changeImage(self, image)
        inCF = True
    
def changeImage(self, image):
    ''' Funkcja zmienająca wyświetlany obraz.
    
    Funkcja changeImage zmienia obraz wyświetlany w przeznaczonym
    do tego panelu na obraz przekazany.
    :param image: Obraz odcisku palca.
    :type image: PIL.Image
    :returns: None
    '''
    global display_image
    display_image = getDisplayImage(image)
    self.canvasImage = self.canvas.create_image((300-display_image.width())/2, (300-display_image.height())/2, image=display_image, anchor='nw')

def getDisplayImage(image): 
    ''' Funkcja dopasowująca rozmiary obrazu do wyświetlenia.
    
    Funkcja getDisplayImage zmienia rozmiar wgranego obrazu 
    w celu dopasowania go do wyświetlenia w panelu.
    :param image: Obraz odcisku palca.
    :type image: PIL.Image
    :returns: None
    '''
    width, height = image.size
    #powiększanie
    if width<=300 and height<=300:
        if width*2<=300 and height*2<=300*2:
            image = image.resize((width*2, height*2)) 
    #zmniejszanie
    else:
        ratio = min(300/width, 300/height)
        image = image.resize((int(ratio*width), int(ratio*height)))
    display_image = ImageTk.PhotoImage(image)
    return display_image
        
def saveCF(self):
    ''' Funkcja podejmująca próbę zapisu obrazu do bazy danych.
    
    Funkcja saveCF sprawdza wgranie obrazu
    i podejmuje próbę jego zapisu w bazie danych.
    :returns: None
    '''
    #sprawdzanie wczytania obrazu przed uruchomieniem
    if 'display_image' in globals():    
        if inCF:
            w.connectToDB(self, False)
        else:
            showerror('Problem z obrazem', 'Proszę wczytać obraz z plików komputera')
    else:
        showerror('Problem z obrazem', 'Proszę wczytać obraz z plików komputera')
                
def openDB(self):
    ''' Funkcja podejmujaca próbę wczytania obrazu z bazy danych.
    
    Funkcja openDB podejmuje próbę wczytania obrazu z bazy danych.
    :returns: None
    '''
    global inCF
    for widget in self.resultsFrame.winfo_children():
        widget.destroy()
    w.connectToDB(self, True)
    inCF = False 
    
def checkNumber(user_input): 
    ''' Funkcja sprawdzająca czy wprowadzane dane są cyframi.
    
    Funkcja checkNumber sprawdza czy wprowadzane sane są cyframi.
    :parma user_input: Dane wprowadzane przez użytkownika.
    :type user_input: str
    :returns: True, jeżeli wprowadzane dane są cyframi, False jeśli nie.
    :rtype: bool
    '''     
    return user_input.isdigit()    

def convertToBytes(filepath):
    ''' Funkcja konwertująca obraz na bajty.
    
    Funkcja convertToBinary przeprowadza konwersję obrazu na bajty. 
    :param filepath: Ścieżka do pliku z obrazem.
    :type filepath: str
    :returns: Plik obrazu przekonwertowany na bajty.
    :rtype: bytes
    '''
    with open(filepath, 'rb') as file:
       db_image = file.read()
    return db_image

def executeDB(self, openFile, id_person, nr):
    ''' Funkcja przekazująca komendy do bazy danych.
    
    Funkcja executeDB przekazuje komendy dotyczące odczytu
    lub zapisu pliku do bazy danych. 
    :param openFile: Informacje czy wykonana operacja ma byc odczytem.
    :type openFile: bool
    :param id_person: Nr ID osoby.
    :type id_person: str
    :param nr: Nr zdjęcia.
    :type nr: str
    :returns: None
    '''
    global image, imageprep
    if len(id_person)==0 or len(nr)==0:
        showerror('Problem z wartościami', 'Proszę wprowadzić wszystkie wartości')
    else:
        try:
            connection = pymysql.connect(host="localhost", user="root", passwd="", database="fingerprint_data")
            cursor = connection.cursor()
            check = 'SELECT id_person FROM fingerprint WHERE id_person={} AND nr={}'.format(id_person, nr)
            cursor.execute(check)
            data = cursor.fetchall()
            connection.commit()
            inDB = False if len(data)==0 else True
            #operacja odczytu
            if openFile:
                if inDB: 
                    try:
                        open_sql = 'SELECT image FROM fingerprint WHERE id_person={} AND nr={}'.format(id_person, nr)
                        cursor.execute(open_sql)
                        connection.commit()
                        data = cursor.fetchall()
                        file = io.BytesIO(data[0][0])
                        imageprep= cv2.imdecode(np.frombuffer(data[0][0], np.uint8), 0)
                        image = Image.open(file)
                        changeImage(self, image)
                        self.db.destroy()
                        showinfo('Zakończono połączenie', 'Przeprowadzono operację')
                    except:
                        showerror('Problem z poleceniem', 'Nie udało się przeprowadzić operacji. Proszę sprawdzić poprawność wprowadzonych danych')
                else:
                    showerror('Problem z danymi', 'Brak danych w bazie') 
            #operacja zapisu
            else:
                if not inDB:
                    try:
                        save_sql = 'INSERT INTO fingerprint (id_person, nr, image) VALUES (%s,%s,%s)'
                        db_image = convertToBytes(filepath)
                        db_tuple = (id_person, nr, db_image)
                        data = cursor.execute(save_sql, db_tuple)
                        connection.commit()
                        self.db.destroy()
                        showinfo('Zakończono połączenie', 'Przeprowadzono operację')
                    except:
                        showerror('Problem z poleceniem', 'Nie udało się przeprowadzić operacji. Proszę sprawdzić poprawność wprowadzonych danych')
                else:
                    showerror('Problem z danymi', 'Dla podanych danych istnieje już obraz. Poroszę zmienić wartości')                    
            cursor.close()
            connection.close()
        except:
             showerror('Problem z połączeniem', 'Nie udało się nawiązać połączenia z bazą')  

#uruchamianie programu
def executeProgram(self):
    ''' Funkcja rozpoczynjąca proces ekstrakcji.
    
    Funkcja executeProgram rozpoczyna proces ekstrakcji cech
    z dostarczanego odcisku palca.
    :returns: None
    '''    
    if 'display_image' in globals():
        array, results = a.imagepreproces(imageprep)
        image = Image.fromarray(np.uint8(array)).convert('RGB')
        changeImage(self, image)
        showResults(self, results)
        showinfo('Ekstrakcja zakończona', 'Detekcja została przeprowadzona')

#wyświetlanie wyników
def showResults(self, results): 
    ''' Funkcja wyświetlająca wyniki.
    
    Funkcja showResults wyświetla wynikowy wektor cech
    w przeznaczonym do tego panelu.
    :param results: Ciąg znaków zawierjący wynikowy wektor cech.
    :type results: str
    :returns: None
    '''    
    self.resultsScrollbar = tk.Scrollbar(self.resultsFrame, orient=tk.VERTICAL)
    self.resultsScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.resultsCanvas = tk.Canvas(self.resultsFrame, bg=s.color2, yscrollcommand=self.resultsScrollbar.set)
    self.resultsCanvas.create_text(100, 100, text=results, font=s.textFont)
    self.resultsCanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    self.resultsScrollbar.config(command=self.resultsCanvas.yview)
    self.resultsCanvas.config(scrollregion=self.resultsCanvas.bbox('all'))