#!/usr/bin/python

# Some python modules are needed:

# sudo apt-get install python-tk
# sudo apt-get install python-pmw
# sudo apt-get install python-imaging

from Tkinter import *
from PIL import Image, ImageTk
import Pmw
import time


# Import modules.


import imp

task1 = imp.load_source('task1', 'AsibotSimulation/programas/pick_can.py')
task2 = imp.load_source('task2', 'AsibotSimulation/programas/fill_glass.py')
task3 = imp.load_source('task3', 'AsibotSimulation/programas/move_dish.py')


# Global variables.


selectedOption = 0
redCircle = None
greenCircle = None
x1 = -1
y1 = -1
x2 = -1
y2 = -1


root = Tk()
root.title("Asibot Task Simulator")


# Functions.


def placedObjsLabel(selectedOption, x1, y1):

   global placedObjs
   coords1 = ""

   if x1 != -1:
       
      coords1 = "("+ str(x1) + "," + str(y1) + ")"

      if selectedOption == 1 and x1 != -1:
   
         placedObjs.config(text = "red can " + coords1, fg = "red")

      if selectedOption == 2 and x1 != -1:

         placedObjs.config(text = "glass " + coords1, fg = "red")

      if selectedOption == 3 and x1 != -1:

         placedObjs.config(text = "dish " + coords1, fg = "red")

   else:

      placedObjs.config(text = "")

def placedObjsLabel2(selectedOption, x2, y2):

   global placedObjs2
   coords2 = ""

   if x2 != -1:

      coords2 = "("+ str(x2) + "," + str(y2) + ")"
      placedObjs2.config(text = "bottle " + coords2, fg = "green")

   else:
      placedObjs2.config(text = "")


def placeMainObj(event):

   global canvas
   global selectedOption
   global redCircle
   global x1, y1

   if redCircle != None:
      canvas.delete(redCircle)

   if selectedOption != 0:

   # Corners Valid area [(85, 40), (301, 40), (52, 182), (268, 182)]
   # Vertical lines 142x + 33y = 13390 and 142x + 33y = 44062

   # Corners respect canvas Kitchen [(313,41), (101, 41), (347, 181), (133, 181)]
   # Aprox. coords in simulated kitchen [(1.22, 0.08), (0.6, 0.08), (1.28, 0.5), (0.7, 0.5)]
   # scale_x = 0.0028 , scale_y = 0.003
   # x_offset = 0.31, y_offset = -0.04

      x_offset = 0.31
      y_offset = -0.04
      scale_x = 0.0029
      scale_y = 0.003

      if event.y < 182 and event.y > 40:
         if event.x < (44062 - 33 * event.y) / 142 and event.x > (13390 - 33 * event.y) / 142:
            redCircle = canvas.create_oval(event.x - 2, event.y - 2, event.x + 2, event.y + 2, fill = "red")
	    x1 = round((400 - event.x) * scale_x + x_offset, 3)
            y1 = round(event.y * scale_y + y_offset, 3)
	    placedObjsLabel(selectedOption, x1, y1)

         else:
	    x1 = -1
            y1 = -1
	    placedObjsLabel(selectedOption, x1, y1)
      else:
         x1 = -1
	 y1 = -1
	 placedObjsLabel(selectedOption, x1, y1)


def placeSecondObj(event):

   global canvas
   global selectedOption
   global greenCircle
   global x2, y2

   if greenCircle != None:
      canvas.delete(greenCircle)

   if selectedOption != 0 and selectedOption == 2:

   # Corners Valid area [(85, 40), (301, 40), (52, 182), (268, 182)]
   # Vertical lines 142x + 33y = 13390 and 142x + 33y = 44062

      x_offset = 0.31
      y_offset = -0.04
      scale_x = 0.0029
      scale_y = 0.003

      if event.y < 182 and event.y > 40:
         if event.x < (44062 - 33 * event.y) / 142 and event.x > (13390 - 33 * event.y) / 142:
	    greenCircle = canvas.create_oval(event.x - 2, event.y - 2, event.x + 2, event.y + 2, fill = "green")
	    x2 = round((400 - event.x) * scale_x + x_offset, 3)
            y2 = round(event.y * scale_y + y_offset, 3)
	    placedObjsLabel2(selectedOption, x2, y2)

         else:
	    x2 = -1
            y2 = -1
	    placedObjsLabel2(selectedOption, x2, y2)
      else:
         x2 = -1
	 y2 = -1
	 placedObjsLabel2(selectedOption, x2, y2)


def pickcan():
    global selectedOption
    global canvas
    global taskname, placedObjsLabel, placedObjsLabel2
    global x1, x2, y1, y2
    x1 = -1
    x2 = -1
    y1 = -1
    y2 = -1
    canvas.delete(greenCircle)
    canvas.delete(redCircle)
    placedObjsLabel(selectedOption, x1, y1)
    placedObjsLabel2(selectedOption, x2, y2)
    selectedOption = 1
    taskname.config(text = "Pick red can")
    buttons.button("b1").config(highlightbackground="red", highlightcolor="red")
    buttons.button("b2").config(highlightbackground= "light grey", highlightcolor="light grey")
    buttons.button("b3").config(highlightbackground= "light grey", highlightcolor="light grey")


