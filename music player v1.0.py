import pygame
from pygame import mixer
from tkinter import*
import os
import time
import subprocess

mixer.init()

proc = subprocess.Popen(r "path of the timer.bat") #replace with the path of the timer.bat file

proc.terminate()

processo = subprocess.Popen(r "path of the resume_timer.bat", shell = True) #replace with the path of the resume_timer.bat file

processo.terminate()

canzone = ""

hotpoint = []

n = 0

a = pygame.mixer.music.get_pos()

finestra= Tk() 

finestra.geometry ("1200x600")
finestra.title ("Cdj Player")
finestra.configure(background="light blue")

scroll_bar = Scrollbar(finestra, orient = VERTICAL) 
scroll_bar.grid(row = 10, column = 4)

scroll_bar1 = Scrollbar(finestra, orient = VERTICAL) 
scroll_bar1.grid(row = 10, column = 9)

listbox = Listbox(finestra, height = 10,  
                  width = 30, 
                  yscrollcommand = scroll_bar.set, 
                  bg = "grey", 
                  activestyle = 'dotbox',  
                  font = "Helvetica", 
                  fg = "yellow")

listbox.grid(row = 10, column = 3)

listbox1 = Listbox(finestra, height = 10,  
                  width = 15, 
                  yscrollcommand = scroll_bar1, 
                  bg = "grey", 
                  activestyle = 'dotbox',  
                  font = "Helvetica", 
                  fg = "yellow")

listbox1.grid(row = 10, column = 8)

er = 0

os.chdir(r "path music_position") # replace with the path of the folder of the music to play

lista = os.listdir()

for i in range (0, len(lista)):

    item = lista[er]

    er += 1

    listbox.insert(er, item)

def load2 ():

    selection = Listbox.curselection(listbox)

    numero = selection[0]

    path_2 = lista[numero]

    percorso = r "path music_position" # replace with the path of the folder of the music to play 

    path = percorso + "\\" + path_2

    pygame.mixer.music.load(path)

    canzone = path_2

    print("\n\nSong Loaded!!")

    Loaded_song= Label(finestra, text = canzone, background = "light blue", font = 20)
    Loaded_song.grid(row=5, column=5)

    finestra.update_idletasks()

def queue(): # may this function not work, I will correct that issue as soon as possible!!

    selection = Listbox.curselection(listbox)

    numero = selection[0]

    path_2 = lista[numero]

    percorso = r "path music_position" # replace with the path of the folder of the music to play

    path = percorso + "\\" + path_2
 
    pygame.mixer.music.queue(path)

    canzone = path_2

    print ("\n\nSong Queued!!")

    Loaded_song= Label(finestra, text = canzone, background = "light blue", font = 20)
    Loaded_song.grid(row=5, column=5)

    finestra.update_idletasks()

def play_martingarrix():

    global proc

    proc.terminate()

    pygame.mixer.music.play(0)

    proc = subprocess.Popen(r "path of the timer.bat") #replace with the path of the timer.bat file

    print ("\n\nPlaying!!")

def remove_martingarrix(): # may this function not work, I will correct that issue as soon as possible!!

    global proc

    proc.terminate()

    pygame.mixer.music.unload()

def stop_martingarrix():

    global proc

    proc.terminate()

    pygame.mixer.music.stop()

def rewind_martingarrix():

    global proc

    proc.terminate()

    proc = subprocess.Popen(r "path of the timer.bat") #replace with the path of the timer.bat file

    pygame.mixer.music.rewind()

def pause_martingarrix():

    global proc

    proc.terminate()

    pygame.mixer.music.pause()

def resume_martingarrix():

    result_ms = pygame.mixer.music.get_pos()

    result_s = int(result_ms) / 1000

    result_m = int(result_s) / 60

    round(result_m, 0)

    if (result_m < 1):

        result_m = 0

    result_s1 = int(result_s)

    round(result_s1, 0)

    if (result_m < 10):

        result_m = "0" + str(result_m)

    if (result_s1 < 10):

        result_s1 = "0" + str(result_s1)

    result = str(result_m) + " : " + str(result_s1)

    result_pass = round(result_s, 0)

    res_pass = int(result_pass)

    f = open ("get_pos.txt", "w")

    f.write(str(res_pass))

    f.close()

    processo = subprocess.Popen(r "path of the resume_timer.bat", shell = True) #replace with the path of the resume_timer.bat file

    pygame.mixer.music.unpause()

    def pause_resume():

        processo.terminate()

        pygame.mixer.music.pause()

    pause_resumer = Button(finestra, text = "Pause Resume", command = pause_resume)
    pause_resumer.grid(row = 3, column = 7)

    finestra.update_idletasks()

