import os
import sys
import tkinter as tk
from tkinter import filedialog
from imagerank import Ranker
from PIL import ImageTk, Image

MAXSIZE = (800, 800)

class GUI():
    def __init__(self):
    
        self._scores = []
        
        self._root = tk.Tk()
        self._root.title('Image Ranker')
                
        self._folder = filedialog.askdirectory(
            parent=self._root,
            initialdir=os.getcwd(),
            title='Please select a folder:'
        ) + '/'
        
        if self._folder == '/':
            sys.exit()
        
        self._ranker = Ranker(self._folder)
        
        self._nameA, self._nameB = self._ranker.query()
        
        imgA = Image.open(self._folder + self._nameA)
        imgB = Image.open(self._folder + self._nameB)
        imgA = ImageTk.PhotoImage(imgA.resize(MAXSIZE, Image.ANTIALIAS))
        imgB = ImageTk.PhotoImage(imgB.resize(MAXSIZE, Image.ANTIALIAS))
        
        self._panelA = tk.Label(self._root, image=imgA)
        self._panelB = tk.Label(self._root, image=imgB)
        
        self._panelA.pack(side='left')
        self._panelB.pack(side='right')
        
        self._panelA.bind('<Button-1>', lambda e: self.var_left())
        self._panelB.bind('<Button-1>', lambda e: self.var_right())
                
        self._root.mainloop()
    
    def var_left(self):
        self._ranker.process(self._nameA, self._nameB)
        self.update_images()
    
    def var_right(self):
        self._ranker.process(self._nameB, self._nameA)
        self.update_images()
        
    def update_images(self):
        self._nameA, self._nameB = self._ranker.query()
        if self._nameA is None:
            print('yes')
            self._ranker.finish()
            self._root.destroy()
            sys.exit()
        
        imgA = Image.open(self._folder + self._nameA)
        imgB = Image.open(self._folder + self._nameB)
        imgA = ImageTk.PhotoImage(imgA.resize(MAXSIZE, Image.ANTIALIAS))
        imgB = ImageTk.PhotoImage(imgB.resize(MAXSIZE, Image.ANTIALIAS))
        self._panelA.configure(image=imgA)
        self._panelB.configure(image=imgB)
        self._panelA.image = imgA
        self._panelB.image = imgB
        
if __name__ == '__main__':
    gui = GUI()
        