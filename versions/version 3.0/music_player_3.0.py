import pygame
from pygame import mixer
from tkinter import*
import os
import time
from aubio import source, tempo
from numpy import median, diff
import scipy.io.wavfile
import matplotlib.pyplot as plt
from tkinter import*
from mutagen.mp3 import MP3
from tkinter.ttk import *
from os import path
from pydub import AudioSegment
import ffmpy

mixer.init()

lenght = 0

go = True

long = 0

song_name = ""

canzone = ""

new_file_save = ""

len_s = 0

song_name2 = ""

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

os.chdir(r"C:\Users\Emanuele\Desktop\Informatica\python\progetti\Chiavetta USB") 

lista = os.listdir()

try :

    for songers in lista:

        if (songers.endswith("_changed.mp3") == True or songers.endswith("_changed.wav") == True):
                
            os.remove(songers)
    
except BaseException as ex:

    print(ex)

lista = os.listdir()

for ert in range (0, len(lista)):

    item = lista[er]

    er += 1

    listbox.insert(er, item)

bpm = 0 

b_pmer = 0 

song_prov = ""

durations = 0

song_name2 = 0 

def add(): 

    global song_prov

    selection = Listbox.curselection(listbox)

    numero = selection[0]

    pather = lista[numero]

    song_prov = pather

    canzone = "In queue: " + str(pather)
    
    Loaded_song= Label(finestra, text = "                                  ", background = "light blue", font = 20)
    Loaded_song.grid(row=6, column=3)

    finestra.update_idletasks()

    Loaded_song= Label(finestra, text = canzone, background = "light blue", font = 20)
    Loaded_song.grid(row=6, column=3)

    finestra.update_idletasks()
    
    return song_prov

def time_translator():

    global go

    if (go == True):

        global lenght, long 

        minute, second = 0, 0

        long += 1

        second = long 

        while (second >= 60):

            second -= 60
        
            minute += 1    
    
        if (minute < 10):

            minute = "0" + str(minute)

        if (second < 10):

            second = "0" + str(second)

        shower = Label(finestra, text = "Timing :    " + str(minute) + " : " + str(second), background = "light blue", font = 20)
        shower.grid(row = 4, column = 3)

        if (long < lenght):

            shower.after(1000, time_translator)

def play ():

    global song_prov, song_name, b_pmer

    global lenght, long, durations, song_name2

    song_name2 = 0
    
    path_2 = song_prov
    
    percorso = r"C:\Users\Emanuele\Desktop\Informatica\python\progetti\Chiavetta USB" # replace with the path of the folder of the music to play 

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

    song_name = file_wav
    
    file = percorso + "\\" + file_wav 

    file1 = percorso + "\\" + file_name
    
    src = file1
    dst = file
                                       
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    
    audio = MP3(file1)

    len_s = audio.info.length

    len_w = int(len_s)

    durations = len_w 

    rate, data = scipy.io.wavfile.read(file)
     
    plt.plot(data)

    save_path = r"C:\Users\Emanuele\Desktop\Informatica\python\progetti"

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

    b_pmer = round(bpm, 1)

    pygame.mixer.music.play(0)

    lenght = len_w 

    long = 0

    return durations, song_name, song_name2, b_pmer, lenght, long, time_translator()

def remove_martingarrix(): 

    global long, lenght 

    long = lenght + 10

    pygame.mixer.music.unload()

    return long

def stop_martingarrix():

    global long, lenght

    long = lenght + 10

    pygame.mixer.music.stop()

    return long

def rewind_martingarrix():

    global long

    long = 0

    pygame.mixer.music.rewind()

    return long, time_translator()

def pause_martingarrix():

    global lenght, long

    long = lenght + 10

    pygame.mixer.music.pause()

    return long

def resume_martingarrix():

    global long

    result_ms = pygame.mixer.music.get_pos()

    result_s = int(result_ms) / 1000

    result_pass = round(result_s, 0)

    res_pass = int(result_pass)

    long = res_pass
    
    pygame.mixer.music.unpause()

    return long, time_translator()

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

    global n, song_name2

    hot1 = pygame.mixer.music.get_pos()

    hot = float(hot1) / 1000

    if (song_name2 == 1):

       hot += 13

    n += 1

    listbox1.insert(n, hot)

    return n

