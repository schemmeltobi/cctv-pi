
import datetime
import time
import os
import base64
from PIL import ImageFont, ImageDraw, Image
from picamera2 import Picamera2

def init_camera_for_photos(x_res : int =2592, y_res : int =1944) -> Picamera2:
    """
    Returns initialized camera. 
    Default: Maximum resolution for raspberry pi V1 camera
    """
    picam = Picamera2()
    camera_config = picam.create_still_configuration(main={"size": (x_res,y_res)})
    picam.configure(camera_config)

    return picam

def take_photo(camera: Picamera2) -> str:
    """
    Starts camera and takes a picture.
    Returns the path at which it is saved.
    """

    # Potentially move this out of this method to save overhead
    camera.start()

    now = datetime.datetime.now()
    filepath = f"img/photo_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}___{base64.b64encode(os.urandom(8))[:4].decode()}.jpg"

    camera.capture_file(filepath)


    # Potentially move this out of this method to save overhead
    camera.stop()

    watermark_image(filepath=filepath, timestamp=now)
    return filepath


def watermark_image(filepath, timestamp: datetime = None) -> None:
    """
    Watermarks image at filepath with a timestamp
    If no timestamp is given datetime.now() is used.
    """
    if not timestamp:
        timestamp = datetime.datetime.now()
    
    image = Image.open(filepath)

    draw = ImageDraw.Draw(image)
    w, h = image.size
    font_size = h/20
    x = w/20
    y = h - font_size
    font = ImageFont.truetype("arial.ttf", int(font_size))



    draw.text((x, y), str(timestamp), fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0), font=font, anchor='ls')
    image.save(filepath)






# if __name__ == "__main__":
#     cam = init_camera_for_photos()
#     path = take_photo(cam)
#     print(f"Filepath: {path}")



