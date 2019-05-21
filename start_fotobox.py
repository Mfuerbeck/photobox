#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
from PIL import Image
import os, time, sys, random
from os.path import isfile, join
import pygame
from time import sleep
from picamera import PiCamera

#Bibliothek für Printer:
from Adafruit_Thermal import *
from os import listdir

#initialize camera
camera=PiCamera(resolution = (1920, 1080))

#camera.rotation = 180

# Some variables
photoPath = '/home/pi/photobox/fotos/'
photoName = time.strftime("%Y-%m-%d-%H-%M-%S") + "_fotobox.jpg"
photoResize = 512, 384
photoTitle = "Projekt " + time.strftime("%Y-%m-%d-%H-%M") + "\n Magga"
gewinnerTitle = " "

#define printer
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

#start camera preview
camera.start_preview(fullscreen=False, window=(0,0,800,480))

#init pygame for mouseclick (to take foto - ersetzbar durch Knopfdruck)
pygame.init()

# take picture & save to photoPath (see variabled)
def photo_callback():

    # Define filename with timestamp
    photoName = time.strftime("%Y-%m-%d-%H-%M-%S") + "_fotobox.jpg"
    
    #take a picture
    camera.capture(photoPath+photoName)

    # Resize the high res photo to create thumbnail
    Image.open(photoPath + photoName).resize(photoResize, Image.ANTIALIAS).save(photoPath + "thumbnail.jpg")


# open the picture taken in photo_callback & print it using the adafruit printer.
def print_callback():
        # Rotate the thumbnail for printing
        Image.open(photoPath + "thumbnail.jpg").transpose(2).rotate(180).save(photoPath + "thumbnail-rotated.jpg")
        # Print the foto
        printer.begin(90)                       # Warmup time
        printer.setTimes(40000, 3000)           # Set print and feed times
        printer.justify('C')                    # Center alignment
        printer.println(photoTitle)
        printer.printImage(Image.open(photoPath + "thumbnail-rotated.jpg"), True)   # Specify image to print
        printer.feed(1)



#MAIN Dauerschleife
while True: 
    #WARTE auf ein Ereignis:
    for event in pygame.event.get():        
        if(event.type == pygame.MOUSEBUTTONDOWN):   # WENN Knopf gedrückt wird
            photo_callback()        #DANN mache Foto
            print_callback()        #DANN druck das ganze
            pygame.event.clear()    #lösche alles, beginne wieder mit warten auf Knopfdruck
