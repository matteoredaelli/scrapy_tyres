from flask import Flask
from flask import request, render_template

app = Flask(__name__)

import tyre_utils
import utils
import json

VERSION=0.1


@app.route('/a')
def root():
    return render_template('index.html')

@app.route('/version')
def version():
    return 'Tyre info extractor version %s' % VERSION

@app.route('/extractor')
def extract_info():
    description = request.args.get('description', '')

    result = {}
    if description is not None:
        item = {"description": utils.clean_text(description.upper())}
        result = tyre_utils.mergeItems(item, tyre_utils.extractAll(item))
    return json.dumps(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
