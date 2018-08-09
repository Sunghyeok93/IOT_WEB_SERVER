from flask import Flask, render_template, Response, request
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#cors = CORS(app, resources={r"/*": {"origins": "http://121.129.2.195:8080"}})
CORS(app)

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/')
def index():
    #json = request.form
    #print(json['data'])
    return render_template('index.html')

@app.route('/location')
def location():
    return render_template('map.html')


@app.route('/path')
def path():
    return render_template('path.html')

@app.route('/test', methods=["POST"])
def test():
    print(request.data)
    json = request.form
    file = request.files['abc']
    filename = file.filename
    file.save('/Users/sunghyeok/video_streaming/static/pic.jpg')
    print(json)
    print(file)
    #print(json)
    data = {
        'status': 200
    }
    #js = json.dumps(data)
    return Response(status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
