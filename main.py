from PIL import ImageGrab
from globalhotkeys import GlobalHotKeys
from threading import Thread
import pyautogui
import time
import dearpygui.dearpygui as gui

windowSize = (400, 350)
screenSize = pyautogui.size()
clickCoordinates = (950, 385)
offset = 75
isRunning = False
fishes = 0

# Hotkeys
@GlobalHotKeys.register(GlobalHotKeys.VK_F10, "VK_F10")
def TurnOffBot(sender=None, data=None):
    global isRunning
    gui.set_value(1, "Running: False")
    isRunning = False

@GlobalHotKeys.register(GlobalHotKeys.VK_F9, "VK_F9")
def RunBot(sender=None, data=None):
    global isRunning
    isRunning = True
    pyautogui.click(clickCoordinates)
    gui.set_value(1, "Running: True")

@GlobalHotKeys.register(GlobalHotKeys.VK_F8, "VK_F8")
def SetNewClickCoordinates():
    ChangeClickCoordinates(None, pyautogui.position())
    gui.set_value(20, clickCoordinates)

# Main bot functions
def CheckForFish(imageCheck):
    for x in range(clickCoordinates[0] - offset, clickCoordinates[0] + offset):
        for y in range(clickCoordinates[1] - offset, clickCoordinates[1] + offset):
            color = imageCheck.getpixel((x, y))
            if color == (55, 97, 137) or color == (50, 89, 128):
                return True
    return False

def ChangeClickCoordinates(sender, data):
    global clickCoordinates
    x, y = data

    if x > screenSize[0] - offset - 1:
        x = screenSize[0] - offset - 1
    if y > screenSize[1] - offset - 1:
        y = screenSize[1] - offset - 1

    clickCoordinates = x, y

def ChangeOffset(sender, data):
    global offset
    offset = data

def MainLoop():
    global fishes
    while gui.is_dearpygui_running():
        time.sleep(0.1)
        # print("MainLoop")
        if isRunning:
            image = ImageGrab.grab()
            isGettingFish = CheckForFish(image)
            if isGettingFish:
                time.sleep(0.5)
                pyautogui.click(clickCoordinates)

                fishes += 1
                gui.set_value(10, "Collected times: " + str(fishes))

                time.sleep(0.5)
                pyautogui.click(clickCoordinates)

        gui.render_dearpygui_frame()

# Functions needed for looping in threads
def ThreadMainLoop():
    while True:
        MainLoop()
def ThreadGlobalHotkeysLoop():
    while True:
        GlobalHotKeys.listen()

gui.create_context()

gui.create_viewport(title="Necesse fishing bot", width=windowSize[0], height=windowSize[1])
gui.setup_dearpygui()
gui.set_global_font_scale(1.3)
gui.set_viewport_resizable(False)
gui.set_viewport_always_top(True)

with gui.window(tag="Primary window"):
    gui.add_text("Collected times: 0", tag=10)

    gui.add_button(label="Start Fishing", callback=RunBot, width=160, height=50, pos=(20, windowSize[1] - 105))
    gui.add_button(label="Stop fishing", callback=TurnOffBot, width=160, height=50, pos=(windowSize[0] - 195, windowSize[1] - 105))

    gui.add_input_intx(label="Clicking Coordinates(x,y)", tag=20, default_value=clickCoordinates, size=2, width=125, callback=ChangeClickCoordinates)
    gui.add_input_int(label="Area size", default_value=offset, width=125, callback=ChangeOffset)

    gui.add_spacing(count=8)
    gui.add_separator()

    gui.add_text("GLOBAL HOTKEYS: \nF8 - to set coordinates for mouse\nF9 - to start fishing\nF10 - to stop fishing")

    gui.add_spacing(count=4)
    gui.add_text("Running: False", tag=1)

gui.show_viewport()
gui.set_primary_window("Primary window", True)

# It is not a good way of doing it but only works that way -.-
thread1 = Thread(target=ThreadMainLoop)
thread1.start()
thread2 = Thread(target=ThreadGlobalHotkeysLoop())
thread2.start()

thread2.join()
thread1.join()

gui.destroy_context()
