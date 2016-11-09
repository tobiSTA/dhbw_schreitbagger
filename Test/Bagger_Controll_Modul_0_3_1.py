#!/usr/bin/python
#-*- coding: latin-1 -*-


"""
Bagger_Controll_Modul     V:0.3.1
Programm Modul zum aufsetzen der Befehle, welche zur Inbetriebnahme
und Steuerung des Baggers notwendig sind.
"""
import time
from RPi import GPIO
import pygame
#from nanpy import ArduinoApi
#from nanpy import SerialManager
from threading import *
import logging
import os
import datetime
from Tkinter import *

def horn():
    '''
    Funktion zum schalten des Relais für die Hupe des Baggers
    '''
    GPIO.output (11, False)
    time.sleep(1)
    GPIO.output (11, True)

def light():
    """
    Funktion zum schalten des Relais zur Bestromung des Scheinwerfersystems am Bagger
    """
    GPIO.output(13, not GPIO.input(13))
    

def taillight():
    """
    Funktion zum schalten des Relais zur Bestromung des Rücklichtsystems am Bagger
    """
    GPIO.output(19, not(GPIO.input(19)))
    
def FU():
    """
    Funktion zum Freischalten der Leistungsschaltung des Frequenzumrichters
    """
    GPIO.output(15, not(GPIO.input(15)))

def FU_reset():
    """
    Funktion zum restten des Frequenzumrichters
    """
    GPIO.output(15, False)
    time.sleep(2)
    GPIO.output(15, True)

def pump():
    """
    Funktion zum Starten der Entwässerungspumpe
    """
    GPIO.output(23, not(GPIO.input(23)))
    
def change_controler():
        '''
        Funktion zum wechseln des Eingabegeräts/Controlers
        '''
        global controler_state
        controler_state = not controler_state
        showinfo('Controler Change', ' Sie haben %s  als Controler ausgewählt' % (controler_list[controler_state]))
        logging.info('Controler wurde zu %s geändert' % (controler_list[controler_state]))

def Controler_read():   #es werden die Achspositionen ausgelesen und der Speed bestimmt.
        '''
        Funktion zum Lesen der Axpositionen der Controler in eine Matrix
        
        '''
        
        print("hallo")
        #while 1:
        for k in range (500):
                global controler_state
                global controler_pos
                global speed
                global Travel_max
                global DeadBand
                controler_state=False
                
                
            
                
                if speed > Travel_max:
                	speed = Travel_max


                if controler_state:
                	for i in range (4):
                                 
                		 controler_pos[i] = gamepad.get_axis(i)
                		 logging.info("Pad %f" %gamepad.get_axis(i))
                		 
                else:
                        for i in range (2):
                                controler_pos[i] = JS_1.get_axis(i)
                                
                                      
                                controler_pos[i+2] = JS_2.get_axis(i)
                                   
                                
                                                                
                                logging.info("ControlerPos: %f" %controler_pos[i])
                                logging.info("JsPos2: %f" %JS_2.get_axis(i))
                                logging.info("JsPos1: %f" %JS_1.get_axis(i))

                                
                                

                for i in (controler_pos):
                    if ((i < (-DeadBand)) | (i > DeadBand)):
                        i = int (i *speed)
                        logging.info("speed: %f%" %i)
                    else:
                        i = 0
                	
                time.sleep(BitTime)


    
                

def ValveStep(Valve_num):
        '''
        Funktion zur Befehlsgabe eines Schrittes der Ventile
        '''
        global Valve_pos
        lock.acquire()
        
        Arduino.digitalWrite(Valve_num*2, Arduino.HIGH)
        time.sleep(0.5* BitTime)
        Arduino.digitalWrite(Valve_num*2, Arduino.LOW)
        time.sleep(0.5*BitTime)
	
        if Arduino.digitalRead(Valve_num*2+1):                  #Auslesen der Step Direction
        	Valve_pos[Valve_num] = Valve_pos[Valve_num] +1
        else:	
        	Valve_pos[Valve_num] = Valve_pos[Valve_num] -1

        lock.release()
        
def ValveSetZero(Valve_num, log):
        '''
        Funktion zumsetzen der Ventile auf ihre Nullposition
        '''
        global ThreadCount
        lock.acquire()
        ThreadCount += 1
        log.info("starting to sett Valve number %d to Zero-Position" %Valve_num)
        lock.release()

        #Set Valve into upper Limit
        Arduino.digitalWrite((Valve_num*2+1), Arduino.HIGH)
        
        for i in range(int(Travel_max * 2.1)):
        	ValveStep(Valve_num)
        
        #move Valve to Zero-Position
        Arduino.digitalWrite((Valve_num*2+1), Arduino.LOW)
        
        for i in range(Travel_max):
        	ValveStep(Valve_num)
        
        global Valve_pos
        Valve_pos[Valve_num] = 0

        lock.acquire()
        ThreadCount -= 1
        log.info("Seting Valve number %d to Zero-Position" %Valve_num)
        lock.release()
        
