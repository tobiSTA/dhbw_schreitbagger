
'''
Bagger_GUI v0.0.0.1

Grafische Benutzeroberfläche für den Wasserhydraulischen Schreitbagger der DHBW-Ravensburg -Campus Friedrichshafen
mit der Implementierung rudimentärer Systemsteuerungs-Eingaben
'''

from tkinter import *
import logging
import datetime
import os
from PIL import Image, ImageTk

if os.path.exists("/home/pi/Desktop/bagger/log") == False :
    os.mkdir("/home/pi/Desktop/bagger/log")                                                       #anlegen Loggverzeichnis

dt = datetime.datetime.now()                                                                                #Auslesen der Aktuelllen Systemzeit

d = str(dt.strftime('%d-%m-%Y_%H-%M'))                                                                      #Zeit Formatierung

loggfile = str("/home/pi/Desktop/bagger/log" + d)                                  #Erstellung Logg-file-Adresse
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
            self.destroy
        else:
            logging.info('Die Funktion Close wurde gecanceld')

            
    def change_controler(state):
        '''
        Funktion zum wechseln des Eingabegeräts/Controlers
        '''
        global controler_state
        if state == 0:
            controler_state = 1
        else:
            controler_state = 0
        
        messagebox.showinfo('Controler Change', ' Sie haben %s  als Controler ausgewählt' % (controler_list[controler_state]))
        logging.info('Controler wurde zu %s geändert' % (controler_list[controler_state]))

        
    modi= [("baggern",0),("Schreiten vorne",1),("schreiten hinten",2), ("Fahren",3)]                            # Definition Steuermodie mit radiobutton Wert


    controler_list= {0: "Gamepad", 1: "Joystik"}
    controler_state = 0
        
    m =Tk()                                                                                                     #Initialisierung Tk-Window
    m.title("Bagger GUI")                                                                                       #Titel GUI-Fenster

    image_schreitbagger = "/home/pi/Desktop/bagger/Grafiken/Schreitbagger_Baggern_V2_2.png" #Paf für image
    image_joy_L = "/home/pi/Desktop/bagger/Grafiken/Baggern_links.png"
    image_joy_R = "/home/pi/Desktop/bagger/Grafiken/Baggern_rechts.png"
	
    image_input = [image_schreitbagger, 0.31, image_joy_L, 1, image_joy_R, 1]  # image Pfad, Skalierungsfaktor,......

    for i in range(1,int(len(image_input)/2 +1)):        #Schleife zur image Skalierung
        pil_image = Image.open(image_input[i*2-2])  # image laden
        x, y = pil_image.size	#Größe des Bilds
        skal = image_input[i*2-1]	#Skalierungsvaktor
        x_neu = int(x*skal) # skalierung x
        y_neu = int(y*skal) # skalierung y
        print("alte Bildgröße =", x, "x", y, "neue Bildgröße =", x_neu, "x", y_neu) # print size
        pil_image_neu = pil_image.resize((x_neu, y_neu), Image.ANTIALIAS)	#größenänderung auf X, Y
        pfad = image_input[i*2-2]
        pfad_neu = pfad.replace(".png", "_neu.png")
        pil_image_neu.save(pfad_neu) #speichern des geänderten Bildes
        print("File saved as %s" % pfad_neu)

    baggern_P = PhotoImage(file="/home/pi/Desktop/bagger/Grafiken/Schreitbagger_Baggern_V2_2_neu.png")     #Laden Bagger Zentralbild Funktion barggern_P
    Joy_L   = PhotoImage(file="/home/pi/Desktop/bagger/Grafiken/Baggern_links_neu.png")               #laden Bild Erklärung Steuerung Joystik Links
    Joy_R   = PhotoImage(file="/home/pi/Desktop/bagger/Grafiken/Baggern_rechts_neu.png")              #Laden Bild Erklärung Steuerung Joystik Rechts
   
    cv_w = m.winfo_screenwidth()                                                                                                 #Canvas/Fenster Breite
    cv_h =( m.winfo_screenheight()  -20)                                                                                               #Canvas/Fenster Höhe
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

    modus = IntVar()

    w = Canvas(m, width = cv_w, height = cv_h, bg = "black")                                                                  #Initialisierung Canvas (Grafische objekte)

    w.pack()

    w.create_rectangle(border, c_s_y, cv_w-border, cv_h-c_s_y-border, fill ="lightgray")                     #Initialisierung background für Steuerungserklärung
    w.create_oval(c_s_x,c_s_y, c_e_x, c_e_y, width = line_width*3, outline = "black", fill ="gray")                                       #Initialisierung Zentralkreis
    w.create_oval(c_s_x,c_s_y, c_e_x, c_e_y, width = line_width, outline = "blue" )                                       #Initialisierung Zentralkreis
    w.create_image(cv_w/2, cv_h/2, image = baggern_P)                                                             #Initialisierung Zentralbild
    w.create_image(c_s_x/2, cv_h/2, image = Joy_L)                                                              #Initialisierung Bild Erklärung Stererung Joystik Links
    w.create_image(cv_w - c_s_x/2, cv_h/2, image = Joy_R)                                                       #Initialisierung Bild Erklärung Stererung Joystik Rechts

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
    wartung.place(x=border, y=cv_h-1.5*border, anchor= SW)

    
    mainloop()

    logging.info("Bagger_GUI wurde geschlossen")
    
except Exception as e:
    e = str(e)
    logging.error(str(e))
    logging.info("Bagger_GUI wurde abgebrochen")
    print (e)
