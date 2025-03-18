from flask import Flask, render_template, request, jsonify
import requests

import multiprocessing

app = Flask(__name__)
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

def update_dashboard(new_data):
    # it updates the shared_data via API
    try:
        requests.post('http://127.0.0.1:5000/update', json=new_data)
    except:
        pass


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)