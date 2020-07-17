import scraper
from tkinter import *
import os
import newdb


root = Tk()
dc = dict()

for i in newdb.c.execute("SELECT * FROM things_to_watch WHERE new = 'True\n'"):
    dc[i[0]] = i[1:]


def go_to_page(url):
    os.system("start \"\" https://{}".format(url))


def enter_new(entr1,entr2,entr3,counter):
    #МАШИНАТОРЫ
    # www.youtube.com / channel / UC1FvG76TSFV5prFkA_xoaLw
    #59
    a = entr1.get()
    entr1.delete(0,END)
    b = entr2.get()
    entr2.delete(0, END)
    c = entr3.get()
    entr3.delete(0, END)
    try:
        newdb.write_to([a,b,c,"Flase\n"])
        Label(root,text="Successfully added to database").grid(row=counter)
    except:
        Label(root,text="Error occurred when trying to add to database").grid(row=counter)

    # b = Entry(root).get()
    # c = Entry(root).get()
    print(a,b,c)


def myLabels():
    counter = 0
    for j in dc.keys():
        Label(root, text="Can watch:" + j).grid(row=counter,sticky=W)
        Button(root,text="{}".format(dc[j][1]),command=lambda j=dc[j]: go_to_page(j[1])).grid(row=counter,column=1)
        counter += 1
    a = Entry(root,width=50,borderwidth=5)
    b = Entry(root,width=50,borderwidth=5)
    c = Entry(root,width=50,borderwidth=5)
    a.grid(row=counter,)
    b.grid(row=counter+1)
    c.grid(row=counter+2)
    a.insert(0,"HTML name for anime or youtube channel name")
    b.insert(1, "Anime episode or video count")
    c.insert(2, "Website or youtube channel url")

    Button(root, text="Add new", command=lambda j=(a,b,c,counter+4):enter_new(j[0],j[1],j[2],j[3])).grid(row=counter+3,)


myLabels()
root.mainloop()
