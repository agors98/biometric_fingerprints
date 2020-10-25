import tkinter as tk
import tkinter.ttk as ttk
import functions as f
import style as s

def getImageMessage():
    tk.messagebox.showerror(title='Problem z obrazem', message='Proszę wczytać obraz z plików komputera')

def getConnectionMessage():
    tk.messagebox.showerror(title='Problem z połączeniem', message='Nie udało się nawiązać połączenia z bazą')
  
def getCommandMessage():
    tk.messagebox.showerror(title='Problem z poleceniem', message='Nie udało się przeprowadzić operacji. Proszę sprawdzić poprawność wprowadzonych danych')

def getNoIDMessage():
    tk.messagebox.showerror(title='Problem z brakiem ID', message='Proszę wprowadzić ID')
        
def getDoneMessage():
    tk.messagebox.showinfo(title='Zakończono połączenie', message='Przeprowadzono operację')

def getNotInMessage():
    tk.messagebox.showerror(title='Problem z danymi', message='Brak danych w bazie')

def getInMessage():
    tk.messagebox.showerror(title='Problem z danymi', message='Dla podanych danych istnieje już obraz. Poroszę zmienić wartości')
    
def getInfoFrame(self):
    self.info = tk.Toplevel(self.root, width=450, height=200, background=s.color4)
    self.info.grab_set()
    self.info.geometry('+%d+%d' % (self.root.winfo_x()+100, self.root.winfo_y()+200))
    self.info.title('Informacje')
    self.info.iconbitmap(s.infoIcon)
    self.info.resizable(0, 0)
    self.infoFrame = tk.Frame(self.info, bg=s.color2)
    self.infoFrame.place(relwidth=0.95, relheight=0.9, relx=0.025, rely=0.05)
    s.getInfo()
    self.infoText = tk.Label(self.info, text=s.infoText, bg=s.color2, font=s.textFont)
    self.infoText.place(relwidth=0.95, relheight=0.9, relx=0.025, rely=0.05)

def connectToDB(self, openFile):
    if openFile==True:
        title = 'Odczytaj obraz'
        button_text = 'Odczytaj'
    else:
        title = 'Zapisz obraz'
        button_text = 'Zapisz'
    self.db = tk.Toplevel(self.root, width=300, height=100, background=s.color4)
    self.db.grab_set()
    self.db.geometry('+%d+%d' % (self.root.winfo_x()+175, self.root.winfo_y()+250))
    self.db.title(title)
    self.db.iconbitmap(s.dbIcon)
    self.db.resizable(0, 0)
    
    self.idLabel = tk.Label(self.db, text='ID', bg=s.color2, font=s.labelFont)
    self.idLabel.place(x=0, y=0, width=100, height=25)
    valid = self.db.register(f.checkNumber)
    self.idEntry = tk.Entry(self.db, validate='key', validatecommand=(valid, '%S'), font=s.inputFont) 
    self.idEntry.place(x=0, y=25, width=100) 
    
    self.handLabel = tk.Label(self.db, text='Ręka', bg=s.color2, font=s.labelFont)
    self.handLabel.place(x=100, y=0, width=100, height=25)
    self.handCB = ttk.Combobox(self.db, state="readonly", font=s.inputFont) 
    self.handCB['values'] = ('Prawa', 'Lewa')
    self.handCB.current(0)
    self.handCB.place(x=100, y=25, width=100)
    self.handLabel = tk.Label(self.db, text='Palec', bg=s.color2, font=s.labelFont)
    self.handLabel.place(x=200, y=0, width=100, height=25)
    self.fingerCB = ttk.Combobox(self.db, state="readonly", font=s.inputFont) 
    self.fingerCB['values'] = ('Kciuk', 'Wskazujący', 'Środkowy', 'Serdeczny', 'Mały')
    self.fingerCB.current(0)
    self.fingerCB.place(x=200, y=25, width=100) 
    
    self.dbButton = tk.Button(self.db, text=button_text, command=lambda: f.executeDB(self, openFile, self.idEntry.get(), self.handCB.get(), self.fingerCB.get()), font=s.buttonFont)
    self.dbButton.place(width=80, height=40, x=110, y=55)        