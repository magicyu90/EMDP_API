import time
import redis
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import Flask, render_template, session, request, copy_current_request_context, current_app
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room, rooms
from threading import Lock

r = redis.StrictRedis(host='localhost', port=6379, charset="utf-8", decode_responses=True)  # Redis连接器
mongo_client = MongoClient('mongodb://localhost:27017')  # mongo连接器
db = mongo_client['SITS']

app = Flask(__name__)

async_mode = None
socketio = SocketIO(app)
thread = None
thread_lock = Lock()
whole_room = {
    "ctlight": {

    }
}
# room['ctlight'] = dict()
ct_thread = None

def query_device_ct_light_data():
    while True:
        socketio.sleep(5)
        for eqp_id in whole_room['ctlight']:
            if r.hexists(eqp_id, 'ctlight'):
                result = r.hget(eqp_id, 'ctlight')
            else:
                compare_date = datetime.utcnow() - timedelta( minutes=1)
                pipeline = [
                    {"$match": {"clock": {"$gt": compare_date}}},
                    {"$group": {"_id": "$name", "value": {"$push": {"clock": "$clock", "value": "$value"}}}},
                    {"$project": {"_id": 0, "type": "$_id", "value": 1}}
                ]
                res = list(db.ctlight.aggregate(pipeline))
                result = {}
                for item in res:
                    new_list = []
                    for v in item['value']:
                        new_list.append({
                            'clock': v['clock'].strftime('%Y-%m-%d %H:%M:%S'),
                            'value': v['value']
                        })
                    result[item['type']] = new_list
                r.hset(eqp_id, 'ctlight', result)

            result_str = json.dumps(result)
            socketio.emit('ctlight_data', {'data': result_str},
                          namespace='/ctlight', room=eqp_id)


def query_device_running_stat():
    while True:
        socketio.sleep(5)
        if r.exists('DEVICE_EVENT_STAT'):
            device_event_stat_str = json.dumps(r.hgetall('DEVICE_EVENT_STAT'))
            # 发送设备报警信息
            socketio.emit('device_running_stat', {'data': device_event_stat_str}, namespace='/devicestat')
        if r.exists('DEVICE_STAT'):
            # 发送设备运行状态
            device_stat_values = list(r.hgetall('DEVICE_STAT').values())
            normal_status_count = device_stat_values.count('1')
            error_status_count = device_stat_values.count('2')
            device_stat_dict = {'normal': normal_status_count, 'error': error_status_count}
            device_stat_str = json.dumps(device_stat_dict)
            socketio.emit('device_stat', {'data': device_stat_str}, namespace='/devicestat')


@socketio.on('connect', namespace='/devicestat')
def connect():
    print('%s connected in devicestat' % request.sid)
    global thread
    with thread_lock:
        if thread is None:
            print('thread is none')
            thread = socketio.start_background_task(target=query_device_running_stat)
    emit('server_response', {'data': None, 'msg': 'client %s is connected' % request.sid})


@socketio.on('connect_event', namespace='/devicestat')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})


@socketio.on('disconnect', namespace='/devicestat')
def shutdown():
    print('devicestat disconnect...')
    disconnect()


@socketio.on('connect_event', namespace='/ctlight')
def ct_ligth_connected_msg(msg):
    emit('server_response', {'data': msg['data']})


@socketio.on('disconnect', namespace='/ctlight')
def ctlightshutdown():
    print('ctlight data disconnect...')
    for key in whole_room['ctlight'].keys():
        if request.sid in whole_room['ctlight'][key]:
            whole_room['ctlight'][key].remove(request.sid)
            if len(whole_room['ctlight'][key]) == 0:
                whole_room['ctlight'].pop(key, None)
            break
    for room in rooms(namespace='/ctlight'):
        leave_room(room, namespace='/ctlight')
    disconnect()
    print(whole_room['ctlight'])


@socketio.on('connect', namespace='/ctlight')
def ctlightconnect():
    print('%s connected in ctlight' % request.sid)
    eqp_id = request.args.get('eqp_id')
    join_room(eqp_id, namespace='/ctlight')
    if eqp_id is None:
        print('eqp_id is missing,disconnect...')
        disconnect()

    if eqp_id not in whole_room['ctlight'].keys():
        whole_room['ctlight'][eqp_id] = []
        whole_room['ctlight'][eqp_id].append(request.sid)
    else:
        whole_room['ctlight'][eqp_id].append(request.sid)

    print(whole_room['ctlight'])
    with thread_lock:
        global ct_thread
        if ct_thread is None:
            ct_thread = socketio.start_background_task(target=query_device_ct_light_data)
    emit('server_response', {'data': None, 'msg': 'client %s is connected' % request.sid})


if __name__ == '__main__':
    socketio.run(app, debug=True, port=6001)
