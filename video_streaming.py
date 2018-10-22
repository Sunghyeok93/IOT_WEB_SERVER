from flask import Flask, render_template, Response, request
from flask_cors import CORS
import DBconnect as DB
import DBresponse as Resp
from yolo import detect_image
import camera
from camera import Camera
import time
from time import gmtime, strftime, localtime
import json
import datetime
import os
import shutil
from collections import Counter

translateEtoK = { 'blue':'심장약', 'red':'수면제', 'person':'사람', 'bicycle':'자전거', 'car':'자동차', 'motorbike':'오토바이', 'aeroplane':'비행기', 'bus':'버스', 'train':'전철', 'truck':'트럭', 'boat':'보트', 'traffic light':'신호등', 'fire hydrant':'소화전', 'stop sign':'정지 표지판', 'parking meter':'계량기', 'bench':'벤치', 'bird':'새', 'cat':'고양이', 'dog':'개', 'horse':'말', 'sheep':'양', 'cow':'소', 'elephant':'코끼리', 'bear':'곰', 'zebra':'얼룩말', 'giraffe':'기린', 'backpack':'가방', 'umbrella':'우산', 'handbag':'핸드백', 'tie':'넥타이', 'suitcase':'서류가방', 'frisbee':'원반', 'skis':'스키', 'snowboard':'스노우보드', 'sports ball':'공', 'kite':'연', 'baseball bat':'방망이', 'baseball glove':'장갑', 'skateboard':'스케이트보드', 'surfboard':'서핑보드', 'tennis racket':'테니스라켓', 'bottle':'유리병', 'wine glass':'유리컵', 'cup':'컵', 'fork':'포크', 'knife':'나이프', 'spoon':'숟가락', 'bowl':'그릇', 'banana':'바나나', 'apple':'사과', 'sandwich':'샌드위치', 'orange':'오렌지', 'broccoli':'브로콜리', 'carrot':'당근', 'hot dog':'핫도그', 'pizza':'피자', 'donut':'도넛', 'cake':'케이크', 'chair':'의자', 'sofa':'소파', 'pottedplant':'화분', 'bed':'침대', 'diningtable':'식탁', 'toilet':'화장실', 'tvmonitor':'모니터', 'laptop':'노트북', 'mouse':'마우스', 'remote':'리모컨', 'keyboard':'키보드', 'cell phone':'핸드폰', 'microwave':'전자렌지', 'oven':'오븐', 'toaster':'토스터기', 'sink':'싱크대', 'refrigerator':'냉장고', 'book':'책', 'clock':'시계', 'vase':'병', 'scissors':'가위', 'teddy bear':'곰인형', 'hair drier':'헤어드라이어', 'toothbrush':'칫솔' }

db = DB.DBconnect()
resp = Resp.DBresponse()
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
cors = CORS(app, supports_credentials=False)
app.config['CORS_HEADERS'] = 'Content-Type'
imagePath = '/home/ubuntu/IOT_WEB_SERVER/static/'

def get_current_time():
    utcnow = datetime.datetime.utcnow()
    time_gap = datetime.timedelta(hours=9)
    kor_time = str(utcnow + time_gap) # Kor_time -> %Y-%m-%d %H:%M:%S.%f
    yearMonthDay = kor_time.split(' ')[0]
    extra = kor_time.split(' ')[1]
    extra = extra.split('.')[0]
    hour = extra.split(':')[0]
    minute = extra.split(':')[1]
    second = extra.split(':')[2]
    
    return yearMonthDay + "-" + hour + minute + second #180901-010101 형태로 전달
 
def removeDuplicates(string):
    string = string.split(" ")
    for i in range(0, len(string)):
        string[i] = "".join(string[i])
        
    UniqW = Counter(string)

    s = " ".join(UniqW.keys())
    return s

