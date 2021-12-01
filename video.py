from __future__ import print_function
from sys import platform
if(platform == 'win32'):
    import winsound

import os
try:
    from pywintypes import DEVMODEType, error
    import win32api
    import os
    import sys
    import time
    import ctypes
    from sys import platform
    import cv2
    import imutils
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from BlurWindow.blurWindow import GlobalBlur

except:
    os.system('pip install PySide2')
    os.system('pip install pywin32')
    os.system('pip install pypiwin32')
    os.system('pip install opencv-python')
    os.system('pip install imutils')
    os.system('pip install BlurWindow')
    from pywintypes import DEVMODEType, error
    import win32api
    import os
    import sys
    import time
    import ctypes
    from sys import platform
    import cv2
    import imutils

class MainWindow(QWidget):
    def __init__(self,width=500,height=500):
        super(MainWindow, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(width, height)
        GlobalBlur(self.winId(),Dark=True,QWidget=self)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

class ScreenRes(object):
    @classmethod
    def set(cls, width=None, height=None, depth=32):
        '''
        Set the primary display to the specified mode
        '''
        # if width and height:
        #     print('Setting resolution to {}x{}'.format(width, height, depth))
        # else:
        #     print('Setting resolution to defaults')

        if sys.platform == 'win32':
            cls._win32_set(width, height, depth)
        elif sys.platform.startswith('linux'):
            cls._linux_set(width, height, depth)
        elif sys.platform.startswith('darwin'):
            cls._osx_set(width, height, depth)

    @classmethod
    def get(cls):
        if sys.platform == 'win32':
            return cls._win32_get()
        elif sys.platform.startswith('linux'):
            return cls._linux_get()
        elif sys.platform.startswith('darwin'):
            return cls._osx_get()

    @classmethod
    def get_modes(cls):
        if sys.platform == 'win32':
            return cls._win32_get_modes()
        elif sys.platform.startswith('linux'):
            return cls._linux_get_modes()
        elif sys.platform.startswith('darwin'):
            return cls._osx_get_modes()

    @staticmethod
    def _win32_get_modes():
        '''
        Get the primary windows display width and height
        '''
        
        modes = []
        i = 0
        try:
            while True:
                mode = win32api.EnumDisplaySettings(None, i)
                modes.append((
                    int(mode.PelsWidth),
                    int(mode.PelsHeight),
                    int(mode.BitsPerPel),
                    ))
                i += 1
        except error:
            pass

        return modes

    @staticmethod
    def _win32_get():
        '''
        Get the primary windows display width and height
        '''
        
        user32 = ctypes.windll.user32
        screensize = (
            user32.GetSystemMetrics(0), 
            user32.GetSystemMetrics(1),
            )
        return screensize

    @staticmethod
    def _win32_set(width=None, height=None, depth=32):
        '''
        Set the primary windows display to the specified mode
        '''
        # Gave up on ctypes, the struct is really complicated
        #user32.ChangeDisplaySettingsW(None, 0)

        if width and height:

            if not depth:
                depth = 32

            mode = win32api.EnumDisplaySettings()
            mode.PelsWidth = width
            mode.PelsHeight = height
            mode.BitsPerPel = depth

            win32api.ChangeDisplaySettings(mode, 0)
        else:
            win32api.ChangeDisplaySettings(None, 0)


    @staticmethod
    def _win32_set_default():
        '''
        Reset the primary windows display to the default mode
        '''
        # Interesting since it doesn't depend on pywin32
        user32 = ctypes.windll.user32
        # set screen size
        user32.ChangeDisplaySettingsW(None, 0)

    @staticmethod
    def _linux_set(width=None, height=None, depth=32):
        raise NotImplementedError()

    @staticmethod
    def _linux_get():
        raise NotImplementedError()

    @staticmethod
    def _linux_get_modes():
        raise NotImplementedError()

    @staticmethod
    def _osx_set(width=None, height=None, depth=32):
        raise NotImplementedError()

    @staticmethod
    def _osx_get():
        raise NotImplementedError()

    @staticmethod
    def _osx_get_modes():
        raise NotImplementedError()






    #ScreenRes.set(1920, 1080)
    #ScreenRes.set() # Set defaults




# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# To capture video from webcam. 
cap = cv2.VideoCapture(0)
# To use a video file as input

batas_width = 300
batas_height = 300
ganti = 0


while True:
    # Read the frame
    _, img = cap.read()
    img = imutils.resize(img, width=800,height=800)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        mw = MainWindow()
        if((w>batas_width) and (h>batas_height)):
            lebarnya,tingginya = ScreenRes.get()
            mw.showFullScreen()
            app.processEvents()
            #time.sleep(3) ngatur selang waktunya agar lebih mudah gitu
        else:
            mw.hide()
            app.processEvents()
            #sys.exit(app.exec_())
            #ScreenRes.set(lebarnya,tingginyra,32)
            #time.sleep(3)
        #app.exec_()
    # resolution  
    #cv2.imshow('img', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
        
# Release the VideoCapture object
cap.release()