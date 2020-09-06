import pygame
from pygame import mixer
from tkinter import*
import os
import time
import subprocess
from aubio import source, tempo
from numpy import median, diff
import scipy.io.wavfile
import matplotlib.pyplot as plt
from tkinter import*
from mutagen.mp3 import MP3
from tkinter.ttk import *
from os import path
from pydub import AudioSegment

mixer.init()

proc = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\timer.bat") 

proc.terminate()

processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True) #replace with the path of the resume_timer.bat file

processo.terminate()

canzone = ""

new_file_save = ""

len_s = 0

hotpoint = []

n = 0

a = pygame.mixer.music.get_pos()

finestra= Tk() 

finestra.geometry ("1500x550")
finestra.title ("Cdj Player")
finestra.configure(background="light blue")

scroll_bar = Scrollbar(finestra, orient = VERTICAL) 
scroll_bar.grid(row = 10, column = 2)

scroll_bar1 = Scrollbar(finestra, orient = VERTICAL) 
scroll_bar1.grid(row = 10, column = 5)

listbox = Listbox(finestra, height = 10,  
                  width = 30, 
                  yscrollcommand = scroll_bar.set, 
                  bg = "grey", 
                  activestyle = 'dotbox',  
                  font = "Helvetica", 
                  fg = "yellow")

listbox.grid(row = 10, column = 1)

listbox1 = Listbox(finestra, height = 10,  
                  width = 15, 
                  yscrollcommand = scroll_bar1, 
                  bg = "grey", 
                  activestyle = 'dotbox',  
                  font = "Helvetica", 
                  fg = "yellow")

listbox1.grid(row = 10, column = 4)

er = 0

try:

    os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

except BaseException:

    print("")

durate = []

lista_canzoni = []

os.chdir(r"C:\Users\Emanuele\Desktop\python\progetti\Chiavetta USB") 

lista = os.listdir()

for i in range (0, len(lista)):

    item = lista[er]

    er += 1

    listbox.insert(er, item)

n_song = 0

n_pause = 0

bpm = 0 

b_pmer = []

def add(): 

    selection = Listbox.curselection(listbox)

    numero = selection[0]

    pather = lista[numero]

    lista_canzoni.append(str(pather))

    canzone = "In queue: " + str(pather)
    
    Loaded_song= Label(finestra, text = "                                  ", background = "light blue", font = 20)
    Loaded_song.grid(row=6, column=3)

    finestra.update_idletasks()

    Loaded_song= Label(finestra, text = canzone, background = "light blue", font = 20)
    Loaded_song.grid(row=6, column=3)

    finestra.update_idletasks()
    
    return lista_canzoni
    
