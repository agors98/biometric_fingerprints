"""
Moduł zawierający stałe wartoci (kolory, grafiki, czcionki)
"""
import tkinter.font as font

#grafika
mainIcon='resources/icon.ico'
infoIcon='resources/info.ico'
dbIcon='resources/db.ico'

#kolory
color1='#2e2e2e'
color2='#dfdfdf'
color3='#d64162'
color4='#e48297'
color5='#f9e2e7'

#teksty
def getInfo():
    ''' Funkcja pobierająca informacje.
    
    Funkcja getInfo pobieranie informacje z pliku tekstowego
    i zapisuje je do zmiennej.
    :returns: None
    '''
    global infoText
    with open('resources/info.txt', 'r', encoding='utf8') as t:
        infoText = t.read()

#czcionki
def makeFonts(tk):
    ''' Funkcja tworząca czcionki.
    
    Funkcja makeFonts tworzy czcionki, 
    które są wykorzystywane w interfejsie graficznym. 
    :param tk: Obiekt klasy tkinter.Tk(), odnoszący się do głównego okna.
    :type tk: tkinter.Tk()
    :returns: None
    '''
    global labelFont, infoFont, buttonFont, textFont, inputFont
    labelFont = font.Font(tk, size=10, weight='bold')
    buttonFont = font.Font(tk, size=9)
    infoFont = font.Font(tk, size=11, weight='bold')
    textFont = font.Font(tk, size=9)
    inputFont = font.Font(tk, size=10)