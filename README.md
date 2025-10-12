# 📸 Photobooth

A simple **photobooth** app that takes pictures and prints them applying a **miniportraits-style overlay**, perfect for events, parties, and interactive installations.

## ✨ Features

- Captures photos using a connected camera
- Applies a miniportraits-style PNG overlay 
- Customizable with your own graphic effects
- Automatically prints the final image
- Easy configuration via YAML file

## 📦 Technical specifications

- [LINUX](https://www.kernel.org/) as operating system
- [gphoto2](https://github.com/jim-easterbrook/python-gphoto2) library in order to shoot photos via bash commands
- [Python](https://www.python.org/) (recommended: 3.8+)
- [Gutenprint](https://gimp-print.sourceforge.io/) driver in order to print edited miniportraits via bash commands
- [YAML](https://pypi.org/project/PyYAML/) library in order to easily set camera, paths and printing configuration's parameters
- [gphoto2](https://github.com/jim-easterbrook/python-gphoto2) compatible camera to be connected to your PC via USB
- [Gutenprint](https://gimp-print.sourceforge.io/) compatible printer to be connected to your PC via USB

## 📑 User guide

- Install [Python](https://www.python.org/) and its packet's manager ([pip](https://pypi.org/project/pip/)) (a packet's manager allows to install the libraries your code needs in order to be executed):
  - **sudo apt install python3 -y**
  - **sudo apt install python3-pip -y**
- Move to a folder of your choice and clone this GitHub repo (if you don't have [git](https://git-scm.com/) installed, run **sudo apt install git -y**):
  - **git clone https://github.com/gdgbari/photobooth.git**
- Install and activate a virtual environment in order to install and store the libraries your code needs to be executed (be sure to be in the folder where you previously cloned the repo):
  - **python3 -m venv .venv**
  - **source .venv/bin/activate**
  - **pip3 install -r requirements.txt**
  - **sudo apt install gphoto2 -y**
- Verify if your camera is supported by [gphoto2](https://github.com/jim-easterbrook/python-gphoto2):
  - **gphoto2 --list-cameras**
- If your camera is supported, connect it to your PC via USB, and verify if it's ready to be used from [gphoto2](https://github.com/jim-easterbrook/python-gphoto2):
  - **gphoto2 --auto-detect**
- Set configuration's parameters in **settings.yaml** file, inserting:
  - the path where you want your photos to be stored
  - your camera's name
  - your printer's name
  - the name of the event where you are shooting, in order to automatically name photo
- Run **python3 src/main.py** and you're finally ready to enjoy the software. 

Have fun!! ☺️☺️