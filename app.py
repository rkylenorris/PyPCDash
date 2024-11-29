from flask import Flask, render_template, request, jsonify
import psutil
import os
import GPUtil
from pycaw.pycaw import AudioUtilities
import pythoncom

app = Flask(__name__)


@app.route("/get_volumes", methods=["GET"])
def get_volumes():
    process_volumes = get_audio_sessions()  # Use the function to gather process and volume info
    return jsonify(process_volumes)


def get_audio_sessions():
    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    process_volumes = []
    for session in sessions:
        if session.Process:
            if session.Process.name().lower() in session.Process.name().lower():
                interface = session.SimpleAudioVolume
                process_volumes.append({"process": session.Process.name().lower(), "volume": round(interface.GetMasterVolume() * 100)})

    return process_volumes


@app.route('/')
def dashboard():
    volumes = get_audio_sessions()
    return render_template('dashboard.html', process_volumes=volumes)


@app.route('/action', methods=['POST'])
def action():
    action_type = request.form['action']
    if action_type == 'open_browser':
        os.system('start chrome')  # Adjust for your OS
    return "Action executed"


@app.route('/stats', methods=['GET'])
def stats():
    gpus = GPUtil.getGPUs()

    pc_stats = {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'GPU': 0 if len(gpus) == 0 else round(gpus[0].load * 100, 2)
    }
    return jsonify(pc_stats)


@app.route("/update_volume", methods=["POST"])
def update_volume():
    data = request.json
    process_name = data["process"]
    volume_level = float(data["volume"]) / 100

    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()

    for session in sessions:
        if session.Process:
            if session.Process.name().lower() == process_name.lower():
                volume = session.SimpleAudioVolume
                volume.SetMasterVolume(volume_level, None)

    return jsonify({"status": "success", "process": process_name, "volume": volume_level * 100})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