def play ():

    global lista_canzoni

    global n_song
    
    global proc

    proc.terminate()
    
    path_2 = lista_canzoni[n_song]
    
    percorso = r"C:\Users\Emanuele\Desktop\python\progetti\Chiavetta USB" # replace with the path of the folder of the music to play 

    path = percorso + "\\" + path_2

    pygame.mixer.music.load(path)

    canzone = "Playing: " + str(path_2)

    Loaded_song= Label(finestra, text = "                                                          ", background = "light blue", font = 20)
    Loaded_song.grid(row=5, column=3)

    finestra.update_idletasks()

    Loaded_song= Label(finestra, text = canzone, background = "light blue", font = 20)
    Loaded_song.grid(row=5, column=3)

    finestra.update_idletasks()

    file_name = path_2
                                                                        
    file_wav = file_name.replace(".mp3", ".wav")
    
    file = percorso + "\\" + file_wav 

    file1 = percorso + "\\" + file_name
    
    src = file1
    dst = file
                                       
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    
    audio = MP3(file1)

    len_s = audio.info.length

    len_w = int(len_s)

    durate.append(len_w)

    n_song += 1

    f = open(r"C:\Users\Emanuele\Desktop\python\progetti\duration.txt", "w")

    f.write(str(len_w))

    f.close()

    rate, data = scipy.io.wavfile.read(file)
     
    plt.plot(data)

    save_path = r"C:\Users\Emanuele\Desktop\python\progetti"

    file_save = save_path + "\\" + (file_wav.replace(".wav", ""))

    plt.savefig(file_save, orientation='portrait')

    from PIL import Image, ImageTk

    new_file_save = file_save + ".png"

    im = Image.open(new_file_save) 
      
    width, height = im.size 
      
    x1 = 81

    y1 = 53

    x2 = width - 80

    y2 = height - 53

    im1 = im.crop((x1, y1, x2, y2)) 

    im1.save(new_file_save)

    im.close()

    import PIL

    basewidth = 300
    img1 = Image.open(new_file_save)
    wpercent = (basewidth / float(img1.size[0]))
    hsize = int((float(img1.size[1]) * float(wpercent)))
    img2 = img1.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    img2.save(new_file_save)

    path = file

    params = None

    if params is None:
        params = {}
    try:
        win_s = params['win_s']
        samplerate = params['samplerate']
        hop_s = params['hop_s']
    except KeyError:
        """
        # super fast
        samplerate, win_s, hop_s = 4000, 128, 64 
        # fast
        samplerate, win_s, hop_s = 8000, 512, 128
        """

        try:

            # default:
            samplerate, win_s, hop_s = 44100, 1024, 512

            s = source(path, samplerate, hop_s)
            samplerate = s.samplerate
            o = tempo("specdiff", win_s, hop_s, samplerate)
            # List of beats, in samples
            beats = []
            # Total number of frames read
            total_frames = 0

        except RuntimeError:
 
            # default:
            samplerate, win_s, hop_s = 48000, 1024, 512

            s = source(path, samplerate, hop_s)
            samplerate = s.samplerate
            o = tempo("specdiff", win_s, hop_s, samplerate)
            # List of beats, in samples
            beats = []
            # Total number of frames read
            total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    # Convert to periods and to bpm 
    if len(beats) > 1:
        if len(beats) < 4:
            print("few beats found in {:s}".format(path))
        bpms = 60./diff(beats)
        b = median(bpms)
        bpm = round(b, None)
        
    else:
        b = 0
        print("not enough beats found in {:s}".format(path))

    bpm_show = int(bpm)

    len_m = 0

    len_sec1 = len_s

    while (int(len_sec1) >= 60):

        len_m += 1

        len_sec1 = len_sec1 - 60

    len_sec = int(len_sec1)

    if (len_m < 10):

        len_m = "0" + str(len_m)
        
        if (len_sec < 10):

            len_sec = "0" + str(len_sec)

    duration_song = str(len_m) + " : " + str(len_sec)

    bpmer = Label(finestra, text = str(bpm), background = "light blue", font = 20)
    bpmer.grid(row = 7, column = 3) 

    duration = Label(finestra, text = duration_song, background = "light blue", font = 20)
    duration.grid(row = 8, column = 3)

    photo = ImageTk.PhotoImage(file = new_file_save, master=finestra) 
    panel = Label(finestra, image = photo)
    panel.image = photo
    panel.grid(row = 10, column = 3, padx = 20)

    finestra.update_idletasks()

    b_pmer.append(bpm)

    pygame.mixer.music.play(0)

    proc = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\timer.bat") #replace with the path of the timer.bat file

    return durate, n_song, b_pmer

def remove_martingarrix(): 

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

    proc = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\timer.bat") #replace with the path of the timer.bat file

    pygame.mixer.music.rewind()

def pause_martingarrix():

    global proc

    proc.terminate()

    pygame.mixer.music.pause()

