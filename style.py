import tkinter.font as font

#grafika
mainIcon='resources/icon.ico'
infoIcon='resources/info.ico'
dbIcon='resources/db.ico'

#kolory
color0='#2e2e2e'
color1='#c1c1c1'
color2='#dfdfdf'
color3='#d64162'
color4='#e48297'
color5='#f9e2e7'

#teksty
def getInfo():
    global infoText
    with open('resources/info.txt', 'r', encoding='utf8') as t:
        infoText = t.read()

#czcionki
def makeFonts(tk):
    global labelFont, infoFont, buttonFont, textFont, inputFont
    labelFont = font.Font(tk, size=10, weight='bold')
    buttonFont = font.Font(tk, size=9)
    infoFont = font.Font(tk, size=11, weight='bold')
    textFont = font.Font(tk, size=9)
    inputFont = font.Font(tk, size=10)