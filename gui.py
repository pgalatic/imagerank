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
                
        self._filepath = filedialog.askdirectory(
            parent=self._root,
            initialdir=os.getcwd(),
            title='Please select a folder:'
        )
        
        self._ranker = Ranker(self._filepath)
        
        self._combos = self._ranker.query()
        self._counter = 1
        self._var = tk.IntVar()
        
        imgA = Image.open(self._filepath + '/' + self._combos[0][0])
        imgA = ImageTk.PhotoImage(imgA.resize(MAXSIZE, Image.ANTIALIAS))

        imgB = Image.open(self._filepath + '/' + self._combos[0][1])
        imgB = ImageTk.PhotoImage(imgB.resize(MAXSIZE, Image.ANTIALIAS))
        
        self._panelA = tk.Label(self._root, image=imgA)
        self._panelB = tk.Label(self._root, image=imgB)
        
        self._panelA.pack(side='left')
        self._panelB.pack(side='right')
        
        self._panelA.bind('<Button-1>', lambda e: self.var_left())
        self._panelB.bind('<Button-1>', lambda e: self.var_right())
                
        self._root.mainloop()
    
    def var_left(self):
        self._var.set(0)
        self.nextimage()
    
    def var_right(self):
        self._var.set(1)
        self.nextimage()
        
    def nextimage(self):
        if self._counter >= len(self._combos):
            self._ranker.process(self._scores)
            self._root.destroy()
            sys.exit()
        
        imgA = Image.open(self._filepath + '/' + self._combos[self._counter][0])
        imgA = ImageTk.PhotoImage(imgA.resize(MAXSIZE, Image.ANTIALIAS))
        
        imgB = Image.open(self._filepath + '/' + self._combos[self._counter][1])
        imgB = ImageTk.PhotoImage(imgB.resize(MAXSIZE, Image.ANTIALIAS))
    
        self._panelA.configure(image=imgA)
        self._panelB.configure(image=imgB)
        self._panelA.image = imgA
        self._panelB.image = imgB
        
        if self._var.get() == 0:
            self._scores.append((1, -1))
        elif self._var.get() == 1:
            self._scores.append((-1, 1))
        else:
            print(self._var.get())
            raise Exception('Something went wrong in nextimage()!')
        
        self._var.set(-1)
        
        self._counter += 1
        
if __name__ == '__main__':
    gui = GUI()
        