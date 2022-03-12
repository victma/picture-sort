import glob
import os
import argparse
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps

class App:
  imageExtensions = ['jpg', 'JPG', 'jpeg']
  numberOfPreviews = 5

  def __init__(self, directory, leftDirName, rightDirName) -> None:
      self.directory = directory
      self.leftDirectory = os.path.join(directory, leftDirName)
      self.rightDirectory = os.path.join(directory, rightDirName)
      self.currentFile = None
      self.image = None
      self.mainImageWidget = None
      self.nextImages = []
      self.nextImagesWidgets = []
      self.fileList = []
      self.previousFiles = []
      self.help = f'← or <space> : "{leftDirName}" directory | → or ⏎ : "{rightDirName}" directory | <s> : skip | <p> : previous'

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

  def getScaledImage(self, fileName, maxHeight):
    image = Image.open(fileName)
    if image.height > maxHeight:
      return ImageOps.scale(image, maxHeight / image.height)
    return image

  def left(self, event):
    if not self.currentFile:
      return
    print(f"<- Left     | {self.currentFile}")
    dest = os.path.join(self.leftDirectory, self.getCurrentFileName())
    os.renames(self.currentFile, dest)
    self.previousFiles.append(dest)
    self.nextImage()

  def right(self, event):
    if not self.currentFile:
      return
    print(f"   Right -> | {self.currentFile}")
    dest = os.path.join(self.rightDirectory, self.getCurrentFileName())
    os.renames(self.currentFile, dest)
    self.previousFiles.append(dest)
    self.nextImage()

  def skip(self, event):
    if not self.currentFile:
      return
    self.previousFiles.append(os.path.join(self.directory, self.getCurrentFileName()))
    self.nextImage()

  def previous(self, event):
    if len(self.previousFiles) == 0:
      return
    
    previousFile = self.previousFiles.pop()
    originalFile = os.path.join(self.directory, os.path.basename(previousFile))
    os.renames(previousFile, originalFile)
    self.fileList.append(self.currentFile)
    self.fileList.append(originalFile)

    print(len(self.nextImages))
    self.nextImages.insert(0, self.getScaledImage(originalFile, 200))
    print(len(self.nextImages))
    if (len(self.nextImages) > self.numberOfPreviews):
      self.nextImages.insert(0, self.nextImages.pop())
    else:
      self.nextImages.insert(0, None)

    self.nextImage()


  def nextImage(self):
    if self.image:
      self.image.close()

    if len(self.fileList) == 0:
      self.mainImageWidget.configure(image=None, text=f"Done ! No image left in {self.directory}")
      self.mainImageWidget.image = None
      self.currentFile = None
      return
    
    self.currentFile = self.fileList.pop()
    self.image = self.getScaledImage(self.currentFile, 1000)
    photoImage = ImageTk.PhotoImage(self.image)
    
    self.mainImageWidget.configure(image=photoImage)
    self.mainImageWidget.image = photoImage
    self.previewNext()


  def previewNext(self):
    if len(self.nextImages) > 0:
       firstImage = self.nextImages.pop(0)
       if firstImage:
         firstImage.close()
    
    if len(self.fileList) >= self.numberOfPreviews:
      image = self.getScaledImage(self.fileList[-self.numberOfPreviews], 200)
      self.nextImages.append(image)

    for i in range(len(self.nextImages)):
      photoImage = ImageTk.PhotoImage(self.nextImages[i])
      self.nextImagesWidgets[i].configure(image=photoImage)
      self.nextImagesWidgets[i].image = photoImage
    
    for i in range(self.numberOfPreviews - len(self.nextImages)):
      self.nextImagesWidgets[self.numberOfPreviews - 1 - i].configure(image=None)
      self.nextImagesWidgets[self.numberOfPreviews - 1 - i].image = None


  def initializePreview(self):
    for i in range(min(len(self.fileList), self.numberOfPreviews)):
      image = self.getScaledImage(self.fileList[-i - 1], 200)
      self.nextImages.append(image)

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
    for i in range(self.numberOfPreviews):
      mainframe.rowconfigure(i, weight=1)

    self.mainImageWidget = ttk.Label(mainframe)
    self.mainImageWidget.grid(row=0, column=0, rowspan=self.numberOfPreviews, sticky=(N, W))

    for i in range(self.numberOfPreviews):
      self.nextImagesWidgets.append(ttk.Label(mainframe))
      self.nextImagesWidgets[i].grid(row=i, column=1, sticky=(E))

    helpLabel = ttk.Label(mainframe, text=self.help)
    helpLabel.grid(row=self.numberOfPreviews, column=0, sticky=(S), padx=16, pady=16)

    self.initializePreview()
    self.nextImage()

    root.bind("<KeyPress-Left>", self.left)
    root.bind("<KeyPress-space>", self.left)
    root.bind("<KeyPress-Right>", self.right)
    root.bind("<KeyPress-Return>", self.right)
    root.bind("<KeyPress-s>", self.skip)
    root.bind("<KeyPress-p>", self.previous)

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