def resume_martingarrix():

    global durate

    global n_song

    global n_pause

    result_ms = pygame.mixer.music.get_pos()

    result_s = int(result_ms) / 1000

    result_pass = round(result_s, 0)

    res_pass = int(result_pass)

    n_song_r = n_song - 1

    if (n_pause >= 1):

        f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

        f3.write("3")

        f3.close()

    len_seconds = durate[n_song_r]

    f = open (r"C:\Users\Emanuele\Desktop\python\progetti\get_pos.txt", "w")

    f.write(str(res_pass))

    f.close()

    n_loop = int(len_seconds) - int(res_pass)

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\n_loop.txt", "w")

    f1.write(str(n_loop))

    f1.close()  

    if (n_pause >= 1):

        time.sleep(1)

        print ("elimino il .txt di blocco!!")

        os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    n_pause += 1
    
    processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True) #replace with the path of the resume_timer.bat file

    pygame.mixer.music.unpause()

    def pause_resume():

        processo.terminate()

        pygame.mixer.music.pause()

    pause_resumer = Button(finestra, text = "Pause Resume", command = pause_resume)
    pause_resumer.grid(row = 4, column = 6)

    finestra.update_idletasks()

    return n_pause

def ctrl_volume():

    new_vol1 = sp1.get()

    new_vol = float(new_vol1)

    new_vol2 = "The volume is : " + str(new_vol) 

    pygame.mixer.music.set_volume(new_vol)

    volume = Label(finestra, text = new_vol2, background = "light blue", font = 15)
    volume.grid(row = 10, column = 8)

    finestra.update_idletasks()

    vol = pygame.mixer.music.get_volume()

    vol_impostato1 = round(vol, 1)

    vol_impostato = "The volume is : " + str(vol_impostato1) 

    volume = Label(finestra, text = vol_impostato, background = "light blue", font = 15)
    volume.grid(row = 9, column = 8)

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

    global durate

    global n_song

    global n_pause

    proc.terminate()

    n_song_c = n_song - 1

    if (n_pause >= 1):

        print ("attivo il .txt di blocco!!")

        f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

        f3.write("3")

        f3.close()
 
    selection1 = Listbox.curselection(listbox1)

    selected = selection1[0]

    pos2 = listbox1.get(int(selected), int(selected))

    pos1 = pos2[0]

    pos = float(pos1)

    position = round(pos, 0)

    position_i = int(position)

    len_seconds = durate[n_song_c]

    pygame.mixer.music.set_pos(pos)

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\get_pos.txt", "w")

    f1.write(str(position_i))

    f1.close()

    n_loop = int(len_seconds) - int(position_i)

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\n_loop.txt", "w")

    f1.write(str(n_loop))

    f1.close()

    if (n_pause >= 1):

        time.sleep(1)

        print ("elimino il .txt di blocco!!")

        os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True) #replace with the path of the resume_timer.bat file
    
    n_pause += 1

    def pause_cue():

        processo.terminate()

        pygame.mixer.music.pause()

    pause_resumer = Button(finestra, text = "Pause Cue", command = pause_cue)
    pause_resumer.grid(row = 4, column = 7)

    finestra.update_idletasks()

    return n_pause

def delete_Cue():

    selection2 = Listbox.curselection(listbox1)

    selected1 = selection2[0]

    listbox1.delete(selected1,selected1)

def get_volume():

    vol = pygame.mixer.music.get_volume()

    vol_impostato1 = round(vol, 1)

    vol_impostato = "The volume is : " + str(vol_impostato1)

    volume = Label(finestra, text = vol_impostato, background = "light blue", font = 15)
    volume.grid(row = 9, column = 8)

    finestra.update_idletasks()

