from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gabap'
socketio = SocketIO(app, cors_allowed_origins='*')
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
        socketio.emit('updateSensorData', {'value': dummy_sensor_value, "date": get_current_datetime()})
        socketio.sleep(1)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mq135")
def get_mq135_data():
    return Response({"None: None"})

@app.route("/pm25")
def get_pm25_data():
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