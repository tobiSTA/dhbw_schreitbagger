#!/usr/bin/python
#-*- coding: latin-1 -*-


"""
Controll_red-Test

Dieses Modul dient der Überprüfung der Funktionalität des Controlerauslesens Mittels Pygame
dazu sollen die Achsen der Controler in einem Logfile Wiedergegeben werden.
"""
import time
import pygame
from threading import *
import logging
import os
import datetime

def Controler_read():   #es werden die Achspositionen ausgelesen und der Speed bestimmt.
    '''
    Funktion zum Lesen der Axpositionen der Controler
    '''
	
    global ThreadCount
	ThreadCount +=1

	for i in range (500):
		lock.aquire()

		logging.info("%s\n" %gamepad.get_name)
		for i in range (gamepad.numaxes):
		    	axes = gamepad.get_axis(i)
			logging.info("   Axe %d %f\n" %i, axes)

		logging.info("%s\n" %JS_1.get_name)
		for i in range (JS_1.numaxes):
		    	axes = JS_1.get_axis(i)
			logging.info("   Axe %d %f\n" %i, axes)

		logging.info("%s\n" %JS_2.get_name)
        	for i in range (JS_2.numaxes):
		    	axes = JS_2.get_axis(i)
            		logging.info("   Axe %d %f\n" %i, axes)

		time.sleep(BitTime)

		lock.release()

	ThreadCount -=1

sdir = ""

if not os.path.exists(str(sdir + "/log")) :
    os.makedirs(str(sdir + "/log"))                                                       #anlegen Loggverzeichnis

dt = datetime.datetime.now()                                                                                #Auslesen der Aktuelllen Systemzeit

d = str(dt.strftime('%d-%m-%Y_%H-%M'))                                                                      #Zeit Formatierung

loggfile = str(sdir + "/log/bControler_read_log_" + d)                                  #Erstellung Logg-file-Adresse
logging.basicConfig(filename = loggfile, format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)   #initialiesierung der Log funktion
logging.info('Start des Moduls Bagger_Controll_Modul')
log = logging.getLogger()

lock = Lock()
ThreadCount = 0

BitTime = 0.2
logging.info("bittime: %f" %BitTime)


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


if (JS_2.get_init())
	logging.info("JS_2 initialisiert")


if (JS_1.get_init())
	logging.info("JS_1 initialisiert")


if (gamepad.get_init())
	logging.info("gamepad initialisiert")
logging.info('Controler Initialized')


Controler_read()

logging.info("Reading in Thread")

t1=Thread(target = Controler_read)
t1.start()

while ThreadCount != 0:
	time.sleep(0.5)

pygame.quit()

logging.info("done")
