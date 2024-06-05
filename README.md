# CCTV using Raspberry Pi 

Small project to catch the shoe thieve in my apartement building.

# Setup on Raspberry Pi

## Initial Rasperry Pi setup

I recommend using PiOs Lite as an operating system and adding packages as necessary.

Install basic packages:
```
sudo apt install git
```

## Providing a font file for timestamps

Provide a font file and specify the path to it with `PATH_TO_FONFTILE`.


## Setting up CCTV

Do not try to run the python script inside a virtual env. It does not play nicely with picamera2. 
The python version from PiOs wants you to use apt to install python modules instead of pip.


```
$ sudo apt install python3-bottle python3-pillow python3-picamera2 python3-dotenv python3-nc-py-api
$ git clone https://github.com/schemmeltobi/cctv-pi.git
$ cd cctv-pi
$ python main.py
```

## Setting it up as a service

Follow this tutorial for setting it up as a systemd.service https://github.com/torfsen/python-systemd-tutorial




#### Useful links

https://gpiozero.readthedocs.io/en/latest/recipes.html#motion-sensor

