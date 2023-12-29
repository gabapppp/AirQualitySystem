from flask import Flask, render_template, Response, request, redirect, session, url_for
import json
from bson import ObjectId
import redis
from flask_socketio import SocketIO
from threading import Lock
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from pymongo import MongoClient
from hashlib import sha256
import uuid
from bson.json_util import dumps

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
mail = Mail(app)
# Initialize DB
uri = "mongodb+srv://..."
try:
    client = MongoClient(uri)
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.database
sensordata = db.sensordata
users = db.users
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def io_background_thread():
    while True:
        try:
            dustLevel = redis_db.get("pm25")
            CO2_ppm = redis_db.get("mq7")       
            CO_ppm = redis_db.get("mq135") 
            temperature = redis_db.get("temperature")
            humidity = redis_db.get("humidity")
        except:
            return
        if (dustLevel > 50 or CO_ppm > 100):
            msg = Message('Alert from Air Quality Monitoring', sender =   'peter@mailtrap.io', recipients = ['paul@mailtrap.io'])
            msg.body = "Reduce smoke in your vehicle by closing the windows and vents and running the air conditioner in recirculate mode"
            mail.send(msg)
        if (CO2_ppm > 1000):
            msg = Message('Alert from Air Quality Monitoring', sender =   'peter@mailtrap.io', recipients = ['paul@mailtrap.io'])
            msg.body = "Make sure it is sized for the room and that it does not make ozone, which is a harmful air pollutante"
            mail.send(msg)
        socketio.emit('updateSensorData', {
            "pm25": float(dustLevel),
            "mq7": float(CO2_ppm),
            "mq135": float(CO_ppm),
            "temperature": float(temperature),
            "humidity": float(humidity),
            });
        socketio.sleep(3)

@app.route("/")
def index():
    if 'username' in session:
        seven_days_ago = datetime.utcnow() - timedelta(days=30)
        query = {"time": {"$gte": seven_days_ago}}
        objects_per_day = []
        for i in range(30):
            start_date = seven_days_ago + timedelta(days=i)
            end_date = seven_days_ago + timedelta(days=i+1)

            # Query to get 1 object for each day
            query_per_day = {
                "time": {
                    "$gte": start_date,
                    "$lt": end_date
                }
            }
            object_for_day = sensordata.find_one(query_per_day)
            print(object_for_day)
            if object_for_day:
                objects_per_day.append(object_for_day)

        chartData = dumps(objects_per_day)
        return render_template('index.html', username=session['username'], chartData = chartData)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})
        if user and sha256(password.encode("utf-8")).hexdigest()==user['password']:
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            hashed_password = sha256(password.encode("utf-8")).hexdigest()
            users.insert_one({'_id':uuid.uuid4().hex,'username': username, 'password': hashed_password})
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Passwords do not match')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

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