def all_loop():
    
    global proc

    global n_pause

    global durate

    global n_song

    global b_pmer

    proc.terminate()

    if (n_pause >= 1):

        f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

        f3.write("3")

        f3.close()
    
    n_song_bpm = n_song - 1

    bpm1 = b_pmer[n_song_bpm]

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    tot_loop = 0

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):
        
        time.sleep(beat)

        pygame.mixer.music.set_pos(loop_get_pos)

    n_song_r = n_song - 1

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    len_seconds = durate[n_song_r]

    f = open (r"C:\Users\Emanuele\Desktop\python\progetti\get_pos.txt", "w")

    f.write(str(res_pass))

    f.close()

    n_loop = int(len_seconds) - int(res_pass)

    res_pass_m = 0 

    while (res_pass >= 60):

        res_pass_sec = res_pass - 60

        res_pass_m += 1

    if (res_pass_m < 10):

        res_pass_m = "0" + str(res_pass_m)

        if (res_pass_sec < 10):

            res_pass_sec = "0" + str(res_pass_sec)

    print(str(res_pass_m) + " : " + str(res_pass_sec))

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\n_loop.txt", "w")

    f1.write(str(n_loop))

    f1.close()

    if (n_pause >= 1):

        time.sleep(1)

        os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    n_pause += 1

    processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True)

    return n_pause

def half_loop():

    global proc

    global n_pause

    global durate

    global n_song

    global b_pmer

    proc.terminate()

    if (n_pause >= 1):

        f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

        f3.write("3")

        f3.close()
    
    n_song_bpm = n_song - 1

    bpm1 = b_pmer[n_song_bpm]

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/2
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    n_song_r = n_song - 1

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    len_seconds = durate[n_song_r]

    f = open (r"C:\Users\Emanuele\Desktop\python\progetti\get_pos.txt", "w")

    f.write(str(res_pass))

    f.close()

    n_loop = int(len_seconds) - int(res_pass)

    res_pass_m = 0

    while (res_pass >= 60):

        res_pass_sec = res_pass - 60

        res_pass_m += 1

    if (res_pass_m < 10):

        res_pass_m = "0" + str(res_pass_m)

        if (res_pass_sec < 10):

            res_pass_sec = "0" + str(res_pass_sec)

    print(str(res_pass_m) + " : " + str(res_pass_sec))

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\n_loop.txt", "w")

    f1.write(str(n_loop))

    f1.close()

    if (n_pause >= 1):

        time.sleep(1)

        os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    n_pause += 1

    processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True)

    return n_pause

def quarter_loop():

    global proc

    global n_pause

    global durate

    global n_song

    global b_pmer

    proc.terminate()

    if (n_pause >= 1):

        f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

        f3.write("3")

        f3.close()
    
    n_song_bpm = n_song - 1

    bpm1 = b_pmer[n_song_bpm]

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/4
        
        print(waiter_time)
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    n_song_r = n_song - 1

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    len_seconds = durate[n_song_r]

    f = open (r"C:\Users\Emanuele\Desktop\python\progetti\get_pos.txt", "w")

    f.write(str(res_pass))

    f.close()

    n_loop = int(len_seconds) - int(res_pass)

    res_pass_m = 0

    while (res_pass >= 60):

        res_pass_sec = res_pass - 60

        res_pass_m += 1

    if (res_pass_m < 10):

        res_pass_m = "0" + str(res_pass_m)

        if (res_pass_sec < 10):

            res_pass_sec = "0" + str(res_pass_sec)

    print(str(res_pass_m) + " : " + str(res_pass_sec))

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\n_loop.txt", "w")

    f1.write(str(n_loop))

    f1.close()

    if (n_pause >= 1):

        time.sleep(1)

        os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    n_pause += 1

    processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True)

    return n_pause

def eight_loop():

    global proc

    global n_pause

    global durate

    global n_song

    global b_pmer

    proc.terminate()

    if (n_pause >= 1):

        f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

        f3.write("3")

        f3.close()
    
    n_song_bpm = n_song - 1

    bpm1 = b_pmer[n_song_bpm]

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/8
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    n_song_r = n_song - 1

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    len_seconds = durate[n_song_r]

    f = open (r"C:\Users\Emanuele\Desktop\python\progetti\get_pos.txt", "w")

    f.write(str(res_pass))

    f.close()

    n_loop = int(len_seconds) - int(res_pass)

    res_pass_m = 0

    while (res_pass >= 60):

        res_pass_sec = res_pass - 60

        res_pass_m += 1

    if (res_pass_m < 10):

        res_pass_m = "0" + str(res_pass_m)

        if (res_pass_sec < 10):

            res_pass_sec = "0" + str(res_pass_sec)

    print(str(res_pass_m) + " : " + str(res_pass_sec))

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\n_loop.txt", "w")

    f1.write(str(n_loop))

    f1.close()

    if (n_pause >= 1):

        time.sleep(1)

        os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    n_pause += 1

    processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True)

    return n_pause

