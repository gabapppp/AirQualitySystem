from flask import Flask, render_template, Response, request
import json
from bson import ObjectId
import redis
from flask_socketio import SocketIO
from threading import Lock
from pymongo.mongo_client import MongoClient
from datetime import datetime, timedelta
"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZUCGiYmt_H3~ZGJ'
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config['MAIL_USERNAME'] = ""
app.config['MAIL_PASSWORD'] = ""
socketio = SocketIO(app, cors_allowed_origins='*')

# Initialize DB
uri = "mongodb+srv://gabap:FmJPMHijB74BsuZ6@cluster0.widcuv7.mongodb.net/?retryWrites=true&w=majority"
try:
    client = MongoClient(uri)
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.database
sensordata = db.sensordata
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def io_background_thread():
    while True:
        try:
            dustLevel = redis_db.get("pm25")
            CO2_ppm =redis_db.get("mq7")       
            CO_ppm = redis_db.get("mq135") 
            temperature = redis_db.get("temperature")
            humidity = redis_db.get("humidity")
        except:
            return
        socketio.emit('updateSensorData', {
            "pm25": float(dustLevel),
            "mq7": float(CO2_ppm),
            "mq135": float(CO_ppm),
            "temperature": float(temperature),
            "humidity": float(humidity),
            });
        socketio.sleep(8)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)     

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chart")
def get_chart():
    data = sensordata.find({})
    return Response(data)

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
            thread = socketio.start_background_task(io_background_thread)
            

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app)
    app.run(debug=True)