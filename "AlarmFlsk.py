from flask import Flask, render_template, request, redirect, url_for
import threading
import time
import os

app = Flask(__name__)

# Variable to hold the alarm time
alarm_time = None

def play_alarm():
    # Function to play the alarm sound
    os.system("start your-music-file.mp3")  # Replace "your-music-file.mp3" with your actual file path

def set_alarm(hour, minute, ampm):
    global alarm_time

    # Convert hour to 24-hour format
    if ampm == "PM":
        hour = (hour + 12) % 24

    # Set the alarm time
    alarm_time = hour * 3600 + minute * 60

    # Calculate the time until the alarm
    current_time = time.localtime(time.time())
    current_seconds = current_time.tm_hour * 3600 + current_time.tm_min * 60 + current_time.tm_sec
    time_diff = alarm_time - current_seconds

    # Start a new thread to play the alarm sound when the time comes
    if time_diff > 0:
        threading.Timer(time_diff, play_alarm).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_alarm', methods=['POST'])
def set_alarm_route():
    hour = int(request.form['hour'])
    minute = int(request.form['minute'])
    ampm = request.form['ampm']

    set_alarm(hour, minute, ampm)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
