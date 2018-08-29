from flask import json, Response

class DBresponse():

    def statusResponse(self, responseStatus):
        data = {
            'status' : responseStatus
        }
        js = json.dumps(data)
        resp = Response(js, status=responseStatus, mimetype='application/json')
        return resp

    def photoResponse(self, responseStatus, photoRow):
        photoList = []
        data = {
            'status': responseStatus
        }
        for photo in photoRow:
            val = {'num':photo[0], 'time':photo[1], 'size': photo[3]}
            photoList.append(val)

        data['list'] = photoList
        js = json.dumps(data)
        resp = Response(js, status=responseStatus, mimetype='application/json')
        return resp

    def messageResponse(self, responseStatus, messageRow):
        messageList = []
        data = {
            'status' : responseStatus
        }
        for message in messageRow :
            val = {'num':message[0], 'time':message[1], 'content':message[2], 'sender':message[3]}
            messageList.append(val)
        
        data['list'] = messageList
        js = json.dumps(data)
        resp = Response(js, status=responseStatus, mimetype='application/json')
        return resp
