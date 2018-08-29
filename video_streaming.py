from flask import Flask, render_template, Response, request
from flask_cors import CORS
import DBconnect as DB
import DBresponse as Resp
from yolo import detect_image
import os
import json

translateEtoK = { 'person':'사람', 'bicycle':'자전거', 'car':'자동차', 'motorbike':'오토바이', 'aeroplane':'비행기', 'bus':'버스', 'train':'전철', 'truck':'트럭', 'boat':'보트', 'traffic light':'신호등', 'fire hydrant':'소화전', 'stop sign':'정지 표지판', 'parking meter':'계량기', 'bench':'벤치', 'bird':'새', 'cat':'고양이', 'dog':'개', 'horse':'말', 'sheep':'양', 'cow':'소', 'elephant':'코끼리', 'bear':'곰', 'zebra':'얼룩말', 'giraffe':'기린', 'backpack':'가방', 'umbrella':'우산', 'handbag':'핸드백', 'tie':'넥타이', 'suitcase':'서류가방', 'frisbee':'원반', 'skis':'스키', 'snowboard':'스노우보드', 'sports ball':'공', 'kite':'연', 'baseball bat':'방망이', 'baseball glove':'장갑', 'skateboard':'스케이트보드', 'surfboard':'서핑보드', 'tennis racket':'테니스라켓', 'bottle':'유리병', 'wine glass':'유리컵', 'cup':'컵', 'fork':'포크', 'knife':'나이프', 'spoon':'숟가락', 'bowl':'그릇', 'banana':'바나나', 'apple':'사과', 'sandwich':'샌드위치', 'orange':'오렌지', 'broccoli':'브로콜리', 'carrot':'당근', 'hot dog':'핫도그', 'pizza':'피자', 'donut':'도넛', 'cake':'케이크', 'chair':'의자', 'sofa':'소파', 'pottedplant':'화분', 'bed':'침대', 'diningtable':'식탁', 'toilet':'화장실', 'tvmonitor':'모니터', 'laptop':'노트북', 'mouse':'마우스', 'remote':'리모컨', 'keyboard':'키보드', 'cell phone':'핸드폰', 'microwave':'전자렌지', 'oven':'오븐', 'toaster':'토스터기', 'sink':'싱크대', 'refrigerator':'냉장고', 'book':'책', 'clock':'시계', 'vase':'병', 'scissors':'가위', 'teddy bear':'곰인형', 'hair drier':'헤어드라이어', 'toothbrush':'칫솔' }

db = DB.DBconnect()
resp = Resp.DBresponse()
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#cors = CORS(app, resources={r"/*": {"origins": "http://121.129.2.195:8080"}})
CORS(app)

video_content = ""

def get_frame(filename):
    try:
         print('get_frame : 안')
         file = request.files['abc']
         print('get_frame : request 지나감')
         file.save('/home/ubuntu/IOT_WEB_SERVER/static/' + filename)
         print('get_frame : save 지나감')
    except IOError:
         print("get_frame : 파일 저장 에러")
    return file

#while 없이 테스트
""" 
    while True:
        try:
            file = request.files[request_code]
            file.save('/home/ubuntu/' + filename)
            yield(file)
            if is_it_stream == False:
                break
        except IOError:
            print("파일 저장 에러")
            break
"""


def video_gen(filename):
    try:
        while True:
            print('video_gen : 안')
            file = request.files['abc']
            print('video_gen : request 지나감')
            file.save('/home/ubuntu/IOT_WEB_SERVER/static/' + filename)
            with open('/home/ubuntu/IOT_WEB_SERVER/static/'+filename, 'rb') as frame: 
                pass
                #yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except IOError:
        print("파일 저장 에러")

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

# ==================Homepage Route======================

@app.route('/photos')
def photos():
    photoList = db.selectPhoto()
    print(photoList)
    return resp.photoResponse(200, photoList)
    

@app.route('/messages')
def messages():
    messageList = db.selectMessage()
    print(messageList)
    return resp.messageResponse(200, messageList)

# =================VIDEOSTREAM TEST=====================
@app.route('/videostream', methods=["POST"]) # 아틱-> 서버 : 비디오스트리밍
def videostream():
    print('videostrem : 안')
    return Response(video_gen('video.jpg'), status=200, mimetype='text/plain')

@app.route('/videostreaming', methods=["GET"]) # 서버 -> 웹 : 비디오스트리밍
def videostreaming():
    return Response(video, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video') # 보호자 -> 웹 : 비디오스트리밍  조회
def video():
    return render_template('video.html')

@app.route('/location') # 보호자 -> 웹 : gps 조회
def location():
    return render_template('map.html')

@app.route('/path') # 보호자 -> 웹 : 길찾기 경로 조회
def path():
    return render_template('path.html')

@app.route('/image', methods=["POST"]) # 아틱 -> 서버 -> 아틱 : 사진 yolo 수행
def test():
    get_frame('yolo.jpg')
    result = detect_image('/home/ubuntu/IOT_WEB_SERVER/static/yolo.jpg')
    if result is not '':
        str_result = ''
        for i in result:
            str_result=str_result + translateEtoK.get(i['class'], '') + ' '
        str_result = str_result + '있습니다'
        print(str_result)
    else:
        str_result = '인식된 주요 물체가 없습니다'
    return Response(str_result,status=200, mimetype='text/plain')

@app.route('/gps') # 안드로이드 -> 서버 : gps 저장
def receive_gps():
    lat = request.args.get('latitude', '')
    lon = request.args.get('longitude', '')
    gps = {"latitude":lat, "longitude": lon}
    f = open('/home/ubuntu/gps.txt','w+')
    f.write(''.join(json.dumps(gps)))
    f.close
    print(lat+ ' ' + lon)
    return Response(json.dumps({'lat':lat, 'lon':lon}), status=200)

@app.route('/gpsartik') # 서버 -> 아틱 : gps 전송
def send_gps():
    try:
        f = open('/home/ubuntu/gps.txt','r')
        gps = f.readlines()
        f.close()
    except IOError:
	#gps 파일 오픈에 실패할 경우 광화문 좌표를 줌
        gps = '{"longitude": "126.976799", "latitude": "37.574071"}'
    finally:
        print(gps)
        return Response(gps, status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
