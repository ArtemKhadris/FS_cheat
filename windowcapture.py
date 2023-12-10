import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:

    w = 0
    h = 0
    ws = 0
    hs = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, window_name=None):
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect [0]
        self.h = window_rect[3] - window_rect[1]
        border_pixels = 8
        titlebar_pixels = 30
        #self.w = self.w - (border_pixels * 2)
        #self.h = self.h - titlebar_pixels - border_pixels
        self.w = 650
        self.h = 60
        self.ws = 300
        self.hs = 80
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y


    def get_screenshot(self):
        #bmpfilenamename = "out.bmp" #set this
        
        #hwnd = None
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x+200,self.cropped_y+565), win32con.SRCCOPY)
        #cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x,self.cropped_y), win32con.SRCCOPY)
        #dataBitMap.SaveBitmapFile(cDC, "out.bmp")
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img1 = np.fromstring(signedIntsArray, dtype='uint8')
        img1.shape = (self.h,self.w,4)
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img1 = img1[..., :3]
        img1 = np.ascontiguousarray(img1)
        #bmpfilenamename = "out.bmp" #set this
        
        #hwnd = None
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.ws, self.hs)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.ws, self.hs) , dcObj, (self.cropped_x+470,self.cropped_y+540), win32con.SRCCOPY)
        #cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x,self.cropped_y), win32con.SRCCOPY)
        #dataBitMap.SaveBitmapFile(cDC, "out.bmp")
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img2 = np.fromstring(signedIntsArray, dtype='uint8')
        img2.shape = (self.hs,self.ws,4)
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img2 = img2[..., :3]
        img2 = np.ascontiguousarray(img2)
        return img1, img2
    
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)