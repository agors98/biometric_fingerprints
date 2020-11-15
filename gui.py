import tkinter as tk
import style as s
import functions as f

class Gui:
 
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('System ekstrakcji cech na podstawie odcisku palca')
        self.root.iconbitmap(s.mainIcon)
        self.root.configure(bg=s.color0)
        self.root.geometry('650x600')
        self.root.resizable(0, 0)
        
        s.makeFonts(self.root)  
        
        #wyświetlanie informacji
        self.displayButton = tk.Button(master=self.root, text='ⓘ', command=lambda: f.displayInfo(self), font=s.infoFont)
        self.displayButton.place(relx=0.93, rely=0.02)
        
        #wczytywanie obrazu z plików komputera i zapisywanie go do bazy
        self.openCFLabel = tk.Label(self.root, text='Wczytaj obraz z plików komputera', bg=s.color3, font=s.labelFont)
        self.openCFLabel.place(width=300, relx=0.03, rely=0.1)
        self.openCFButton = tk.Button(master=self.root, text='Wczytaj z komputera', command=lambda: f.openCF(self), font=s.buttonFont)
        self.openCFButton.place(width=120, relx=20/650+0.03, rely=0.15)
        self.saveButton = tk.Button(master=self.root, text='Dodaj obraz do bazy', command=lambda: f.saveCF(self), font=s.buttonFont)
        self.saveButton.place(width=120, relx=160/650+0.03, rely=0.15)
        
        #wczytywanie obrazu z bazy danych
        self.openDBLabel = tk.Label(self.root, text='Wczytaj obraz z bazy danych', bg=s.color3, font=s.labelFont)
        self.openDBLabel.place(width=300, relx=0.03, rely=0.22)
        self.openDBButton = tk.Button(master=self.root, text='Wczytaj z bazy', command=lambda: f.openDB(self), font=s.buttonFont)
        self.openDBButton.place(width=120, relx=90/650+0.03, rely=0.27)
        
        #wyświetlanie obrazu
        self.canvas = tk.Canvas(self.root, bg=s.color5, width=300, height=300)
        self.canvas.place(relx=0.03, rely=0.35)
        
        #uruchomienie programu
        self.startButton = tk.Button(self.root, text='Wykonaj', command=lambda: f.executeProgram(self), font=s.buttonFont)
        self.startButton.place(relwidth=0.12, relheight=0.06, relx=300/650-0.09, rely=0.89)
        
        #wyświetlanie wynikow
        self.resultsLabel = tk.Label(self.root, text='Wyniki', bg=s.color3, font=s.labelFont)
        self.resultsLabel.place(relwidth=0.42, x=350, rely=0.1)
        self.resultsFrame = tk.Frame(self.root, bg=s.color2)
        self.resultsFrame.place(relwidth=0.42, relheight=0.815, x=350, rely=0.135)
        
        self.root.mainloop()