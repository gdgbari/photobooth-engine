# 📸 Photobooth

A simple **photobooth** app that takes pictures and prints them with a **miniportraits-style overlay**, perfect for events, parties, and interactive installations.

## ✨ Features

- Captures photos using a connected camera
- Applies a miniportraits-style PNG overlay 
- Customizable with your own graphic effects
- Automatically prints the final image
- Easy configuration via YAML file

## 📦 Technical specifications

- [LINUX](https://www.kernel.org/) as OS ([Ubuntu distribution](https://ubuntu.com/) is recommended)
- [gphoto2](https://github.com/jim-easterbrook/python-gphoto2) library in order to shoot photos via PC (run **sudo apt install gphoto2** to install it)
- [Python](https://www.python.org/downloads/) (recommended: 3.8+)
- [Gutenprint](https://gimp-print.sourceforge.io/) driver in order to print edited miniportraits via bash commands
- [YAML](https://pypi.org/project/PyYAML/) library in order to easily set camera, paths and printing configuration's parameters
- [gphoto2](https://github.com/jim-easterbrook/python-gphoto2) compatible camera (run gphoto2 **--list-cameras** to know which cameras you can use)
- [Gutenprint](https://gimp-print.sourceforge.io/) compatible printer

Have fun ;)