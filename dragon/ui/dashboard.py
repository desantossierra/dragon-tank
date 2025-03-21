import logging
import time

from flask import Flask, render_template, request, jsonify
import requests

from dragon.conf import SIMULATION_SLEEP_S

app = Flask(__name__)
# Disable Werkzeug logging
log = logging.getLogger('werkzeug')
log.disabled = True

shared_data = {'x': 0, 'y': 0, 'angle': 0, 'sonar_distance': 0}

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html', data=shared_data)

@app.route('/update', methods=['POST'])
def update():
    """Endpoint para actualizar la posición del robot."""
    data = request.json
    shared_data.update(data)
    return jsonify(shared_data)

def update_dashboard(location):
    while True:
        data = {'x': location[0],
                'y': location[1],
                'angle': location[2],
                'sonar_distance': location[3]}
        # it updates the shared_data via API
        try:
            requests.post('http://127.0.0.1:5000/update', json=data)
        except Exception as e:
            pass

        time.sleep(SIMULATION_SLEEP_S)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)