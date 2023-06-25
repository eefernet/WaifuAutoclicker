"""
Ethan Jamieson
6/20/2023
a stupid autoclicker for eu4
"""
from PIL import Image, ImageTk
import customtkinter
import pyautogui
import time
import keyboard
import threading
import os
import sys

#setup tkcustom stuff
app = customtkinter
app.set_appearance_mode("dark")
app.set_default_color_theme("dark-blue")

#set root window and size, might change later idk spending too much time on this as is
root = app.CTk()
root.geometry("512x688")

#Global program vars 
clickInterval = 1
keyboardHook = None
shortCutActive = False
shortCutKey = None
autoClickerThread = None
clickCount = 0
#lower the pause that py takes between clicks (default is .1)
pyautogui.PAUSE = 0.000001

#Resource path because autopy is dumb
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#functions for window click events, unfocus the window when clicked
def unfocus(event):
    root.focus()

#functions for program
def startButton():
    global keyboardHook
    #Update the label to tell the user whos giving orders
    button.configure(text="press any key on the keyboard")
    #remove the keyboard listener
    keyboard.unhook_all()
    #send the keyboard event to the onKeyPress function, also lets replace that nun
    keyboardHook = keyboard.on_press(onKeyPress)

#start listining for a keyboard press
def onKeyPress(event):
    global keyboardHook, shortCutActive, shortCutKey
    keyCombination = event.name

    #check to see if the shortcut is already active before we go assigning new keys
    if not shortCutActive:
        keyboard.add_hotkey(keyCombination, onShortcut)
        # Update the label with the detected shortcut
        keyShortCutLabel.configure(text = "Shortcut: " + keyCombination)
        #remove the keyboard hook so it doesnt just keep updating
        if keyboardHook is not None and callable(keyboardHook):
            keyboard.unhook(keyboardHook)
        shortCutActive = True
        button.configure(text="set keyboard shortcut")
    else:
        disableShortcut()

    shortCutKey = keyCombination

#Run this function when the shortcut key is pressed
def onShortcut():
    global shortCutActive, shortCutKey, clickInterval, autoClickerThread
    
    if not shortCutActive:
        #make sure the interval is not a str and that its not a 0
        if entry.get() is not str and float(entry.get()) != 0.0:
            print("Short cut enabled, click interval" + str(clickInterval))
            shortCutActive = True
            clickInterval = 1/float(entry.get())
            autoClickerThread = threading.Thread(target=autoClickerLoop)
            autoClickerThread.start()
        else:
            errorLogLabel.configure(text= "Your click interval must be a \nnumber and can't be zero!")
    
    else:
        print("shortcut disabled")
        shortCutActive = False
        errorLogLabel.configure(text= "Waiting for you ;)")

#The autoclicker func
def autoClickerLoop():
    global clickInterval
    errorLogLabel.configure(text= "Clicking! Teehee")
    startTime = time.perf_counter()

    #while our shortcut is active run this 
    while shortCutActive:
        currentTime = time.perf_counter()
        #sleep gives me inconsistent results, time steping instead
        elapsedTime = currentTime - startTime
        if elapsedTime >= clickInterval:
            print("shortcut active! ClickeInterval : " + str(clickInterval))
            pyautogui.click()
            startTime = time.perf_counter()

#Disable the autoclicker and join the thread
def disableShortcut():
    global shortCutActive, autoClickerThread
    shortCutActive = False
    autoClickerThread.join()

#Higher numbers means lizzard brain happy
def testClicker():
    global clickCount
    clickCount+=1
    clickButton.configure(text=str(clickCount))

#set windows properties like the title and icon
root.title("Autoclicker: Waifu Edition")
root.iconbitmap(default=resource_path("./waifuIcon.ico"))

#Create the basic window and set frame to the CTKFrame root
frame = app.CTkFrame(master=root,)
frame.pack(pady = 0, padx = 0, fill= "both", expand = True)

#make a canvas to render the background image in the background, all below will be child objects of canvas
canvas = app.CTkCanvas(master=frame, width=512, height=688)
canvas.pack(fill="both", expand=True)
#loading that background image ;)
backgroundImage = Image.open(resource_path("waifu.png"))
backgroundPhoto = ImageTk.PhotoImage(backgroundImage)
#create the background image from the loaded image
canvas.create_image(0, 0, anchor="nw", image=backgroundPhoto)
canvas.bind("<Button-1>", unfocus)


#Set fonts for use later
titleFont = customtkinter.CTkFont("Cascadia Code", size=25, weight='bold')
labelFont = customtkinter.CTkFont("Cascadia Code", size=20, weight='normal')
placeHolderFont = customtkinter.CTkFont("Cascadia Code", size=23, weight='normal')
buttonFont = customtkinter.CTkFont("Cascadia Code", size=20, weight='bold')

#make a label with padding
label = app.CTkLabel(master=canvas, text = "AutoClicker: Waifu edition", bg_color= "black",font=titleFont)
label.pack(pady=40, padx=5)

#make a entry field for user input for clicks per second
entry = app.CTkEntry(master=canvas, placeholder_text= "clicks per second", bg_color="black",font=placeHolderFont, width=300,height=50,justify="center")
entry.pack(pady=12, padx=2)

#make a label for the shortcut the user has set
keyShortCutLabel = app.CTkLabel(master=canvas, text= "Current short cut",bg_color="black",font=labelFont)
keyShortCutLabel.pack(pady=1, padx=10)


#create a button frame to stick the button on
buttonFrame = app.CTkFrame(master=canvas, bg_color="#33b249",corner_radius=4,border_width=0)
buttonFrame.pack(pady=1, padx=10)

#create a set keybind button for the user to click and add it to the button frame
button = app.CTkButton(master=buttonFrame, text="Set keybind", command=startButton,font=buttonFont,fg_color="#097969",border_width=0)
button.pack(pady=1, padx=1)

#just displays current status
errorLogLabel = app.CTkLabel(master=canvas, text="Waiting for senpai :p", bg_color="black",font=labelFont)
errorLogLabel.pack(pady=40, padx=10)

#Add click button
clickButton = app.CTkButton(master=canvas, text="Set keybind", command=testClicker,font=buttonFont,fg_color="#097969",border_width=0)
clickButton.pack(pady=1, padx=1)

root.mainloop()