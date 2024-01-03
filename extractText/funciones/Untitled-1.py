import tkinter as tk
from tkinter import *
my_w = tk.Tk()
my_w.geometry("300x200") 
my_w.title("www.plus2net.com") 

font1=('Arial',24,'bold')
sv = StringVar() #string variable 
sb = Spinbox(my_w,textvariable=sv,font=font1,
     width=3,from_=0,to=100)
sb.grid(row=1,column=1,padx=30,pady=10)

sc = Scale(my_w, from_=0, to=100, font=font1,
    orient=HORIZONTAL,variable=sv,length=180)
sc.grid(row=2,column=1,padx=30)
ss = Spinbox(my_w,textvariable=sv, to=100)
my_w.mainloop()  # Keep the window open