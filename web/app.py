from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
from redis import Redis

redis = Redis(host='localhost', port=6379, decode_responses=True)
"""
Background Thread
"""
thread = None
thread_lock = Lock()


dummy_sensor_value = 0
co_sensor_value = 0
temp_sensor_value = 0
humi_sensor_value = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZUCGiYmt_H3~ZGJ'
socketio = SocketIO(app, cors_allowed_origins='*')


"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""

def background_thread():
    print("Generating random sensor values")
    while True:
        dummy_sensor_value = round(random() * 100, 3)
        co_sensor_value = round(random() * 100, 3)
        temp_sensor_value = round(random() * 100, 3)
        humi_sensor_value = round(random() * 100, 3)
        print(humi_sensor_value, temp_sensor_value, co_sensor_value, dummy_sensor_value)
        #socketio.emit('updateSensorData', {'pm25': dummy_sensor_value,'co': co_sensor_value,
        #'temp': temp_sensor_value,'humi': humi_sensor_value, "date": get_current_datetime()
        #})
        socketio.emit('updateSensorData', {"value": dummy_sensor_value, "date": get_current_datetime()})
        socketio.sleep(1)

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/mq135")
def get_mq135_list():
    
    return Response({"None: None"})

@app.route("/pm25")
def get_pm25_list():
    return Response({})


"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)