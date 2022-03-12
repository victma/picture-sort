import glob
import os
import argparse
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps

class App:
  imageExtensions = ['jpg', 'JPG', 'jpeg']

  def __init__(self, directory, leftDirName, rightDirName) -> None:
      self.directory = directory
      self.leftDirectory = os.path.join(directory, leftDirName)
      self.rightDirectory = os.path.join(directory, rightDirName)
      self.currentFile = None
      self.image = None
      self.imageWidget = None
      self.fileList = []
      self.help = f'← or <space> : "{leftDirName}" directory | → or ⏎ : "{rightDirName}" directory | <s> : skip'

  def init(self):
    self.getFileList()
    if len(self.fileList) == 0:
      return f"Could not find any file in {self.directory}"

  def getFileList(self):
    self.fileList = []
    for extension in App.imageExtensions:
      self.fileList.extend(glob.glob(f'{self.directory}/*.{extension}'))
    self.fileList.sort(reverse=True)

  def getCurrentFileName(self):
    return os.path.basename(self.currentFile)

  def left(self, event):
    if not self.currentFile:
      return
    print(f"<- Left     | {self.currentFile}")
    os.renames(self.currentFile, os.path.join(self.leftDirectory, self.getCurrentFileName()))
    self.nextImage()

  def right(self, event):
    if not self.currentFile:
      return
    print(f"   Right -> | {self.currentFile}")
    os.renames(self.currentFile, os.path.join(self.rightDirectory, self.getCurrentFileName()))
    self.nextImage()

  def skip(self, event):
    if not self.currentFile:
      return
    self.nextImage()

  def nextImage(self):
    if self.image:
      self.image.close()

    if len(self.fileList) == 0:
      self.imageWidget.configure(image=None, text=f"Done ! No image left in {self.directory}")
      self.imageWidget.image = None
      self.currentFile = None
      return
    
    self.currentFile = self.fileList.pop()
    originalImage = Image.open(self.currentFile)
    if originalImage.height > 1000:
      self.image = ImageOps.scale(originalImage, 1000 / originalImage.height)
    else:
      self.image = originalImage
    photoImage = ImageTk.PhotoImage(self.image)
    
    self.imageWidget.configure(image=photoImage)
    self.imageWidget.image = photoImage

  def run(self):
    error = self.init()
    if error:
      print(error)
      exit(1)

    root = Tk()
    root.title("Picture Sort")

    mainframe = ttk.Frame(root)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    self.imageWidget = ttk.Label(mainframe)
    self.imageWidget.grid(row=0, column=0, sticky=(N, W, E))

    helpLabel = ttk.Label(mainframe, text=self.help)
    helpLabel.grid(row=1, column=0, sticky=(S), padx=16, pady=16)

    self.nextImage()

    root.bind("<KeyPress-Left>", self.left)
    root.bind("<KeyPress-space>", self.left)
    root.bind("<KeyPress-Right>", self.right)
    root.bind("<KeyPress-Return>", self.right)
    root.bind("<KeyPress-s>", self.skip)

    root.mainloop()


def main():
  argParser = argparse.ArgumentParser(description="Sort pictures in 2 categories quickly.\
    Use <Arrow-Left> and <Arrow-Right> (or <Space> and <Enter> respectively) to send the current picture to the correspnding directory. Press <S> to skip.",
    epilog="Hope this helps you finally sort these holiday pictures from 2006.")
  argParser.add_argument("--left", "-l", dest="leftDir", default="left", help='Custom name of the directory for <Arrow-Left> (or <Space>) key (eg. "bad", "throw"...). Defaults to "left"')
  argParser.add_argument("--right", "-r", dest="rightDir", default="right", help='Custom name of the directory for <Arrow-Right> (or <Enter>) key (eg. "good", "keep"...). Defaults to "right"')
  argParser.add_argument("directory", help="Path to the directory where the pictues are located.")
  args = argParser.parse_args()
  app = App(args.directory, args.leftDir, args.rightDir)
  app.run()

if __name__ == "__main__":
  main()
