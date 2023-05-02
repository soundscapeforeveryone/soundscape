from flask import Flask, make_response
from utils import soundscape_tile, check_number
import json

app = Flask(__name__)

@app.route('/<zoom>/<x>/<y>')
def get_soundscape_tile(zoom, x, y):
    if zoom and x and y:
        zoom = int(zoom) if check_number(zoom) else ''
        x = int(x) if check_number(x) else ''
        y = int(y) if check_number(y) else ''
        if zoom and x and y:
            data = soundscape_tile(zoom=zoom, x=x, y=y)
            return make_response(json.loads(data), 200)
        return make_response(dict(message='Bad request !'), 400)
    if not zoom and x and y:
        return make_response(dict(message='Parameter << zoom >> is missing'), 500)
    if not x and zoom and y:
        return make_response(dict(message='Parameter << x >> is missing'), 500)
    if not y and x and zoom:
        return make_response(dict(message='Parameter << y >> is missing'), 500)
    return make_response(dict(message='Failed to load data'), 500)
    #return make_response(dict(message='Database is not accessible at the moment!'), 503)


if __name__=='__main__':
    app.run(debug=True)