def sixteen_loop():

    global proc

    global n_pause

    global durate

    global n_song

    global b_pmer

    proc.terminate()

    if (n_pause >= 1):

        f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

        f3.write("3")

        f3.close()
    
    n_song_bpm = n_song - 1

    bpm1 = b_pmer[n_song_bpm]

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/16
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    n_song_r = n_song - 1

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    len_seconds = durate[n_song_r]

    f = open (r"C:\Users\Emanuele\Desktop\python\progetti\get_pos.txt", "w")

    f.write(str(res_pass))

    f.close()

    n_loop = int(len_seconds) - int(res_pass)

    res_pass_m = 0

    while (res_pass >= 60):

        res_pass_sec = res_pass - 60

        res_pass_m += 1

    if (res_pass_m < 10):

        res_pass_m = "0" + str(res_pass_m)

        if (res_pass_sec < 10):

            res_pass_sec = "0" + str(res_pass_sec)

    print(str(res_pass_m) + " : " + str(res_pass_sec))

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\n_loop.txt", "w")

    f1.write(str(n_loop))

    f1.close()

    if (n_pause >= 1):

        time.sleep(1)

        os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    n_pause += 1

    processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True)

    return n_pause

def thirtytwo_loop():

    global proc

    global n_pause

    global durate

    global n_song

    global b_pmer

    proc.terminate()

    if (n_pause >= 1):

        f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

        f3.write("3")

        f3.close()
    
    n_song_bpm = n_song - 1

    bpm1 = b_pmer[n_song_bpm]

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/32
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    n_song_r = n_song - 1

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    len_seconds = durate[n_song_r]

    f = open (r"C:\Users\Emanuele\Desktop\python\progetti\get_pos.txt", "w")

    f.write(str(res_pass))

    f.close()

    n_loop = int(len_seconds) - int(res_pass)

    res_pass_m = 0

    while (res_pass >= 60):

        res_pass_sec = res_pass - 60

        res_pass_m += 1

    if (res_pass_m < 10):

        res_pass_m = "0" + str(res_pass_m)

        if (res_pass_sec < 10):

            res_pass_sec = "0" + str(res_pass_sec)

    print(str(res_pass_m) + " : " + str(res_pass_sec))

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\n_loop.txt", "w")

    f1.write(str(n_loop))

    f1.close()

    if (n_pause >= 1):

        time.sleep(1)

        os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    n_pause += 1

    processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True)

    return n_pause

def sixtyfour_loop():

    global proc

    global n_pause

    global durate

    global n_song

    global b_pmer

    proc.terminate()

    if (n_pause >= 1):

        f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

        f3.write("3")

        f3.close()
    
    n_song_bpm = n_song - 1

    bpm1 = b_pmer[n_song_bpm]

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/64
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    n_song_r = n_song - 1

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    len_seconds = durate[n_song_r]

    f = open (r"C:\Users\Emanuele\Desktop\python\progetti\get_pos.txt", "w")

    f.write(str(res_pass))

    f.close()

    n_loop = int(len_seconds) - int(res_pass)

    res_pass_m = 0

    while (res_pass >= 60):

        res_pass_sec = res_pass - 60

        res_pass_m += 1

    if (res_pass_m < 10):

        res_pass_m = "0" + str(res_pass_m)

        if (res_pass_sec < 10):

            res_pass_sec = "0" + str(res_pass_sec)

    print(str(res_pass_m) + " : " + str(res_pass_sec))

    f1 = open (r"C:\Users\Emanuele\Desktop\python\progetti\n_loop.txt", "w")

    f1.write(str(n_loop))

    f1.close()

    if (n_pause >= 1):

        time.sleep(1)

        os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    n_pause += 1

    processo = subprocess.Popen(r"C:\Users\Emanuele\Desktop\python\progetti\resume_timer.bat", shell = True)

    return n_pause