def Cue():

    global long
 
    selection1 = Listbox.curselection(listbox1)

    selected = selection1[0]

    pos2 = listbox1.get(int(selected), int(selected))

    pos1 = pos2[0]

    pos = float(pos1)

    position = round(pos, 0)

    position_i = int(position)

    long = position_i

    pygame.mixer.music.set_pos(pos)

    return long, time_translator()

def Cue_real():

    block_timer()

    time.sleep(1)

    Cue()

    global go

    go = True

    return go

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

def block_timer():

    global go

    go = False

    return go

def all_loop():

    global b_pmer, long

    bpm1 = b_pmer

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    tot_loop = 0

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):
        
        time.sleep(beat)

        pygame.mixer.music.set_pos(loop_get_pos)

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    long = int(res_pass)

    return long, time_translator()

def half_loop():

    global long, b_pmer

    bpm1 = b_pmer

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/2
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    long = int(res_pass)

    return long, time_translator()

def quarter_loop():

    global long, b_pmer

    bpm1 = b_pmer

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/4
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    long = int(res_pass)

    return long, time_translator()

def eight_loop():

    global long, b_pmer

    bpm1 = b_pmer

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/8
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    long = int(res_pass)

    return long, time_translator()

def sixteen_loop():

    global long, b_pmer

    bpm1 = b_pmer

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/16
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    long = int(res_pass)

    return long, time_translator()

def thirtytwo_loop():

    global long, b_pmer

    bpm1 = b_pmer

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/32
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    long = int(res_pass)

    return long, time_translator()

def sixtyfour_loop():

    global long, b_pmer

    bpm1 = b_pmer

    beat = (bpm1 / 60) * 4

    loop_get_pos1 = pygame.mixer.music.get_pos()

    loop_get_pos = loop_get_pos1 / 1000

    n_looper_repeat = sp2.get()

    for i in range (0, int(n_looper_repeat)):

        waiter_time = beat/64
        
        time.sleep(waiter_time)

        pygame.mixer.music.set_pos(loop_get_pos)

    result_s = int(loop_get_pos)

    result_pass = round(result_s, None)

    res_pass = int(result_pass)

    long = int(res_pass)

    return long, time_translator()

def exiter_c():

    finestra.quit()

    print("\n\nThe programm has been developed by ©TheProgxy.\n\nThank you for using this programm :) !")

def show_preview():

    global song_prov
    
    path_2 = song_prov
    
    percorso = r"C:\Users\Emanuele\Desktop\Informatica\python\progetti\Chiavetta USB" # replace with the path of the folder of the music to play 

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

    rate, data = scipy.io.wavfile.read(file)
     
    plt.plot(data)

    save_path = r"C:\Users\Emanuele\Desktop\Informatica\python\progetti"

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

    len_sec1 = len_w

    while (int(len_sec1) >= 60):

        len_m += 1

        len_sec1 -= 60

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

def all_looper():

    block_timer()

    time.sleep(1)

    all_loop()

    global go

    go = True

    return go

def half_looper():

    block_timer()

    time.sleep(1)

    half_loop()

    global go

    go = True

    return go

def quarter_looper():

    block_timer()

    time.sleep(1)

    quarter_loop()

    global go

    go = True

    return go

def eight_looper():

    block_timer()

    time.sleep(1)

    eight_loop()

    global go

    go = True

    return go

def sixteen_looper():

    block_timer()

    time.sleep(1)

    sixteen_loop()

    global go

    go = True

    return go

def thirtytwo_looper():

    block_timer()

    time.sleep(1)

    thirtytwo_loop()

    global go

    go = True

    return go

def sixtyfour_looper():

    block_timer()

    time.sleep(1)

    sixtyfour_loop()

    global go

    go = True

    return go

