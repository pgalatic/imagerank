# TODO
# 2) Add progress bar to GUI (tqdm?)
# 4) Verify images land in folders properly
# 5) Add zoom functionality

# STANDARD LIB
import os
import pdb
import sys
import pathlib

# EXTERNAL LIB
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import win32api

# LOCAL LIB
from imagerank import Ranker

class GUI():
    def __init__(self, folder=None):
    
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
    
        self._scores = []
        self._size = (width // 2, height)
        
        self._root = tk.Tk()
        self._root.title('Image Ranker')
        self._root.attributes('-fullscreen', True)
    
        if folder:
            self._folder = pathlib.Path(folder)
        else:
            self._folder = pathlib.Path(filedialog.askdirectory(
                parent=self._root,
                initialdir=os.getcwd(),
                title='Please select a folder:'
            ))
        
        self._ranker = Ranker(self._folder)
        
        self._nameA, self._nameB = self._ranker.query()
        
        self._panelA = tk.Label(self._root, image=None)
        self._panelB = tk.Label(self._root, image=None)
        
        self._panelA.pack(side='left')
        self._panelB.pack(side='right')
        
        self._progress = ttk.Progressbar(self._root, orient=tk.VERTICAL, length=height - (height * 0.1))
        self._progress.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.update_images()
        
        # User can click on an image to select it
        self._panelA.bind('<Button-1>', lambda e: self.var_left())
        self._panelB.bind('<Button-1>', lambda e: self.var_right())
        # User can use A-D to select images
        self._root.bind('a', lambda e: self.var_left())
        self._root.bind('d', lambda e: self.var_right())
        # User can use arrow keys to select images
        self._root.bind('<Left>', lambda e: self.var_left())
        self._root.bind('<Right>', lambda e: self.var_right())
        
        self._root.focus_set()
        self._root.mainloop()
    
    def var_left(self):
        self._ranker.process(self._nameA, self._nameB)
        self.update_images()
    
    def var_right(self):
        self._ranker.process(self._nameB, self._nameA)
        self.update_images()
    
    def update_images(self):
        self._nameA, self._nameB = self._ranker.query()
        self._progress['value'] = self._ranker.progress() * 100

        if self._nameA is None:
            self._ranker.finish()
            self._root.destroy()
            sys.exit()
        
        imgA = Image.open(self._folder / self._nameA)
        imgB = Image.open(self._folder / self._nameB)
        
        imgA.thumbnail(self._size)
        imgB.thumbnail(self._size)
        
        imgA = ImageTk.PhotoImage(imgA)
        imgB = ImageTk.PhotoImage(imgB)
        
        self._panelA.configure(image=imgA)
        self._panelB.configure(image=imgB)
        
        self._panelA.image = imgA
        self._panelB.image = imgB
        
if __name__ == '__main__':
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        gui = GUI(sys.argv[1])
    else:
        gui = GUI()
        