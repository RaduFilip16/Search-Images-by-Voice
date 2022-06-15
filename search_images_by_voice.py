# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 19:27:45 2021

@author: filip
"""

import os
import speech_recognition as sr
from gtts import gTTS
import soundfile
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from tkinter import *
from tkinter import filedialog
from google_images_search import GoogleImagesSearch
import tkinter.font as font
import subprocess
from bing_images import bing
#from pydub import AudioSegment

# DEZARHIVATI IN ACELASI FISIER PROGRAMUL SI EXECUTABILUL CHROMEDRIVE.EXE SI INSTALATI MODULELE NECESARE
# Unzip this python file and the chromedriver in the same directory

# This application searches and downloads pictures using voice search
#You can either use Bing API(using ChromeDriver) or the Google Image Search API(it cannot download pngs or gifs)



# api key for the google custom seach api(create your own)
gis = GoogleImagesSearch('AIzaSyBaQuLDMEheK-l9OdS8tKkii1LPKDgUXCY', '75fc379c5f44b93f6')
rez = ''


def record():
    global rez
    print('Start recording')
    fs = 8000
    duration = 3
    myrecording = sd.rec(int(duration * fs),samplerate=fs, channels=1)
    sd.wait()
    wv.write('my_Audio_file.wav', myrecording, fs, sampwidth=2)
    cale = os.getcwd()
    mymono = os.path.join(cale, 'my_Audio_file.wav')
    data, samplerate = soundfile.read(mymono)
    # the audio file is converted to a compativle .wav file for speech recognition  ( pcm 16biti 8000hz)
    soundfile.write('new_Audio_file.wav', data, 8000, subtype='PCM_16')
    mymono = os.path.join(cale, 'new_Audio_file.wav')
    sprec = sr.Recognizer()
    myaudiofile = sr.AudioFile(mymono)
    
    with myaudiofile as source:
        myaudio = sprec.record(myaudiofile)
        rez = sprec.recognize_google(myaudio, language="en-US", show_all=False)
    print('Finish recording')


# functia care cauta si descarca pozele in functie de variabila globala rez(audio-ul transformat in string) is variabile introduse in GUI(numarul pozelor, dimensiune si tipu)
def search(smotor, snumar, sdimensiune, stip):
    global rez
    motor = smotor.get()
    if motor == 2:
        print('Searching')
        cale = os.getcwd()
        nr = snumar.get()
        dimensiune = sdimensiune.get()
        tip = stip.get()
        _search_params = {
            'q': rez,
            'num': nr,
            'safe': 'off',
            'fileType': tip,
            'imgType': 'photo',
            'imgSize': dimensiune,
           # 'imgDominantColor': 'blue',
           # 'imgColorType': 'color',
           # 'rights': 'cc_publicdomain'
        }
        
        gis.search(search_params=_search_params, path_to_dir=cale, 
                   custom_image_name='my_image')
        print('Finish searching')
    if motor == 1:
        cale = os.getcwd()
        nr = snumar.get()
        tip = stip.get()
        bing.download_images(rez,
                      nr,
                      output_dir=os.path.join(os.getcwd(), "bing-images"), 
                      pool_size=20,
                      file_type=tip,
                      #filters='+filterui:large',             
                      force_replace=False)


# functia care afiseaza imaginile 
def show(smotor, snumarPoze, stip):
    global rez
    cale = os.getcwd()
    nr = snumarPoze.get()
    motor = smotor.get()
    if motor == 2:
        for i in range(1, nr):
            os.startfile(cale + '/my_image(' + str(i) + ').jpg')
    if motor == 1:
        calebing = os.path.join(os.getcwd(), "bing-images/")
        tipbing = stip.get()
        #os.startfile(cale + rez + '.' + tipbing)
        for i in range(1, nr + 1):
            os.startfile(calebing + rez + '_' + str(i)+ '.' + tipbing)




main = Tk()
main.title("Voice image search")
main.geometry("390x300")
main.configure(bg = "#5d7db0")


numarPoze = IntVar()
numarPoze.set(1)
dimensiune = StringVar()
#default value  -> MEDIUM
dimensiune.set("MEDIUM")
tip = StringVar()
#default value -> jpg
tip.set("jpg")

motor = IntVar()
motor.set(1)

w1 = Label(main, text="Record:", bg = "#5d7db0")
w1.grid(row=0, column = 1, sticky = W, ipadx = 5 )


b1 = Button(main, text="Start", command=record, activebackground = "red",width = 7, bg = "#657185")
b1.grid(row=0, column=2, pady = 10)


#w2 = Label(main, text = "Motor cautare:", bg = "#5d7db0")
#w2.grid(row=1, column = 1, sticky = W, ipadx = 5)

rm1 = Radiobutton(main, text = "Bing", variable = motor, value = 1, bg = "#5d7db0" , activebackground = "#5d7db0")
rm1.grid(row = 1, column = 1, sticky = W)


rm2 = Radiobutton(main, text = "Google", variable = motor, value = 2, bg = "#5d7db0", activebackground = "#5d7db0" )
rm2.grid(row = 1, column = 2, sticky = W)

w3 = Label(main, text="Number of images:", bg = "#5d7db0")
w3.grid(row=2, column = 1, sticky = W, ipadx = 5)

e1 = Entry(main, textvariable = numarPoze)
e1.grid(row = 2, column = 2, pady = 10, sticky = W)


w3 = Label(main, text = "Dimension:", bg = "#5d7db0")
w3.grid(row = 4, column = 1, sticky = W, ipadx = 5)


r1 = Radiobutton(main, text = "small", variable = dimensiune, value = 'SMALL', bg = "#5d7db0" , activebackground = "#5d7db0")
r1.grid(row = 5, column = 1, sticky = W, ipadx = 5)


r2 = Radiobutton(main, text = "medium", variable = dimensiune, value = 'MEDIUM', bg = "#5d7db0", activebackground = "#5d7db0" )
r2.grid(row = 6, column = 1, sticky = W, ipadx = 5)

r3 = Radiobutton(main, text = "large", variable = dimensiune, value = 'LARGE', bg = "#5d7db0", activebackground = "#5d7db0" )
r3.grid(row = 7, column = 1, sticky = W, ipadx = 5)


w3 = Label(main, text = "Type:", bg = "#5d7db0")
w3.grid(row = 4, column = 2, sticky = W)

r1 = Radiobutton(main, text = "jpg", variable = tip, value = 'jpg', bg = "#5d7db0" , activebackground = "#5d7db0")
r1.grid(row = 5, column = 2, sticky = W)


r2 = Radiobutton(main, text = "gif", variable = tip, value = 'gif', bg = "#5d7db0", activebackground = "#5d7db0" )
r2.grid(row = 6, column = 2, sticky = W)

r3 = Radiobutton(main, text = "png", variable = tip, value = 'png', bg = "#5d7db0", activebackground = "#5d7db0" )
r3.grid(row = 7, column = 2, sticky = W)

b2 = Button(main, text="Search images", command =lambda:search(motor, numarPoze, dimensiune, tip), bg = "#657185", activebackground = "green",width = 10 )
b2.grid(row=10, column = 1,columnspan = 2, pady = 10, padx = 10, ipadx = 5)

b2 = Button(main, text="Show images", command =lambda:show(motor, numarPoze, tip), bg = "#657185", activebackground = "green",width = 10 )
b2.grid(row=11, column = 1,columnspan = 2, pady = 10, padx = 10, ipadx = 5)


main.mainloop()