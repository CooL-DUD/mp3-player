from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Jonybek's mp3")
root.iconbitmap('')
root.geometry("600x450")

pygame.mixer.init()


def play_time():
    if isStopped:
        return
    unf_current_time = pygame.mixer.music.get_pos() / 1000
    current_time = time.strftime('%H:%M:%S', time.gmtime(unf_current_time))

    # slider_label.config(text=f'Slider: {int(slider.get())} and Song Pos: {int(unf_current_time)}')

    current_song = playlist.curselection()
    song = playlist.get(current_song)
    song = 'C:/OpenServer/domains/localhost/mp3_player/music/' + song + ".mp3"
    song_mut = MP3(song)

    global unf_song_length

    unf_song_length = song_mut.info.length
    song_length = time.strftime('%H:%M:%S', time.gmtime(unf_song_length))

    if int(slider.get()) == int(unf_song_length):
        status_bar.config(text="Time Elapsed: " + song_length + " of " + song_length)
        pass
    elif isPaused:
        pass
    elif int(slider.get()) == int(unf_current_time) + 1:
        slider_pos = int(unf_song_length)
        slider.config(to=slider_pos, value=int(unf_current_time) + 1)
    else:
        slider_pos = int(unf_song_length)
        slider.config(to=slider_pos, value=int(slider.get()))

        current_time = time.strftime('%H:%M:%S', time.gmtime(slider.get()))
        status_bar.config(text="Time Elapsed: " + current_time + " of " + song_length)
        next_time = int(slider.get()) + 1
        slider.config(value=next_time)
    # slider.config(value=int(unf_current_time))

    status_bar.after(1000, play_time)


def add_song():
    songs = filedialog.askopenfilenames(initialdir='music/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song = song.replace(".mp3", "")
        song = song.replace("C:/OpenServer/domains/localhost/mp3_player/music/", "")

        playlist.insert(END, song)


def play():
    stop()
    global isPaused
    isPaused = False
    global isStopped
    isStopped = False
    song = playlist.get(ACTIVE)
    song = 'C:/OpenServer/domains/localhost/mp3_player/music/' + song + ".mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()

    # slider_pos = int(unf_song_length)
    # slider.config(to=slider_pos, value=0)


global isStopped
isStopped = False


def stop():
    status_bar.config(text='')
    slider.config(value=0)

    pygame.mixer.music.stop()
    global isStopped
    isStopped = True


global isPaused
isPaused = False


def pause(state):
    global isPaused
    isPaused = state

    if isPaused:
        pygame.mixer.music.unpause()
        isPaused = False
    else:
        pygame.mixer.music.pause()
        isPaused = True


def forward():
    global isPaused
    isPaused = False
    status_bar.config(text='')
    slider.config(value=0)

    next_song = playlist.curselection()
    next_song = next_song[0] + 1
    if playlist.size() <= next_song:
        playlist.selection_set(0)
        playlist.selection_clear(ACTIVE)
        playlist.activate(0)
    else:
        playlist.selection_set(next_song, next_song + 1)
        playlist.selection_clear(ACTIVE)
        playlist.activate(next_song + 1)
    play()


def rewind():
    global isPaused
    isPaused = False
    status_bar.config(text='')
    slider.config(value=0)

    prev_song = playlist.curselection()
    prev_song = prev_song[0]
    if 0 >= prev_song:
        playlist.selection_set(playlist.size() - 1)
        playlist.selection_clear(ACTIVE)
        playlist.activate(playlist.size() - 1)
    else:
        playlist.selection_set(prev_song, prev_song - 1)
        playlist.selection_clear(ACTIVE)
        playlist.activate(prev_song - 1)
    play()


def delete_song():
    playlist.delete(ANCHOR)
    stop()


def delete_all_songs():
    playlist.delete(0, END)
    stop()


def slide(x):
    # slider_label.config(text=f'{int(slider.get())} of {int(unf_song_length)}')
    song = playlist.get(ACTIVE)
    song = 'C:/OpenServer/domains/localhost/mp3_player/music/' + song + ".mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))


playlist = Listbox(root, bg="grey", fg="white", width=60, selectbackground="white", selectforeground="grey")
playlist.pack(pady=20)

rewind_btn_img = PhotoImage(file='ui/rewind-button-round-50.png')
play_btn_img = PhotoImage(file='ui/play-button-circled-50.png')
pause_btn_img = PhotoImage(file='ui/pause-button-50.png')
stop_btn_img = PhotoImage(file='ui/stop-circled-50.png')
forward_btn_img = PhotoImage(file='ui/fast-forward-round-50.png')

control_frame = Frame(root)
control_frame.pack()

rewind_btn = Button(control_frame, image=rewind_btn_img, borderwidth=0, command=rewind)
play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(isPaused))
stop_btn = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)
forward_btn = Button(control_frame, image=forward_btn_img, borderwidth=0, command=forward)

rewind_btn.grid(row=0, column=0, padx=10)
play_btn.grid(row=0, column=1, padx=10)
pause_btn.grid(row=0, column=2, padx=10)
stop_btn.grid(row=0, column=3, padx=10)
forward_btn.grid(row=0, column=4, padx=10)

menu = Menu(root)
root.config(menu=menu)

add_song_menu = Menu(menu)
menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

# delete_song_menu = Menu(menu)
# delete_song_menu.add_cascade(label="Delete Song", menu=add_song_menu)
add_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
add_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, length=300, command=slide)
slider.pack(pady=30)

# slider_label = Label(root, text="0")
# slider_label.pack(pady=10)

root.mainloop()
