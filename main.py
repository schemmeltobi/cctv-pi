from bottle import Bottle, run, static_file, template
from camera import take_photo, init_camera_for_photos
from gpiozero import MotionSensor
from threading import Thread, Event



app = Bottle()


# initialize camera
cam = init_camera_for_photos()


# initialize motion sensor
pir = MotionSensor(17)


most_recent_path = ""



############################################
###########     ROUTES
############################################

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='/home/pi/img')

@app.route('/webcam')
def web_cam():
    currently_capturing = pir.is_active

    if currently_capturing:
        # if camera is currently capturing display the latest file
        path = most_recent_path
    else:
        # take recent picture
        path = take_photo(camera=cam)

    filename = path.split('/')[-1]

    # show file
    #return static_file(path.split('/')[-1], root="/home/pi/img" )
    return template('webcam', is_active=currently_capturing, img_path=filename)

@app.route('/pir')
def motion_sensor():
    return f"Motion sensor active: {pir.is_active}"


############################################
###########   Motion Sensor Madness
############################################


def start_motion_thread():
    """
    This method gets triggered by the motion sensor. It creates a stop_event for the thread, that is capturing 
    the images while the motion sensor is active. The capturing needs to be started in a different thread, in
    order to be able to interrupt it once the motion sensor is deactivated again.
    """
    print("Registered motion; starting to take pictures!")

    # unique Event for stopping the capturing thread
    stop_event = Event()

    # thread, while sensor is active
    def start_capturing():
        # loop while sensor registers motion
        while True:
            # take picture
            filepath = take_photo(cam)
            global most_recent_path
            most_recent_path = filepath

            if stop_event.is_set():
                break

    # start method, while motion sensor is active
    t = Thread(target=start_capturing, daemon=True)
    t.start()

    def stop_thread():
        print("Not registering motion; stopping the taking of pictures")
        stop_event.set()
 

    # stopping thread when motions sensor deactivates  
    pir.when_deactivated = stop_thread



pir.when_activated = start_motion_thread

run(app, host='0.0.0.0', port=8080)
