"""
Moduł zawierający implementacje dodatkowych okien aplikacji
"""
import tkinter as tk
import functions as f
import style as s


def getInfoFrame(self):
    """ Funkcja umożliwiająca utworzenie okna z informacji.
    
    Funkcja getInfoFrame umożliwa utworzenie okna
    z informacjami na temat progrmu.
    :returns: None
    """
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
    """ Funkcja umożliwiająca utworzenie okna połączenia z bazą danych.
    
    Funkcja connectToDB umożliwa utworzenie okna służącego do wpisywania poleceń
    przekazywanych do bazy danych. Operacja ta może dotyczyć zapisu ub odczytu.
    :param openFile: Informacje czy wykonana operacja ma byc odczytem.
    :type openFile: bool
    :returns: None
    """
    #odczyt danych
    if openFile==True:
        title = 'Odczytaj obraz'
        button_text = 'Odczytaj'
    #zapis danych
    else:
        title = 'Zapisz obraz'
        button_text = 'Zapisz'
    self.db = tk.Toplevel(self.root, width=300, height=46, background=s.color4)
    self.db.grab_set()
    self.db.geometry('+%d+%d' % (self.root.winfo_x()+175, self.root.winfo_y()+277))
    self.db.title(title)
    self.db.iconbitmap(s.dbIcon)
    self.db.resizable(0, 0)
    #pole do wpisywania
    valid = self.db.register(f.checkNumber)
    self.idLabel = tk.Label(self.db, text='ID', bg=s.color2, font=s.labelFont)
    self.idLabel.place(x=0, y=0, width=100, height=25)
    self.idEntry = tk.Entry(self.db, validate='key', validatecommand=(valid, '%S'), font=s.inputFont) 
    self.idEntry.place(x=0, y=25, width=100) 
    self.nrLabel = tk.Label(self.db, text='Nr', bg=s.color2, font=s.labelFont)
    self.nrLabel.place(x=100, y=0, width=100, height=25)
    self.nrEntry = tk.Entry(self.db, validate='key', validatecommand=(valid, '%S'), font=s.inputFont) 
    self.nrEntry.place(x=100, y=25, width=100)
    #przycisk do wykonania polecenia
    self.dbButton = tk.Button(self.db, text=button_text, command=lambda: f.executeDB(self, openFile, self.idEntry.get(), self.nrEntry.get()), font=s.buttonFont)
    self.dbButton.place(width=80, height=40, x=210, y=3)        