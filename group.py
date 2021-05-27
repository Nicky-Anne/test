import serial
import MySQLdb
import time
import threading
from flask import Flask, render_template

device = '/dev/ttyACM1'

x = 1

arduino = serial.Serial(device, 115200)

app = Flask (__name__)

# Dictionary of pins with name of pin and state ON/OFF
pins = {
    13: {'name' : 'PIN 13', 'state' : 0}
}

def monitoring_loop():
    while True:
        while x == 1:
            if arduino.in_waiting > 0:
                line = arduino.readline()
                arduino.write(line)
                print(line)
                #publish.single(topic="v1/devices/me/telemetry",payload='{"Motion Sensor":' + str(int(line)) +'}', hostname="thingsboard

# Main function when accessing the website
@app.route("/")
def index():
    # TODO: Read the status of the pins ON/OFF and update dictionary
    # This data will be sent to index.html (pin dictionary)
    templateData = {
    'pins' : pins
    }
    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData)
    
# Function with buttons that toggle (change on to off or off to on) depending on the status
@app.route("/<changePin>/<toggle>")
def toggle_function(changePin, toggle):
    global x
    # Convert the pin from the URL into an integer
    changePin = int(changePin)
    # Get the device name for the pin being changed
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on", execute the code indented below:
    if toggle == "on":
    # Set the pin high:
        if changePin == 13:
            x = 1
            #arduino.write(b"1")
            pins[changePin]['state'] = 1
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + "on."
    # If the action part of the URL is "on", execute the code indented below:
    if toggle == "off":
    # Set the pin high:
        if changePin == 13:
            x = 0
            arduino.write(b"0")
            pins[changePin]['state'] = 0
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + "off."
        
    # This data will be sent to index.html (pins dictionary)
    templateData = {
        'pins' : pins
    }
    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData)

# Main function, set up serial bus, indicate port for the webserver, and start the service
if __name__ == "__main__" :
    ser = serial.Serial(device, 115200, timeout=1)
    ser.flush()
    print(arduino.in_waiting)
    monitoring_thread = threading.Thread(target = monitoring_loop)
    monitoring_thread.start()
    app.run(host='0.0.0.0', port = 8080, debug = True)