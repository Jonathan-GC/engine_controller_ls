from PIL import Image
import os

import tkinter as tk
from tkinter import filedialog # to use file dialog

my_w = tk.Tk()
my_w.geometry("450x200")  # Size of the window width x height
my_w.title("www.plus2net.com")  #  title
path='' # string to hold source directory path 
path2='' # string to hold destination directory path
def my_fun1(): 
    global path 
    path = filedialog.askdirectory() # select directory 
    l1.config(text=path) # Show directory path in Label 

b1=tk.Button(my_w,text='Source directory',font=22,
    command=lambda:my_fun1(),bg='lightgreen')
b1.grid(row=0,column=0,padx=10,pady=20)

l1=tk.Label(my_w,text='Source',bg='yellow',font=12)
l1.grid(row=1,column=0,padx=2)


def my_fun2(): 
    global path2 
    path2 = filedialog.askdirectory() # select directory 
    l2.config(text=path2) #  Show selected directory path

b2=tk.Button(my_w,text='Destination directory',font=22,
    command=lambda:my_fun2(),bg='lightgreen')
b2.grid(row=0,column=2,padx=10,pady=20)

l2=tk.Label(my_w,text='Destination',bg='yellow',font=12)
l2.grid(row=1,column=2,padx=2) #  show destination path

b3=tk.Button(my_w,text='GO',font=22,
    command=lambda:create_thumbnails(),bg='lightyellow')
b3.grid(row=0,column=3,padx=10,pady=20)

def create_thumbnails():
    global path,path2 
    if os.path.exists(path) and os.path.exists(path2):
        l1=os.listdir(path) # List of all files and directories
        for file in l1:
            #print(file) # Print file or directory names 
            if os.path.splitext(file)[1]=='.png': 
                img = Image.open(path+'/'+file, mode="r")  # 
                #img.show()  # display
                print(img.size) # source image size ( width, height)
                img.thumbnail((200, 200))  # max width, max height
                img.save(path2+'/'+file)  # save thumbnail  image
                #print(img.size)  # thumbnail size ( width, height)
                #img.show()  # display thumbnail image
my_w.mainloop()  # Keep the window open