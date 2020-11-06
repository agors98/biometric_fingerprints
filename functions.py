import tkinter as tk
from PIL import Image, ImageTk
import io
import windows as w
import style as s
from tkinter.filedialog import askopenfilename
import pymysql
 
#wywietlanie informacji
def displayInfo(self):
    w.getInfoFrame(self)
       
#wczytywanie obrazu z plików komputera
def openCF(self):
    global filepath
    global image
    global inCF
    filepath=askopenfilename(title='Wybierz plik', filetypes=(('Image fies', '*.jpg *.jpeg *.png'),))
    if len(filepath)!=0:
        image = Image.open(filepath)
        changeImage(self, image)
        inCF = True

#zmiana obrazu    
def changeImage(self, image):
    global display_image
    display_image = getDisplayImage(image)
    self.canvasImage = self.canvas.create_image((300-display_image.width())/2, (300-display_image.height())/2, image=display_image, anchor='nw')

#skalowanie obrazu
def getDisplayImage(image):
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
        
#wczytywanie obrazu z plików komputera
def saveCF(self):
    #sprawdzanie wczytania obrazu przed uruchomieniem
    if 'display_image' in globals():    
        if inCF:
            w.connectToDB(self, False)
        else:
            w.getErrMessage('Problem z obrazem', 'Proszę wczytać obraz z plików komputera')
    else:
        w.getErrMessage('Problem z obrazem', 'Proszę wczytać obraz z plików komputera')
                
#wczytywanie obrazu z bazt danych
def openDB(self):
    global inCF
    w.connectToDB(self, True)
    inCF = False 

#sprawdzanie czy wprowadzana wartość jest liczbą    
def checkNumber(user_input):      
    return user_input.isdigit()    

#konwersja obrazu na dane binarne
def convertToBinary(filepath):
    with open(filepath, 'rb') as file:
       db_image = file.read()
    return db_image

#wykonywanie wprowadzonego polecenia
def executeDB(self, openFile, id_person, hand, finger):
    global image
    if len(id_person)==0:
        w.getErrMessage('Problem z ID', 'Proszę wprowadzić ID')
    else:
        try:
            connection = pymysql.connect(host="localhost", user="root", passwd="", database="fingerprint_data")
            cursor = connection.cursor()
            check = 'SELECT id_person FROM fingerprint WHERE id_person={} AND hand=\'{}\' AND finger=\'{}\''.format(id_person, hand.lower(), finger.lower())
            cursor.execute(check)
            data = cursor.fetchall()
            connection.commit()
            inDB = False if len(data)==0 else True
            #operacja odczytu
            if openFile:
                if inDB: 
                    try:
                        open_sql = 'SELECT image FROM fingerprint WHERE id_person={} AND hand=\'{}\' AND finger=\'{}\''.format(id_person, hand.lower(), finger.lower())
                        cursor.execute(open_sql)
                        connection.commit()
                        data = cursor.fetchall()
                        file = io.BytesIO(data[0][0])
                        image = Image.open(file)
                        changeImage(self, image)
                        self.db.destroy()
                        w.getInfoMessage('Zakończono połączenie', 'Przeprowadzono operację')
                    except:
                        w.getErrMessage('Problem z poleceniem', 'Nie udało się przeprowadzić operacji. Proszę sprawdzić poprawność wprowadzonych danych')
                else:
                    w.getErrMessage('Problem z danymi', 'Brak danych w bazie') 
            #operacja zapisu
            else:
                if not inDB:
                    try:
                        save_sql = 'INSERT INTO fingerprint (id_person, hand, finger, image) VALUES (%s,%s,%s,%s)'
                        db_image = convertToBinary(filepath)
                        db_tuple = (id_person, hand.lower(), finger.lower(), db_image)
                        data = cursor.execute(save_sql, db_tuple)
                        connection.commit()
                        self.db.destroy()
                        w.getInfoMessage('Zakończono połączenie', 'Przeprowadzono operację')
                    except:
                        w.getErrMessage('Problem z poleceniem', 'Nie udało się przeprowadzić operacji. Proszę sprawdzić poprawność wprowadzonych danych')
                else:
                    w.getErrMessage('Problem z danymi', 'Dla podanych danych istnieje już obraz. Poroszę zmienić wartości')                    
            cursor.close()
            connection.close()
        except:
             w.getErrMessage('Problem z połączeniem', 'Nie udało się nawiązać połączenia z bazą')  

#uruchamianie programu
def executeProgram(self):
    #sprawdzanie wczytania obrazu przed uruchomieniem
    if 'display_image' in globals():
        image.show()
        #results = []
        #image = Image.open(file)
        #changeImage(self, image)
        #showResults(self, results)
        w.getInfoMessage('Ekstrakcja zakończona', 'Detekcja została przeprowadzona')
    else:
        w.getErrMessage('Problem z obrazem', 'Proszę wczytać obraz z plików komputera')

#wyświetlanie wyników
def showResults(self, results): 
    self.resultsScrollbar = tk.Scrollbar(self.resultsFrame, orient=tk.VERTICAL)
    self.resultsScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.resultsCanvas = tk.Canvas(self.resultsFrame, bg=s.color3, yscrollcommand=self.resultsScrollbar.set)
    self.resultsCanvas.create_text(100, 100, text=results, font=s.textFont)
    self.resultsCanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    self.resultsScrollbar.config(command=self.resultsCanvas.yview)
    self.resultsCanvas.config(scrollregion=self.resultsCanvas.bbox('all'))