def change_tempo():

    global song_name, durations, b_pmer

    global lenght, long, song_name2

    try :

        os.chdir(r"C:\Users\Emanuele\Desktop\Informatica\python\progetti\Chiavetta USB") 

        listarella = os.listdir()

        pygame.mixer.music.unload()

        for sng in listarella:

            if (sng.endswith("_changed.mp3") == True or sng.endswith("_changed.wav") == True):
                
                os.remove(sng)
    
    except BaseException as ex:

        return ex

    os.chdir(r"C:\Users\Emanuele\Desktop\Informatica\python\progetti\Chiavetta USB") 

    bpm_dtctd = int(b_pmer)
    
    bpm_from_change = song_name

    bpm_to_change = song_name.replace(".wav","_changed.wav")

    bpm_to_change2 = song_name.replace(".wav","_changed.mp3")

    song_name2 = 1

    bpm_change = tempo_changerino.get()

    bpm_ratio = int(bpm_change) / int(bpm_dtctd)

    bpm_chng = "atempo=" + str(bpm_ratio)

    ff = ffmpy.FFmpeg(inputs={bpm_from_change: None}, outputs={bpm_to_change: ["-filter:a", bpm_chng]})
    ff.run()

    ff2 = ffmpy.FFmpeg(inputs={bpm_to_change: None}, outputs={bpm_to_change2: None})
    ff2.run()

    os.remove(bpm_to_change)

    durate_actual = pygame.mixer.music.get_pos()

    ris = int(durate_actual) / 1000

    ris2 = round(ris, 0)

    ris_f = int(ris2)

    pather = r"C:\Users\Emanuele\Desktop\Informatica\python\progetti\Chiavetta USB" # replace with the path of the folder of the music to play 

    path23 = pather + "\\" + bpm_to_change2

    pygame.mixer.music.load(path23)

    pygame.mixer.music.play()

    pre_bpm = int(bpm_change)

    new_bpm = round(pre_bpm, 1)

    bpmer_pre = Label(finestra, text = "                             ", background = "light blue", font = 20)
    bpmer_pre.grid(row = 7, column = 3)

    finestra.update_idletasks()

    bpmer = Label(finestra, text = str(new_bpm), background = "light blue", font = 20)
    bpmer.grid(row = 7, column = 3)

    finestra.update_idletasks()

    len_new = (bpm_dtctd * durations) / pre_bpm

    second = int(len_new) + 1 

    minute = 0

    while (second >= 60):

        second -= 60
        
        minute += 1    
    
    if (minute < 10):

        minute = "0" + str(minute)

    if (second < 10):

        second = "0" + str(second)

    duration = Label(finestra, text = str(minute) + " : " + str(second), background = "light blue", font = 20)
    duration.grid(row = 8, column = 3)

    finestra.update_idletasks()

    longer = durations

    long2 = (ris_f * len_new) / longer

    long = int(long2)

    lenght = int(len_new) + 1

    pygame.mixer.music.set_pos(long2)

    return song_name2, lenght, long, time_translator()

def change_tempor():

    block_timer()

    time.sleep(1)

    change_tempo()

    global go

    go = True

    return go

sp1 = Spinbox(finestra, from_ = 0.0, to = 1.0, increment = 0.1)
sp1.grid(row = 6, column = 1)
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
Control.grid(row = 5, column = 2)
Hotpoint = Button(finestra, text = "HotPoint", command = HotPoint)
Hotpoint.grid(row = 12, column = 4)
cue = Button(finestra, text = "Cue", command = Cue_real)
cue.grid(row = 13, column = 4)
Delete_cue = Button(finestra, text = "Delete Cue", command = delete_Cue)
Delete_cue.grid(row = 14, column = 4)
get_vol = Button(finestra, text = "Get Volume", command = get_volume)
get_vol.grid(row = 5, column = 1)
change_tempos = Button(finestra, text = "Change Tempo", command = change_tempor)
change_tempos.grid(row  = 16, column = 1)
tempo_changerino = Entry(finestra)
tempo_changerino.insert(0, "Es. 120")
tempo_changerino.grid(row  = 16, column = 2)

scroll_bar.config( command = listbox.yview ) 
scroll_bar1.config( command = listbox1.yview ) 

all_l = Button(finestra,text = "Loop" , command = all_looper)
all_l.grid(row = 15, column = 1)
half = Button(finestra, text = "1/2", command = half_looper)
half.grid(row = 13, column = 1)
quarter = Button(finestra, text = "1/4", command = quarter_looper)
quarter.grid(row = 13, column = 2)
eight = Button(finestra, text = "1/8", command = eight_looper)
eight.grid(row = 13, column = 3)
sixteen = Button(finestra, text = "1/16", command = sixteen_looper)
sixteen.grid(row = 14, column = 1)
thirtytwo = Button(finestra, text = "1/32", command = thirtytwo_looper)
thirtytwo.grid(row = 14, column = 2)
sixtyfour = Button(finestra, text = "1/64", command = sixtyfour_looper)
sixtyfour.grid(row = 14, column = 3)     
exiter = Button(finestra, text = "Exit", command = exiter_c)
exiter.grid(row = 11, column = 8)
show_previewer = Button(finestra, text = "Preview Added", command = show_preview)
show_previewer.grid(row = 12, column = 8)

finestra.mainloop()