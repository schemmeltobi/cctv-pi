
import datetime
import os
import base64
from dotenv import load_dotenv
from PIL import ImageFont, ImageDraw, Image
from picamera2 import Picamera2

############################################################
###########               Load Env
############################################################


load_dotenv()

font_file = os.getenv("PATH_TO_FONFTILE", None)


def init_camera_for_photos(x_res : int =2592, y_res : int =1944) -> Picamera2:
    """
    Returns initialized camera. 
    Default: Maximum resolution for raspberry pi V1 camera
    """
    picam = Picamera2()
    camera_config = picam.create_still_configuration(main={"size": (x_res,y_res)})
    picam.configure(camera_config)

    # fix exposure and gain according to lighting situation in basement
    # TODO works only on the firs shot
    picam.controls.AnalogueGain = 16.0
    picam.controls.ExposureTime = 30000

    return picam

def take_photo(camera: Picamera2) -> str:
    """
    Starts camera and takes a picture.
    Returns the path at which it is saved.
    """

    # Potentially move this out of this method to save overhead
    if not camera.started:
        camera.start()

    now = datetime.datetime.now()
    filepath = f"img/photo_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}___{base64.urlsafe_b64encode(os.urandom(8))[:4].decode()}.jpg"

    camera.capture_file(filepath)

    # Potentially move this out of this method to save overhead
    #camera.stop()

    metadata = camera.capture_metadata()
    print(f"Exposure: {metadata['ExposureTime']}   Analogue gain: {metadata['AnalogueGain']}")

    watermark_image(filepath=filepath, timestamp=now)

    print(f"Took image at {filepath}")
    return filepath


def watermark_image(filepath, timestamp: datetime = None) -> None:
    """
    Watermarks image at filepath with a timestamp
    If no timestamp is given datetime.now() is used.
    """
    if not timestamp:
        timestamp = datetime.datetime.now()
    
    orig_img = Image.open(filepath)
    image = orig_img.rotate(angle=90, expand=True)

    draw = ImageDraw.Draw(image)
    w, h = image.size
    font_size = h/25
    x = font_size
    y = font_size
    if font_file:
        font = ImageFont.truetype(font=font_file, size=int(font_size))
    else:
        font = ImageFont.load_default() 
    draw.text((x, y), str(timestamp), fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0), font=font, anchor='ls')

    image.save(filepath)

