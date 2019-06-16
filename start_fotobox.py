#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
from PIL import Image
import os, time, sys, random
from time import sleep
from picamera import PiCamera

#Bibliothek für Printer:
from Adafruit_Thermal import *
from os import listdir

import RPi.GPIO as GPIO

# Definiere Knopf:

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

#initialize camera
camera=PiCamera(resolution = (1920, 1080))

#camera.rotation = 180

# Some variables
photoPath = '/home/pi/photobox/fotos/'
photoName = time.strftime("%Y-%m-%d-%H-%M-%S") + "_fotobox.jpg"
photoResize = 512, 384
photoTitle = "Projekt " + time.strftime("%Y-%m-%d-%H-%M") + "\n Magga"
gewinnerTitle = " "

#define printer (19200 ist die baudrate (siehe tutorial))
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

#start camera preview (x,y,pixel,pixel)
camera.start_preview(fullscreen=False, window=(0,0,800,480))

# take picture
def take_photo():

    # Dateiname mit Zeitstempel:
    photoName = time.strftime("%Y-%m-%d-%H-%M-%S") + "_fotobox.jpg"
    
    #Mache das Foto, speichere in /home/pi/photobox/fotos/DATUM_fotobox.jpg
    camera.capture(photoPath+photoName)

    # GERADE gemachtes Foto öffnen, kleiner machen , sichern als "thumbnail.jpg" (wird immer überschrieben)
    Image.open(photoPath + photoName).resize(photoResize, Image.ANTIALIAS).save(photoPath + "thumbnail.jpg")


# Foto (thumbnail.jpg) wird geöffnet, gedreht, und gedruckt
def print_photo():
        # Foto öffnen, drehen, sichern als "thumbnail.rotated.jpg"
        Image.open(photoPath + "thumbnail.jpg").transpose(2).rotate(180).save(photoPath + "thumbnail-rotated.jpg")
        # Print the foto (thumbbnail.rotated)
        printer.begin(90)                       # Warmup time
        printer.setTimes(40000, 3000)           # Set print and feed times
        printer.justify('C')                    # Zentrieren (für text und foto aufm papier)

        #drucke fototitel
        printer.println(photoTitle)

        #drucke foto (öffne das thumbnail-rotated)
        printer.printImage(Image.open(photoPath + "thumbnail-rotated.jpg"), True)   # Specify image to print
        
        #eine leere zeile:
        printer.feed(1)



#MAIN Dauerschleife, warte auf Knopfdruck
while True: 

    # WENN Knopfdruck:
    if not GPIO.input(16):
        take_photo()        #DANN mache Foto
        print_photo()        #DANN druck das ganze