def ValveSetPos(valve_num):
        '''
        Funktion zum setzen der Ventilposition in Relation zur Controler-Ax-Position
        '''
        
        global valve_n 
        global Valve_pos
        global Controler_pos        
        
        while 1:
                lock.acquire()
                valve_n = valve_num
                valve_poss = Valve_pos[valve_n]
                con_poss = controler_pos[valve_n]
                lock.release()
                
                if ((valve_poss != con_poss) & (con_poss == 0)):
                	ValveSetZero(valve_num)
                elif (valve_poss > con_poss):
                	Arduino.digitalWrite(valve_num*2+1, Arduino.LOW)
                	ValveStep(valve_num)			
                elif (valve_poss < con_poss):
                	Arduino.digitalWrite(valve_num*2+1, Arduino.HIGH)
                	ValveStep(valve_num)



sdir = "/home/pi/Bagger_Software"

if not os.path.exists(str(sdir + "/log")) :
    os.makedirs(str(sdir + "/log"))                                                       #anlegen Loggverzeichnis

dt = datetime.datetime.now()                                                                                #Auslesen der Aktuelllen Systemzeit

d = str(dt.strftime('%d-%m-%Y_%H-%M'))                                                                      #Zeit Formatierung

loggfile = str(sdir + "/log/bagger_GUI-log_" + d)                                  #Erstellung Logg-file-Adresse
logging.basicConfig(filename = loggfile, format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)   #initialiesierung der Log funktion
logging.info('Start des Moduls Bagger_Controll_Modul')
log = logging.getLogger()

lock = Lock()
ThreadCount = 0

Valve_amount = 4

GPIO_List =[11,13,15,19,21,23]
#Arduino_Pins = range(Valve_amount * 2)
controler_pos = [0,0,0,0]
Valve_pos = [0,0,0,0]
valve_n = 0

controler_list= {True: "Gamepad", False: "Joystik"}
controler_state = False

Travel_max = 31600
speed = 31600
acceleration = 100000.0
BitTime = 1/acceleration
logging.info("bittime: %f" %BitTime)
DeadBand = 0.05

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)                           #Initialisierung und Configuration der GPIO Einheit

#Initialisierung der einzelnen genutzten GPIO ports
GPIO.setup(GPIO_List, GPIO.OUT)   

GPIO.output(GPIO_List, True)
logging.info('RaspberryPi GPIO-Ports Initialized')

pygame.init()					#initialize pygame
pygame.joystick.init()				#initialize joysticks

#Zuweisung der Controler
for i in range(pygame.joystick.get_count()):
        if 'Gamepad' in pygame.joystick.Joystick(i).get_name():
        	gamepad = pygame.joystick.Joystick(i)
        	gamepad.init()
        	logging.info(gamepad)
        elif 'Logitech' in pygame.joystick.Joystick(i).get_name():
        	JS_1 = pygame.joystick.Joystick(i)
        	JS_1.init()
        	logging.info(JS_1)
               
                    
        else:
                JS_2 = pygame.joystick.Joystick(i)
                JS_2.init()
                logging.info(JS_2)


#if (JS_2.get_init()& JS_1.get_init
                #print("2. initialisiert")
#logging.info('Controler Initialized')

#con = SerialManager(device = '/dev/ttyACM0')
#Arduino = ArduinoApi(connection = con)
#logging.info('Arduino conection Initialized')

#Initialisierung der GPIO-Ports des Arduino
#Arduino.pinMode(Arduino_Pins, Arduino.OUTPUT)
#logging.info('Arduino GPIO-Ports Initialized')


#                                                               
#setting all valves to Zero-Poss
#for Valve_num in range(Valve_amount):
#    t = Thread(target = ValveSetZero, args = (Valve_num, log))
#    t.start()



    
    
    
#while ThreadCount != 0:
#    time.sleep(0.5)

# Thread in dem die Controller kontinuierlich ausgelesen werden
t1=Thread(target = Controler_read)
t1.start()




# Threads in denen die Ventilstellungen mit der Controllerpositionen verglichen und angesteuert werden
#for Valve_num in range(Valve_amount):
#    t_valves=Thread(target=ValveSetPos,args = (Valve_num,))     #er will hier ein toupel deswegen das "," nach Valve_num (??)
#    t_valves.start()
       
    
    






    
    

    