def fillglass():
    global selectedOption
    global canvas
    global taskname, placedObjsLabel, placedObjsLabel2
    global x1, x2, y1, y2
    x1 = -1
    x2 = -1
    y1 = -1
    y2 = -1
    canvas.delete(greenCircle)
    canvas.delete(redCircle)
    placedObjsLabel(selectedOption, x1, y1)
    placedObjsLabel2(selectedOption, x2, y2)
    selectedOption = 2
    taskname.config(text = "Fill glass")
    buttons.button("b2").config(highlightbackground="red", highlightcolor="red")
    buttons.button("b1").config(highlightbackground= "light grey", highlightcolor="light grey")
    buttons.button("b3").config(highlightbackground= "light grey", highlightcolor="light grey")


def movedish():
    global selectedOption
    global canvas
    global taskname, placedObjsLabel, placedObjsLabel2
    global x1, x2, y1, y2
    x1 = -1
    x2 = -1
    y1 = -1
    y2 = -1
    canvas.delete(greenCircle)
    canvas.delete(redCircle)
    placedObjsLabel(selectedOption, x1, y1)
    placedObjsLabel2(selectedOption, x2, y2)
    selectedOption = 3
    taskname.config(text = "Move dish")
    buttons.button("b3").config(highlightbackground="red", highlightcolor="red")
    buttons.button("b1").config(highlightbackground= "light grey", highlightcolor="light grey")
    buttons.button("b2").config(highlightbackground= "light grey", highlightcolor="light grey")


def start():
    global selectedOption
    global x1, x2, y1, y2
    global task1, task2, task3

    if selectedOption == 1 and x1 != -1:

	print "\n" + "WARNING: requires a running instance of cartesianServer" + "\n"
	task1.simulation([x1, y1, 0.865], [1, 1.215, 0.7], [1.3, 1.25, 0.7])

    if selectedOption == 2 and x1 != -1 and x2 != -1:

	if x1 - x2 >  0.08 or x1 - x2 < -0.08 or y1 - y2 > 0.08 or y1 - y2 < -0.08:

	   print "\n" + "WARNING: requires a running instance of cartesianServer" + "\n"
	   task2.simulation([x1, y1, 0.865], [x2, y2, 0.865], [1, 1.215, 0.7491], [1.3, 1.25, 0.7])
        else:

	   print "\n" + "Error: Both objects are too much near each other" + "\n"            

    if selectedOption == 3 and x1 != -1:

	print "\n" + "WARNING: requires a running instance of cartesianServer" + "\n"
	task3.simulation([x1, y1, 0.865], [1, 1.215, 0.7491], [1.3, 1.25, 0.7])
    

# Loading images.


movedish_img = ImageTk.PhotoImage(Image.open("AsibotSimulation/asibotGUI/movedish.jpg").resize((150, 100), Image.ANTIALIAS))

pickcan_img = ImageTk.PhotoImage(Image.open("AsibotSimulation/asibotGUI/pickcan.jpg").resize((150, 100), Image.ANTIALIAS))

fillglass_img = ImageTk.PhotoImage(Image.open("AsibotSimulation/asibotGUI/fillglass.jpg").resize((150, 100), Image.ANTIALIAS))

imgCanvas = ImageTk.PhotoImage(Image.open("AsibotSimulation/asibotGUI/scene.png").resize((400, 196), Image.ANTIALIAS))


# Creating GUI.


labelframe = LabelFrame(root, labelanchor = N, font = ("Times", "12"), text = "Choose one task")
labelframe.pack(fill="both", expand=1, padx=10, pady=10)

taskname = Label(labelframe)
taskname.pack(side = BOTTOM)

buttons = Pmw.ButtonBox(labelframe, labelpos='n')
buttons.pack(fill='both', expand=1, padx=10, pady=10)

buttons.add("b1", image = pickcan_img, command = pickcan)
buttons.add("b2", image = fillglass_img, command = fillglass)
buttons.add("b3", image = movedish_img, command = movedish)


# Creating Canvas to catch mouse event.


labelframe2 = LabelFrame(root, labelanchor = N, font = ("Times", "12"), text = "Place Object(s)")
labelframe2.pack(fill="both", expand=1, padx=10, pady=10)

frame = Frame(labelframe2, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
canvas = Canvas(frame, bd=0, width = 400, height = "196")
canvas.grid(row=0, column=0, sticky=N+S+E+W)
frame.pack(expand=1, padx=10, pady=10)

canvas.create_image(0,0,image=imgCanvas,anchor="nw")

canvas.bind("<Button 1>",placeMainObj)
canvas.bind("<Button 3>",placeSecondObj)


# Label Objects Placed


placedObjs2 = Label(labelframe2)
placedObjs2.pack(side = BOTTOM)

placedObjs = Label(labelframe2)
placedObjs.pack(side = BOTTOM)


# Adding button Start Simulation.


bottomframe = Frame(root)
bottomframe.pack(expand=1, padx=10, pady=10)

blackbutton = Button(bottomframe, text="Start Simulation", fg="black", command = start)
blackbutton.pack( side = BOTTOM )


try:
   time.sleep(0.1)
except KeyboardInterrupt:
   root.destroy()

root.mainloop()
