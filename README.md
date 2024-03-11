# CCTV using Raspberry Pi 



# Setup on Raspberry Pi

Packages that need to be installed on PiOs Lite:

```
sudo apt install build-essential libcap-dev libavformat-dev libavdevice-dev libcamera-dev
```

Do not try to run the python script inside a virtual env. Install picamera2 package using apt and not pip. Follow the instructions here from the [documentation page](https://pypi.org/project/picamera2/)

Add a font file to this folder. Configure the font name in camera.py to match the font that you downloaded. I am using arial.ttf


https://gpiozero.readthedocs.io/en/latest/recipes.html#motion-sensor


Followed this tutorial for setting it up as a systemd.service https://github.com/torfsen/python-systemd-tutorial