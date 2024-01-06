"""
import moviepy
from moviepy.editor import VideoFileClip, clips_array
vid1 = VideoFileClip("sources/emocionesVideo1.mp4").subclip(10, 10+4)
vid2 = VideoFileClip("sources/feliz_3.mp4").subclip(0, 0+4)


print(vid2)
comb1 = clips_array([[vid1, vid2]])

comb1.write_videofile("sources/combined.mp4")

vid1.close()
vid2.close()

from tkinter import *
from tkvideo import tkvideo

root = Tk()
my_label = Label(root)
my_label.pack()

clip = VideoFileClip("sources/feliz_3.mp4")

player = tkvideo(clip, my_label, loop = 1)
player.play()

root.mainloop()
"""

from tkinter import *
from moviepy.editor import *

clip1 = VideoFileClip("sources/emocionesVideo1.mp4")
clip2 = VideoFileClip("sources/feliz_3.mp4")
clip3 = VideoFileClip("sources/feliz-2.mp4")


clip1.close()
clip2.close()
clip3.close()

#Main Screen
root = Tk()
root.title("Video Tecnobot")
root.geometry("750x200")


b = Button(root, text="Mix", relief = GROOVE, bg="#232323", fg="white")
b.pack(side="left", padx=100) 
b.config(width=8, height=3)

root.mainloop()