def get_frame(imageName, isDB, isPhotobook=0):

    def get_img_name(img_name):
        if not isinstance(img_name, str):
            raise TypeError('이미지 타입은 스트링')
        if '.' not in img_name:
            return img_name + '.jpg'
        if img_name.split('.')[1] not in ['jpg', 'png', 'jpeg']:
            raise ValueError('이미지 확장자가 이상해')
        return img_name

    def get_time_from_name(img_name):
        if '/' not in img_name:
            return img_name
        else:
            return img_name.split('/')[1]

    try:
        imageTime = get_time_from_name(imageName)
        imageName = get_img_name(imageName)
        filePath = os.path.join(imagePath, imageName)
        file = request.files['abc']
        file.save(filePath)
        if isDB is True:
	    if isStreaming != 0:
                db.insertImage(imageTime, filePath, str(os.path.getsize(filePath)))
            else:
                db.insertPhotobook(imageTime, filePath, str(os.path.getsize(filePath)))
    except IOError:
        print("get_frame : 파일 저장 에러")
    return 200


def video_gen(cam):
    while True:
       # print("video_gen")
        frame = cam.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# No caching at all for API endpoints.


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# ==================Homepage Route======================


@app.route('/photos')
def photos():
    photoList = db.selectPhoto()
    return resp.photoResponse(200, photoList)
    

@app.route('/messages')
def messages():
    messageList = db.selectMessage()
    return resp.messageResponse(200, messageList)

# =================VIDEOSTREAM TEST=====================
@app.route('/videostream', methods=["POST"])  # 아틱-> 서버 : 비디오스트리밍
def videostream():
    return Response(status=get_frame("extra/" + get_current_time(), True), mimetype='text/plain')


