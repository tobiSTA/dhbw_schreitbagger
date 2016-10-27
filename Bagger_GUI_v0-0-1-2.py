'''
Bagger_GUI v0.0.1.2

Grafische Benutzeroberfläche für den Wasserhydraulischen Schreitbagger der DHBW-Ravensburg -Campus Friedrichshafen
mit der Implementierung rudimentärer Systemsteuerungs-Eingaben
'''

from tkinter import *
import logging
import datetime
import os
from Bagger_Controll_Modul_0_3 import *
from PIL import Image

sdir = "/home/ubuntu/Bagger/Bagger_Software"

if os.path.exists(str(sdir + "/log")) == False :
    os.mkdir(str(sdir + "/log"))                                                       #anlegen Loggverzeichnis

if os.path.exists(str(sdir + "/Temp")) == False :
    os.mkdir(str(sdir + "/Temp"))                                                       #anlegen Temporärverzeichnis


dt = datetime.datetime.now()                                                                                #Auslesen der Aktuelllen Systemzeit

d = str(dt.strftime('%d-%m-%Y_%H-%M'))                                                                      #Zeit Formatierung

loggfile = str(sdir + "/log/bagger_GUI-log_" + d)                                  #Erstellung Logg-file-Adresse
logging.basicConfig(filename = loggfile, format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.DEBUG)   #initialiesierung der Log funktion

logging.info('Start der Anwendung Bagger_GUI')

try:

    def close(self):
        '''
        Funktion zum schliesen der GUI
        '''

        logging.info('Die Funktion Close wurde gestartet')
        if messagebox.askokcancel(
            title = 'Schliesen',
            message= 'Sind Sie Sicher, dass sie das Programm Schliesen wollen?/nDas Schliesen dies prgrammes fürt zur Abschaltung des Baggers und seiner Sterung,/n dabei kann es zu ungewollten Störfällen kommen!'
            ):
            self.destroy()
        else:
            logging.info('Die Funktion Close wurde gecanceld')

        
        messagebox.showinfo('Controler Change', ' Sie haben %s  als Controler ausgewählt' % (controler_list[controler_state]))
        logging.info('Controler wurde zu %s geändert' % (controler_list[controler_state]))

        
    modi= [("baggern",0),("Schreiten vorne",1),("schreiten hinten",2), ("Fahren",3)]                            # Definition Steuermodie mit radiobutton Wert

        
    m =Tk()                                                                                                     #Initialisierung Tk-Window
    m.title("Bagger GUI")                                                                                       #Titel GUI-Fenster

    dirBagger = str(sdir + "/Grafiken/Schreitbagger_Baggern.png")     #erstellen Bildaddresse Bagger Zentralbild Funktion barggern_P
    dirJoy_L   = str(sdir + "/Grafiken/Baggern_links.png")               #Erstellen Bildadresse Erklärung Steuerung Joystik Links
    dirJoy_R   = str(sdir + "/Grafiken/Baggern_rechts.png")              #Erstellen Bildadresse Erklärung Steuerung Joystik Rechts

    dirImages = [dirBagger, dirJoy_L, dirJoy_R]                         #Erstellung Adressliste der Bilder
    
    cv_w = m.winfo_screenwidth()                                                                                                 #Canvas/Fenster Breite
    cv_h = m.winfo_screenheight()  -20                                              #Canvas/Fenster Höhe
    screen_Scale = cv_h/748                                             #Berechnung der Bildskalierung im verhältnis zu einem Monitor mit 768p Höhenauflösung
    print('Bildschirmauflösung: %d x %d' %(cv_w, cv_h))
    c_s_y= int(cv_h/8)                                                                                                    #Starhöhe ZentralKreis
    c_e_y = int( cv_h - c_s_y/2)                                                                                  #endhöhe Zentralkreis
    c_s_x=int(cv_w /2-(cv_h-1.5*c_s_y)/2)                                                                         #Startposition in X Zentralkreis
    c_e_x= int(cv_w /2+(cv_h-1.5*c_s_y)/2)                                                                        #Endposition in x Zentralkreis
    rb_w =27                                                                                                    #Radiobutton Breite[Textzeichen]
    line_width = (cv_w/150)                                                                                              #Linienstärke
    border = int(cv_w/100)                                                                                                  #Ausenrand
    b_width = 35
    b_pady = cv_h / 37
    pImages = []                                                        #Erstellung einer Liste für PhotoImages
    
    modus = IntVar()

    for i in dirImages:                                                 # Schleife zur Erstellung der skalierten Bilder mit hilfe der PIL
        ImTemp = Image.open(i)
        ImTemp.resize((int(ImTemp.size[0]*screen_Scale),int(ImTemp.size[1]* screen_Scale)), Image.ANTIALIAS)
        i = i.replace("Grafiken", "Temp")
        ImTemp.save(i)
        pImages.append(PhotoImage(file = i))
        
    w = Canvas(m, width = cv_w, height = cv_h, bg = "black")                                                                  #Initialisierung Canvas (Grafische objekte)

    w.pack()

    w.create_rectangle(border, c_s_y, cv_w-border, cv_h-c_s_y-border, fill ="lightgray")                     #Initialisierung background für Steuerungserklärung
    w.create_oval(c_s_x,c_s_y, c_e_x, c_e_y, width = line_width*3, outline = "black", fill ="gray")                                       #Initialisierung Zentralkreis
    w.create_oval(c_s_x,c_s_y, c_e_x, c_e_y, width = line_width, outline = "blue" )                                       #Initialisierung Zentralkreis
    w.create_image(cv_w/2, cv_h/2, image = pImages[0])                                                             #Initialisierung Zentralbild
    w.create_image(c_s_x/2, cv_h/2, image = pImages[1])                                                              #Initialisierung Bild Erklärung Stererung Joystik Links
    w.create_image(cv_w - c_s_x/2, cv_h/2, image = pImages[2])                                                       #Initialisierung Bild Erklärung Stererung Joystik Rechts

    for txt, val in modi:                                                                                        #Initialisierung Radiobutons Steuerungswahl
        Radiobutton(w,
                    text = txt,
                    indicatoron = 0,
                    width = rb_w,
                    pady = b_pady,
                    variable = modus,
                    value = val,
                    bd=line_width
                    ).place(x = int(val*(cv_w/4)+border),y = border, anchor=NW)

    controler = Button(w, text = "Controler", width =b_width, pady = b_pady, bd = line_width, command = lambda :change_controler(controler_state)).place(x=cv_w-border, y=cv_h-1.5*border, anchor= SE)

    wartung = Menubutton(w, text = "Wartung", width = b_width, pady = b_pady, bd = line_width, direction='above')  

    mb_war = Menu (wartung)
    wartung.config(menu = mb_war)
    mb_war.add_command(label='Schliesen', command = lambda: close(m))
    mb_war.add_command(label='Hupe', command = lambda: horn())
    mb_war.add_command(label='Licht', command = lambda: light())
    mb_war.add_command(label='Rücklicht', command = lambda: Taillight())
    mb_war.add_command(label='Motor', command = lambda: FU())
    mb_war.add_command(label='Pumpe', command = lambda: pump())
    wartung.place(x=border, y=cv_h-1.5*border, anchor= SW)

    
    mainloop()

    logging.info("Bagger_GUI wurde geschlossen")

    
except Exception as e:
    e = str(e)
    logging.error(str(e))
    logging.info("Bagger_GUI wurde abgebrochen")
    print (e)
