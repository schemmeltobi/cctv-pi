from bottle import Bottle, run, static_file
from camera import take_photo, init_camera_for_photos

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/webcam')
def web_cam():
    # take recent picture
    path = take_photo(camera=cam)

    # show file
    return static_file(path.split('/')[-1], root="/home/pi/img" )



# initialize camera
cam = init_camera_for_photos()

run(app, host='0.0.0.0', port=8080)