@app.route('/videostream', methods=["GET"])  # 서버 -> 웹 : 비디오스트리밍
def gen_video():
    cam = Camera()
    return Response(video_gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')  # 보호자 -> 웹 : 비디오스트리밍  조회
def video():
    return render_template('old_video.html')

@app.route('/path')  # 보호자 -> 웹 : 길찾기 경로 조회
def path():
    return render_template('path.html')

@app.route('/voicemail', methods=["POST"]) # * -> 서버 : 음성입력
def send_mail():
    form_data = request.form
    sender = form_data['sender']
    content = form_data['content']
    isRead = 0
    print(sender)
    if sender !=  'Homepage':
        print("####not arrived")
        isRead = 1
    db.insertMessage(get_current_time(), content, sender, isRead)
    #db.insertMessage(strftime("%Y-%m-%d-%H:%M:%S", gmtime()), content, sender, isRead)
    return Response('200', status=200, mimetype='text/plain')

@app.route('/voicemail') # 서버 -> 아틱 : 음성받음
def get_mail():
    print("도착")
    message_not_read = db.getMessageNotRead()
    if len(message_not_read) is 0:
        return Response("읽지 않은 메시지가 없습니다.", status=200, mimetype='text/plain')
    message = str(len(message_not_read)) + "개의, 메시지가 남았습니다." + "한개의, 메시지를 읽겠습니다." + str(db.getMessageContent(message_not_read[0][0])[0])
    print(message)
    db.modifyMessageIsRead(message_not_read[0][0], 1)
    return Response(message, status=200, mimetype='text/plain')

@app.route('/image', methods=["POST"])  # 아틱 -> 서버 -> 아틱 : 사진 yolo 수행
def image():
    get_frame('extra/yolo.jpg', False)
    result = detect_image('/home/ubuntu/IOT_WEB_SERVER/static/extra/yolo.jpg')
    if not result:
        str_result = '인식된 주요 물체가 없습니다'
    else:
        print("result" + str(result))
        str_result = ''
        for i in result:
            str_result = str_result + translateEtoK.get(i['class'], '') + ' '
        print(str_result)
        str_result = removeDuplicates(str_result)
        str_result = str_result + '있습니다'
        print(str_result)

    return Response(str_result, status=200, mimetype='text/plain')


@app.route('/gps')  # 안드로이드 -> 서버 : gps 저장
def receive_gps():
    lat = request.args.get('latitude', '')
    lon = request.args.get('longitude', '')
    gps = {"latitude":lat, "longitude": lon}
    print(gps)
    print('########')
    f = open('/home/ubuntu/gps.txt', 'w+')
    f.write(''.join(json.dumps(gps)))
    f.close
    print(lat + ' ' + lon)
    return Response(json.dumps({'lat':lat, 'lon':lon}), status=200)

@app.route('/gpsartik')  # 서버 -> 아틱 : gps 전송
def send_gps():
    try:
        f = open('/home/ubuntu/gps.txt', 'r')
        gps = f.readlines()
        f.close()
    except IOError:
	# gps 파일 오픈에 실패할 경우 광화문 좌표를 줌
        print('error!!!! gps.txt can not read')
        gps = '{"longitude": "126.976799", "latitude": "37.574071"}'
    finally:
        print(gps)
        return Response(gps, status=200)
    

@app.route( '/' )
def hello():
    return render_template( '시작화면.html' )

@app.route( '/jiah' )
def jiah():
    return render_template( '시작화면.html' )

#게시판 목록
@app.route( '/Board_List' )
def list():
    return render_template( './게시판 목록.html' )

@app.route( '/Board_View' )
def view():
    return render_template( './게시판 내용.html' )


@app.route( '/Board_Write' )
def write():
    return render_template( './글쓰기.html' )

@app.route('/streaming')
def index():
    return render_template('스트리밍2.html')

@app.route('/map')
def location():
    return render_template('지도.html')

@app.route('/gallery')
def gallery():
    return render_template('갤러리.html')

@app.route('/gallery_list')
def gallery_list():
    return render_template('갤러리 목록.html')

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

@app.route('/photobook', methods=["POST"])
def get_photo():
    return Response(status=get_frame("photo/" + get_current_time(), True,1), mimetype='text/plain')

@app.route('/search', methods=["POST"]) # * -> 서버 : table, content에 맞는 결과 검색
def search():
    form_data = request.form
    table = form_data['table']
    content = form_data['content']
    resultList = db.search_content(table, content)
    if table == 'Message':
        return resp.messageResponse(200, resultList)
    else:
        return resp.photoResponse(200, resultList)

@app.route('/findobject', methods=["GET"]) # 아틱 -> 서버 : 찾으려는 물체의 이름 전달
def getObjectName():
    form_data = request.form
    object_name = form_data['object']
    f = open('/home/ubuntu/object_find.txt', 'w+')
    f.write(object_name)
    f.close
    return Response(object_name, status=200)

@app.route('/findobject', methods=["POST"]) # 아틱 -> 서버 -> 아틱 : 물체를 찾을 경우 완성된 문장을 전달, 못찾을 경우 "0" 전달
def findObject():
    f = open('/home/ubuntu/object_find.txt', 'r')
    object_name = f.readlines()
    print('object_name[0]: ' + object_name[0])
    f.close()

    get_frame('extra/yolo.jpg', False)
    result = detect_image('/home/ubuntu/IOT_WEB_SERVER/static/extra/yolo.jpg')
    print("result : " + str(result))
    str_result = ''
    for i in result:
        str_result = str_result + translateEtoK.get(i['class'], '') + ' '
        print(str_result)
    if object_name[0] in str_result:
        print("물건을 찾은 경우입니다 ###########")
        str_result = "전방에 " + str(object_name[0]) + " 찾았습니다"
    else:
        print("물건을 찾지 못한 경우입니다 ################")
        print(str(object_name[0]) + " " + str_result)
        str_result = "0"   # 찾는 물품이 없을경우 0을 전달함으로써 아틱이 식별할 수 있게끔 해줌

    return Response(str_result, status=200, mimetype='text/plain')


if __name__ == '__main__':
    print('start')
    db.delete_extra_img()
    filePath = "/home/ubuntu/pyyolo/darknet/data/dog.jpg"
    #db.insertImage("2018-01-01-000000", filePath, str(os.path.getsize(filePath)))
    try:
        shutil.rmtree("/home/ubuntu/IOT_WEB_SERVER/static/extra")
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    os.mkdir("/home/ubuntu/IOT_WEB_SERVER/static/extra")
    app.run(host='0.0.0.0', debug=True)
