from bottle import Bottle, run, static_file, template
from camera import take_photo, init_camera_for_photos
from gpiozero import MotionSensor, DigitalOutputDevice
from threading import Thread, Event
import time



############################################
###########     Init objects
############################################


# bottle app
app = Bottle()

# initialize camera
cam = init_camera_for_photos(x_res=1296, y_res=972)

# initialize motion sensor
pir = MotionSensor(17)
relais = DigitalOutputDevice(27, active_high=False, initial_value=False)

# initialize as global variable
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
        relais.on()
        time.sleep(0.2)
        path = take_photo(camera=cam)
        relais.off()

    filename = path.split('/')[-1]

    # show file
    return template('webcam', is_active=currently_capturing, img_path=filename)


@app.route('/webcam/dark')
def web_cam():
    currently_capturing = pir.is_active

    if currently_capturing:
        # if camera is currently capturing display the latest file
        path = most_recent_path
    else:
        # take recent picture
        #relais.on()
        time.sleep(0.2)
        path = take_photo(camera=cam)
        #relais.off()

    filename = path.split('/')[-1]

    # show file
    return template('webcam', is_active=currently_capturing, img_path=filename)


@app.route('/sensors')
def motion_sensor():
    return f"Motion sensor active: {pir.is_active}   ====   Relais active: {relais.is_active}"


############################################
###########   Motion Sensor Madness
############################################


def start_motion_thread():
    """
    This method gets triggered by the motion sensor. It creates a stop_event for the thread, that is capturing 
    the images while the motion sensor is active. The capturing needs to be started in a different thread, in
    order to be able to interrupt it once the motion sensor is deactivated again.
    """
    print("Registered motion")
    relais.on()
    print("Turned on light")


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
        print("Not registering motion anymore")
        relais.off()
        print("Turned off light")
        print("Stop taking pictures")
        stop_event.set()
 

    # stopping thread when motions sensor deactivates  
    pir.when_deactivated = stop_thread


pir.when_activated = start_motion_thread



run(app, host='0.0.0.0', port=8080)