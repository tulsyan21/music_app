from tkinter import *
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
import os
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance") 

statusbar=ttk.Label(root,text="welcome to spotify!",relief=SUNKEN,anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

menubar=Menu(root)
root.config(menu=menubar)

def browse_file():
	global filename_path
	filename_path=filedialog.askopenfilename()
	add_to_playlist(filename_path)
	mixer.music.queue(filename_path)

def add_to_playlist(filename):
	filename=os.path.basename(filename)
	index=0
	playlistbox.insert(index,filename)
	playlist.insert(index,filename_path)
	index+=1

submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="file",menu=submenu)
submenu.add_command(label="open",command=browse_file)
submenu.add_command(label="exit",command=root.destroy)

playlist=[]

def about_us():
	tkinter.messagebox.showinfo("About Spotify","Spotify is a digital music streaming service that gives you access to millions of songs, podcasts and videos from artists all over the world. Spotify is immediately appealing because you can access content for free by simply signing up using an email address or by connecting with Facebook.")

submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="help",menu=submenu)
submenu.add_command(label="about us",command=about_us)

mixer.init()
root.title("Spotify")
root.iconbitmap(default='spot.ico')

leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30)

playlistbox=Listbox(leftframe)
playlistbox.pack(padx=30)

addphoto=PhotoImage(file='plus.png')
addbtn=ttk.Button(leftframe,image=addphoto,command=browse_file)
addbtn.pack(side=LEFT)

def del_song():
	selected_song=playlistbox.curselection()
	selected_song=int(selected_song[0])
	playlistbox.delete(selected_song)
	playlist.pop(selected_song)

delphoto=PhotoImage(file='delete.png')
delbtn=ttk.Button(leftframe,image=delphoto,command=del_song)
delbtn.pack(side=LEFT)

rightframe=Frame(root)
rightframe.pack(pady=30)

topframe=Frame(rightframe)
topframe.pack()

text_label = ttk.Label(topframe, text="Dive into spotify!")
text_label.pack(pady=5)

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack()

currenttimelabel = ttk.Label(topframe, text='Current Length : --:--',relief=GROOVE)
currenttimelabel.pack()

def show_details(play_song):
	text_label['text'] = "Playing" + ' - ' + os.path.basename(play_song)
	file_data = os.path.splitext(play_song)
	if file_data[1] == '.mp3':
		audio = MP3(play_song)
		total_length = audio.info.length
	else:
		a = mixer.Sound(play_song)
		total_length = a.get_length()
	mins,secs = divmod(total_length, 60)
	mins = round(mins)
	secs = round(secs)
	timeformat = '{:02d}:{:02d}'.format(mins, secs)
	lengthlabel['text'] = "Total Length" + ' - ' + timeformat

	t1=threading.Thread(target=start_count,args=(total_length,))
	t1.start()

def start_count(t):
	global paused
	current_time=0
	while current_time<=t and mixer.music.get_busy():
		if paused:
			continue
		else:
			mins,secs=divmod(current_time,60)
			mins=round(mins)
			secs=round(secs)
			timeformat = '{:02d}:{:02d}'.format(mins, secs)
			currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
			time.sleep(1)
			current_time+=1

play = PhotoImage(file='play.png')
pause = PhotoImage(file='pause.png')
mute_photo = PhotoImage(file='mute.png')
volume_photo=PhotoImage(file='unmute.png')
rewind=PhotoImage(file='rewind.png')
stop=PhotoImage(file='stop.png')

def play_music():
	global paused
	if paused:
		mixer.music.unpause()
		statusbar['text']="Music resumed!"
		paused=FALSE
	else:
		try:
			stop_music()
			time.sleep(1)
			selected_song=playlistbox.curselection()
			selected_song=int(selected_song[0])
			play_it=playlist[selected_song]
			mixer.music.load(play_it)
			mixer.music.play()
			statusbar['text']="Playing music-"+os.path.basename(play_it)
			show_details(play_it)
		except:
			tkinter.messagebox.showerror("File not found","Spotify could not open the file.Please try again!")
    	
paused=FALSE

def pause_music():
	global paused
	paused=TRUE
	mixer.music.pause()
	statusbar['text']="Music is paused!"

def set_vol(val):
	volume=float(val)/100
	mixer.music.set_volume(volume)

def stop_music():
	mixer.music.stop()
	statusbar['text']="Music stopped!"

middleframe=Frame(rightframe)
middleframe.pack(pady=30,padx=10)

play_btn = ttk.Button(middleframe, image=play, command=play_music)
play_btn.grid(row=0,column=1,padx=10)

pause_btn = ttk.Button(middleframe, image=pause, command=pause_music)
pause_btn.grid(row=0,column=0,padx=10)

stop_btn = ttk.Button(middleframe, image=stop, command=stop_music)
stop_btn.grid(row=0,column=2,padx=10)

buttonframe=Frame(rightframe)
buttonframe.pack(pady=10)

muted=FALSE

def mute_music():
	global muted
	if muted:
		mixer.music.set_volume(0.5)
		volume_btn.configure(image=volume_photo)
		scale.set(50)
		muted=FALSE
	else:
		mixer.music.set_volume(0)
		volume_btn.configure(image=mute_photo)
		scale.set(0)
		muted=TRUE

volume_btn=ttk.Button(buttonframe,image=volume_photo,command=mute_music)
volume_btn.grid(row=1,column=0)

def rewind_music():
	stop_music()
	play_music()
	statusbar['text']="Music rewinded!"

rewind_btn = ttk.Button(buttonframe, image=rewind, command=rewind_music)
rewind_btn.grid(row=0,column=1,padx=10)

scale=ttk.Scale(buttonframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(50)
mixer.music.set_volume(0.7)
scale.grid(row=1,column=1,padx=15)

def on_closing():
	stop_music()
	root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
