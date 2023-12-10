import keyboard as kb
import ctypes
import time
#from pyautogui import press
#import win32api
#import win32con

def up(t):
    kb.press("up arrow")
    time.sleep(t)
    kb.release("up arrow")

def down(t):
    kb.press("down arrow")
    time.sleep(t)
    kb.release("down arrow")

def left(t):
    kb.press("left arrow")
    time.sleep(t)
    kb.release("left arrow")

def right(t):
    kb.press("right arrow")
    time.sleep(t)
    kb.release("right arrow")

def upr(t):
    ctypes.windll.user32.keybd_event(105, 0, 0, 0)
    time.sleep(t)
    ctypes.windll.user32.keybd_event(105, 0, 2, 0)
    #kb.press_and_release("num 9")
    #win32api.keybd_event(105, 0, 0, 0)
    #win32api.keybd_event(105, 0, win32con.KEYEVENTF_KEYUP, 0)

def upl(t):
    ctypes.windll.user32.keybd_event(103, 0, 0, 0)
    time.sleep(t)
    ctypes.windll.user32.keybd_event(103, 0, 2, 0)
    #kb.press_and_release("num 7")
    #win32api.keybd_event(103, 0, 0, 0)
    #win32api.keybd_event(103, 0, win32con.KEYEVENTF_KEYUP, 0)

def downr(t):
    ctypes.windll.user32.keybd_event(99, 0, 0, 0)
    time.sleep(t)
    ctypes.windll.user32.keybd_event(99, 0, 2, 0)
    #kb.press_and_release("num 3")
    #win32api.keybd_event(99, 0, 0, 0)
    #win32api.keybd_event(99, 0, win32con.KEYEVENTF_KEYUP, 0)

def downl(t):
    ctypes.windll.user32.keybd_event(97, 0, 0, 0)
    time.sleep(t)
    ctypes.windll.user32.keybd_event(97, 0, 2, 0)
    #kb.press_and_release("num 1")
    #win32api.keybd_event(97, 0, 0, 0)
    #win32api.keybd_event(97, 0, win32con.KEYEVENTF_KEYUP, 0)

def space():
    kb.press_and_release("space")

def press_f1():
    VK_F1 = 0x70
    ctypes.windll.user32.keybd_event(VK_F1, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_F1, 0, 2, 0)

def press_f2():
    VK_F2 = 0x71
    ctypes.windll.user32.keybd_event(VK_F2, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_F2, 0, 2, 0)

def press_f3():
    VK_F3 = 0x72
    ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

def press_f4():
    VK_F4 = 0x73
    ctypes.windll.user32.keybd_event(VK_F4, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_F4, 0, 2, 0)

def press_f5():
    VK_F5 = 0x74
    ctypes.windll.user32.keybd_event(VK_F5, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_F5, 0, 2, 0)