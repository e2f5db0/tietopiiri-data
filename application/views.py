from flask.json import jsonify
from application import app

@app.route("/")
def index():
    return jsonify({'tietopiiri-data': 'running'})
