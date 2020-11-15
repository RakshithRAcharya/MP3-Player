from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Simple MP3 Player")
root.geometry("500x350")

pygame.mixer.init()

def play_time():
    if stopped:
        return

    current_time = pygame.mixer.music.get_pos()/1000
    converted_time = time.strftime('%M:%S', time.gmtime(current_time))

    song = song_box.get(ACTIVE)
    song = f'C:/Users/raksh/Desktop/Old Songs/{song}.mp3'
    muta_song = MP3(song)
    global song_len
    song_len = muta_song.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_len))

    current_time += 1
    if(int(slider.get()) == int(song_len)):
        stop()
    elif paused:
        pass
    elif(int(slider.get()) == int(current_time)):
        slider_position = int(song_len)
        slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position = int(song_len)
        slider.config(to=slider_position, value=int(slider.get()))
        converted_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))
        status_bar.config(text=f'Time Elapsed: {converted_time}/{converted_song_length}')
        next_time = int(slider.get())+1
        slider.config(value=next_time)

    status_bar.after(1000, play_time)

def slide(x):
    song = song_box.get(ACTIVE)
    song = f'C:/Users/raksh/Desktop/Old Songs/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))


def add_song():
    song = filedialog.askopenfilename(initialdir="C:/Users/raksh/Desktop/Old Songs", title="Choose a Song",
                                      filetypes=(("mp3 files", "*.mp3"),))
    song = song.replace("C:/Users/raksh/Desktop/Old Songs/", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)

def add_songs():
    songs = filedialog.askopenfilenames(initialdir="C:/Users/raksh/Desktop/Old Songs", title="Choose Songs",
                                      filetypes=(("mp3 files", "*.mp3"),))
    for song in songs:
        song = song.replace("C:/Users/raksh/Desktop/Old Songs/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)

def remove_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def remove_all_song():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/raksh/Desktop/Old Songs/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()

global stopped
stopped = False

def stop():
    status_bar.config(text='')
    slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text='')

    global stopped
    stopped = True

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused
    if(paused):
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def next_song():
    status_bar.config(text='')
    slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'C:/Users/raksh/Desktop/Old Songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.select_set(next_one, last=None)

def prev_song():
    status_bar.config(text='')
    slider.config(value=0)
    prev_one = song_box.curselection()
    prev_one = prev_one[0] - 1
    song = song_box.get(prev_one)
    song = f'C:/Users/raksh/Desktop/Old Songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0, END)
    song_box.activate(prev_one)
    song_box.select_set(prev_one, last=None)

def vol(x):
    pygame.mixer.music.set_volume(volume.get())
    current_volume = pygame.mixer.music.get_volume()

master_frame = Frame(root)
master_frame.pack(pady=20)

song_box = Listbox(master_frame, bg='black', fg='green', width=60, selectbackground='gray', selectforeground='black')
song_box.grid(row=0, column=0)

back_btn_img = PhotoImage(file='C:\\Users\\raksh\\PycharmProjects\\pythonProject\\images\\previous.png')
next_btn_img = PhotoImage(file='C:\\Users\\raksh\\PycharmProjects\\pythonProject\\images\\next.png')
play_btn_img = PhotoImage(file='C:\\Users\\raksh\\PycharmProjects\\pythonProject\\images\\play.png')
pause_btn_img = PhotoImage(file='C:\\Users\\raksh\\PycharmProjects\\pythonProject\\images\\pause.png')
stop_btn_img = PhotoImage(file='C:\\Users\\raksh\\PycharmProjects\\pythonProject\\images\\stop.png')

controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

back_btn = Button(controls_frame, image=back_btn_img, borderwidth=0, command=prev_song)
next_btn = Button(controls_frame, image=next_btn_img, borderwidth=0, command=next_song)
play_btn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_btn.grid(row=0, column=0)
next_btn.grid(row=0, column=4)
play_btn.grid(row=0, column=2)
pause_btn.grid(row=0, column=1)
stop_btn.grid(row=0, column=3)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add 1 song to Playlist", command=add_song)
add_song_menu.add_command(label="Add songs to Playlist", command=add_songs)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove 1 song from Playlist", command=remove_song)
remove_song_menu.add_command(label="Remove all songs from Playlist", command=remove_all_song)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
slider.grid(row=2, column=0, pady=10)

volume = ttk.Scale(volume_frame, from_=0, to=100, orient=VERTICAL, value=1, command=vol, length=150)
volume.pack(pady=10)


root.mainloop()