def ctrl_volume():

    new_vol1 = sp1.get()

    new_vol = float(new_vol1)

    new_vol2 = "The volume is : " + str(new_vol) 

    pygame.mixer.music.set_volume(new_vol)

    volume = Label(finestra, text = new_vol2, background = "light blue", font = 20)
    volume.grid(row = 4, column = 9)

    finestra.update_idletasks()

    vol = pygame.mixer.music.get_volume()

    vol_impostato1 = round(vol, 1)

    vol_impostato = "The volume is : " + str(vol_impostato1) 

    volume = Label(finestra, text = vol_impostato, background = "light blue", font = 20)
    volume.grid(row = 3, column = 9)

    finestra.update_idletasks()

def HotPoint():

    global n

    hot1 = pygame.mixer.music.get_pos()

    hot = float(hot1) / 1000

    n += 1

    listbox1.insert(n, hot)

    return n

def Cue():

    global proc

    global processo

    proc.terminate()

    processo.kill()

    selection1 = Listbox.curselection(listbox1)

    selected = selection1[0]

    pos2 = listbox1.get(int(selected), int(selected))

    pos1 = pos2[0]

    pos = float(pos1)

    position = round(pos, 0)

    position_i = int(position)

    pygame.mixer.music.set_pos(pos)

    f1 = open ("get_pos.txt", "w")

    f1.write(str(position_i))

    f1.close()

    processo = subprocess.Popen(r "path of the resume_timer.bat", shell = True) #replace with the path of the resume_timer.bat file
    
    def pause_cue():

        processo.terminate()

        pygame.mixer.music.pause()

    pause_resumer = Button(finestra, text = "Pause Cue", command = pause_cue)
    pause_resumer.grid(row = 4, column = 7)

    finestra.update_idletasks()

def delete_Cue():

    selection2 = Listbox.curselection(listbox1)

    selected1 = selection2[0]

    listbox1.delete(selected1,selected1)

def get_volume():

    vol = pygame.mixer.music.get_volume()

    vol_impostato1 = round(vol, 1)

    vol_impostato = "The volume is : " + str(vol_impostato1)

    volume = Label(finestra, text = vol_impostato, background = "light blue", font = 20)
    volume.grid(row = 3, column = 9)

    finestra.update_idletasks()

sp1 = Spinbox(finestra, from_ = 0.0, to = 1.0, increment = 0.1)
sp1.grid(row = 8, column = 8)
load2 = Button(finestra, text = "Load by selection", command = load2)
load2.grid(row = 12, column = 3)
aggincoda2 = Button(finestra, text = "Aggincoda by selection", command = aggincoda)
aggincoda2.grid(row = 13, column = 3)
Play= Button(finestra,text='Play', command=play_martingarrix)
Play.grid(row=3, column = 1)
Remove= Button(finestra,text='Remove', command=remove_martingarrix)
Remove.grid(row=3, column = 2)
Stop= Button(finestra,text='Stop', command=stop_martingarrix)
Stop.grid(row=3, column = 3)
Rewind= Button(finestra,text='Rewind', command=rewind_martingarrix)
Rewind.grid(row=3, column = 4)
Pause= Button(finestra,text='Pause', command=pause_martingarrix)
Pause.grid(row=3, column = 5)
Resume= Button(finestra,text='Resume', command=resume_martingarrix)
Resume.grid(row=3, column = 6)
Loaded_song= Label(finestra, text = canzone, background = "light blue", font = 20)
Loaded_song.grid(row=5, column=5)
Control = Button(finestra, text = "Set Volume", command = ctrl_volume)
Control.grid(row = 4, column = 8)
Hotpoint = Button(finestra, text = "HotPoint", command = HotPoint)
Hotpoint.grid(row = 12, column = 8)
cue = Button(finestra, text = "Cue", command = Cue)
cue.grid(row = 13, column = 8)
Delete_cue = Button(finestra, text = "Delete Cue", command = delete_Cue)
Delete_cue.grid(row = 14, column = 8)
get_vol = Button(finestra, text = "Get Volume", command = get_volume)
get_vol.grid(row = 3, column = 8)
scroll_bar.config( command = listbox.yview ) 
scroll_bar1.config( command = listbox1.yview ) 
      
finestra.mainloop()