def exiter_c():

    global proc

    proc.terminate()

    f3 = open(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt", "w")

    f3.write("3")

    f3.close()

    time.sleep(1)

    os.remove(r"C:\Users\Emanuele\Desktop\python\progetti\fermati.txt")

    finestra.quit()

def show_preview(): # this function is raccomended to use at the song pause, because it will eventually stop the song
    
    global lista_canzoni

    global n_song
    
    path_2 = lista_canzoni[n_song]
    
    percorso = r"C:\Users\Emanuele\Desktop\python\progetti\Chiavetta USB" # replace with the path of the folder of the music to play 

    path = percorso + "\\" + path_2

    pygame.mixer.music.load(path)

    canzone = "Previewing: " + str(path_2)

    file_name = path_2
                                                                        
    file_wav = file_name.replace(".mp3", ".wav")
    
    file = percorso + "\\" + file_wav 

    file1 = percorso + "\\" + file_name
    
    src = file1
    dst = file
                                       
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    
    audio = MP3(file1)

    len_s = audio.info.length

    len_w = int(len_s)

    durate.append(len_w)

    rate, data = scipy.io.wavfile.read(file)
     
    plt.plot(data)

    save_path = r"C:\Users\Emanuele\Desktop\python\progetti"

    file_save = save_path + "\\" + (file_wav.replace(".wav", ""))

    plt.savefig(file_save, orientation='portrait')

    from PIL import Image, ImageTk

    new_file_save = file_save + ".png"

    im = Image.open(new_file_save) 
      
    width, height = im.size 
      
    x1 = 81

    y1 = 53

    x2 = width - 80

    y2 = height - 53

    im1 = im.crop((x1, y1, x2, y2)) 

    im1.save(new_file_save)

    im.close()

    import PIL

    basewidth = 300
    img1 = Image.open(new_file_save)
    wpercent = (basewidth / float(img1.size[0]))
    hsize = int((float(img1.size[1]) * float(wpercent)))
    img2 = img1.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    img2.save(new_file_save)

    path = file

    params = None

    if params is None:
        params = {}
    try:
        win_s = params['win_s']
        samplerate = params['samplerate']
        hop_s = params['hop_s']
    except KeyError:
        """
        # super fast
        samplerate, win_s, hop_s = 4000, 128, 64 
        # fast
        samplerate, win_s, hop_s = 8000, 512, 128
        """

        try:

            # default:
            samplerate, win_s, hop_s = 44100, 1024, 512

            s = source(path, samplerate, hop_s)
            samplerate = s.samplerate
            o = tempo("specdiff", win_s, hop_s, samplerate)
            # List of beats, in samples
            beats = []
            # Total number of frames read
            total_frames = 0

        except RuntimeError:
 
            # default:
            samplerate, win_s, hop_s = 48000, 1024, 512

            s = source(path, samplerate, hop_s)
            samplerate = s.samplerate
            o = tempo("specdiff", win_s, hop_s, samplerate)
            # List of beats, in samples
            beats = []
            # Total number of frames read
            total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    # Convert to periods and to bpm 
    if len(beats) > 1:
        if len(beats) < 4:
            print("few beats found in {:s}".format(path))
        bpms = 60./diff(beats)
        b = median(bpms)
        bpm = round(b, None)
        
    else:
        b = 0
        print("not enough beats found in {:s}".format(path))

    bpm_show = int(bpm)

    len_m = 0

    len_sec1 = len_s

    while (int(len_sec1) >= 60):

        len_m += 1

        len_sec1 = len_sec1 - 60

    len_sec = int(len_sec1)

    if (len_m < 10):

        len_m = "0" + str(len_m)
        
        if (len_sec < 10):

            len_sec = "0" + str(len_sec)

    duration_song = str(len_m) + " : " + str(len_sec)

    track_name = Label(finestra, text = canzone, background = "light blue", font = 20)
    track_name.grid(row = 5, column = 3)

    bpmer = Label(finestra, text = str(bpm), background = "light blue", font = 20)
    bpmer.grid(row = 8, column = 3)

    duration = Label(finestra, text = duration_song, background = "light blue", font = 20)
    duration.grid(row = 7, column = 3)

    photo = ImageTk.PhotoImage(file = new_file_save, master=finestra) 
    panel = Label(finestra, image = photo)
    panel.image = photo
    panel.grid(row = 10, column = 3, padx = 20)

    finestra.update_idletasks()

sp1 = Spinbox(finestra, from_ = 0.0, to = 1.0, increment = 0.1)
sp1.grid(row = 8, column = 8)
sp2 = Spinbox(finestra, from_ = 0, to = 30)
sp2.grid(row = 15, column = 2, pady = 5)
aggincoda2 = Button(finestra, text = "Add by selection", command = add)
aggincoda2.grid(row = 12, column = 1)
Play= Button(finestra,text='Play', command=play)
Play.grid(row = 3, column = 1)
Remove= Button(finestra,text='Remove', command=remove_martingarrix)
Remove.grid(row = 3, column = 2)
Stop= Button(finestra,text='Stop', command=stop_martingarrix)
Stop.grid(row = 3, column = 3)
Rewind= Button(finestra,text='Rewind', command=rewind_martingarrix)
Rewind.grid(row = 3, column = 4)
Pause= Button(finestra,text='Pause', command=pause_martingarrix)
Pause.grid(row = 3, column = 5)
Resume= Button(finestra,text='Resume', command=resume_martingarrix)
Resume.grid(row = 3, column = 6)
Loaded_song= Label(finestra, text = canzone, background = "light blue", font = 20)
Loaded_song.grid(row = 5, column = 3)
Control = Button(finestra, text = "Set Volume", command = ctrl_volume)
Control.grid(row = 4, column = 8)
Hotpoint = Button(finestra, text = "HotPoint", command = HotPoint)
Hotpoint.grid(row = 12, column = 4)
cue = Button(finestra, text = "Cue", command = Cue)
cue.grid(row = 13, column = 4)
Delete_cue = Button(finestra, text = "Delete Cue", command = delete_Cue)
Delete_cue.grid(row = 14, column = 4)
get_vol = Button(finestra, text = "Get Volume", command = get_volume)
get_vol.grid(row = 3, column = 8)

scroll_bar.config( command = listbox.yview ) 
scroll_bar1.config( command = listbox1.yview ) 

all_l = Button(finestra,text = "Loop" , command = all_loop)
all_l.grid(row = 15, column = 1)
half = Button(finestra, text = "1/2", command = half_loop)
half.grid(row = 13, column = 1)
quarter = Button(finestra, text = "1/4", command = quarter_loop)
quarter.grid(row = 13, column = 2)
eight = Button(finestra, text = "1/8", command = eight_loop)
eight.grid(row = 13, column = 3)
sixteen = Button(finestra, text = "1/16", command = sixteen_loop)
sixteen.grid(row = 14, column = 1)
thirtytwo = Button(finestra, text = "1/32", command = thirtytwo_loop)
thirtytwo.grid(row = 14, column = 2)
sixtyfour = Button(finestra, text = "1/64", command = sixtyfour_loop)
sixtyfour.grid(row = 14, column = 3)     
exiter = Button(finestra, text = "Exit", command = exiter_c)
exiter.grid(row = 11, column = 8)
show_previewer = Button(finestra, text = "Preview Added", command = show_preview)
show_previewer.grid(row = 12, column = 8)

finestra.mainloop()