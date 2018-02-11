import time
import redis
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import Flask, render_template, session, request, copy_current_request_context, current_app
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room, rooms
from threading import Lock
from util.redishelper import redis_decode,redis_types

r = redis.StrictRedis(host='localhost', port=6379, charset="utf-8", decode_responses=True)  # Redis连接器
mongo_client = MongoClient('mongodb://localhost:27017')  # mongo连接器
db = mongo_client['SITS']

app = Flask(__name__)

async_mode = None
socketio = SocketIO(app)
thread = None
thread_lock = Lock()
whole_room = {
    "CT_LIGHT_MACHINE": {

    }
}
# room['ctlight'] = dict()
ct_thread = None

########################### DEVICE_STAT ###########################


def query_device_running_stat():
    while True:
        socketio.sleep(5)
        if r.exists('DEVICE_EVENT_STAT'):
            device_event_stat_in_python = redis_decode(redis_types['DEVICE_EVENT_STAT'], r.hgetall('DEVICE_EVENT_STAT'))
            print(device_event_stat_in_python)
            # 发送设备报警信息
            socketio.emit('device_running_stat', {'data': device_event_stat_in_python}, namespace='/DEVICESTAT')
        # TODO查询设备报警信息mongo中
        if r.exists('DEVICE_STAT'):
            # 发送设备运行状态
            device_stat_values = list(r.hgetall('DEVICE_STAT').values())
            normal_status_count = device_stat_values.count('1')
            error_status_count = device_stat_values.count('2')
            device_stat_dict = {'normal': normal_status_count, 'error': error_status_count}
            #device_stat_str = json.dumps(device_stat_dict)
            socketio.emit('device_stat', {'data': device_stat_dict}, namespace='/DEVICESTAT')
        # TODO查询设备运行状态在mongo中


@socketio.on('connect', namespace='/DEVICESTAT')
def connect():
    print('%s connected in DEVICESTAT' % request.sid)
    global thread
    with thread_lock:
        if thread is None:
            print('thread is none')
            thread = socketio.start_background_task(target=query_device_running_stat)
    emit('server_response', {'data': None, 'msg': 'client %s is connected' % request.sid, 'result': 100})


@socketio.on('connect_event', namespace='/DEVICESTAT')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})


@socketio.on('disconnect', namespace='/DEVICESTAT')
def shutdown():
    print('DEVICESTAT with sid:%s disconnect...' % request.sid)
    disconnect()

########################### CT_LIGHT_MACHINE ###########################


def query_device_ct_light_data():
    while True:
        socketio.sleep(5)
        for eqp_id in whole_room['CT_LIGHT_MACHINE']:
            if r.hexists(eqp_id, 'CT_LIGHT_MACHINE'):
                result = r.hget(eqp_id, 'CT_LIGHT_MACHINE')
                result_str = json.dumps(result)
            else:
                compare_date = datetime.utcnow() - timedelta(minutes=1)
                pipeline = [
                    {"$sort": {"clock": 1}},
                    {"$match": {"clock": {"$gt": compare_date}}},
                    {"$group": {"_id": "$name", "value": {"$push": {"clock": "$clock", "value": "$value"}}}},
                    {"$project": {"_id": 0, "type": "$_id", "value": 1}}
                ]
                ctlight_res = list(db.ctlight.aggregate(pipeline))
                result = dict()
                for item in ctlight_res:
                    new_list = []
                    for v in item['value']:
                        new_list.append({
                            'clock': v['clock'].strftime('%Y-%m-%d %H:%M:%S.%f'),
                            'value': v['value']
                        })
                    result[item['type']] = new_list
                result_str = json.dumps(result)
                r.hset(eqp_id, 'CT_LIGHT_MACHINE', result_str)

            socketio.emit('ctlight_data', {'data': result_str}, namespace='/CT_LIGHT_MACHINE', room=eqp_id)


@socketio.on('connect_event', namespace='/CT_LIGHT_MACHINE')
def ct_ligth_connected_msg(msg):
    emit('server_response', {'data': msg['data']})


@socketio.on('disconnect', namespace='/CT_LIGHT_MACHINE')
def ctlightshutdown():
    print('CT_LIGHT_MACHINE with sid:%s disconnect...' % request.sid)
    for key in whole_room['CT_LIGHT_MACHINE'].keys():
        if request.sid in whole_room['CT_LIGHT_MACHINE'][key]:
            whole_room['CT_LIGHT_MACHINE'][key].remove(request.sid)
            if len(whole_room['CT_LIGHT_MACHINE'][key]) == 0:
                whole_room['CT_LIGHT_MACHINE'].pop(key, None)
            break
    for room in rooms(namespace='/CT_LIGHT_MACHINE'):
        leave_room(room, namespace='/CT_LIGHT_MACHINE')
    disconnect()
    print(whole_room['CT_LIGHT_MACHINE'])


@socketio.on('connect', namespace='/CT_LIGHT_MACHINE')
def ctlightconnect():
    print('%s connected in ctlight' % request.sid)
    eqp_id = request.args.get('eqp_id')

    if eqp_id is None:
        print('eqp_id is missing,disconnect...')
        disconnect()

    join_room(eqp_id, namespace='/CT_LIGHT_MACHINE')
    if eqp_id not in whole_room['CT_LIGHT_MACHINE'].keys():
        whole_room['CT_LIGHT_MACHINE'][eqp_id] = []
        whole_room['CT_LIGHT_MACHINE'][eqp_id].append(request.sid)
    else:
        whole_room['CT_LIGHT_MACHINE'][eqp_id].append(request.sid)

    print(whole_room['CT_LIGHT_MACHINE'])
    with thread_lock:
        global ct_thread
        if ct_thread is None:
            ct_thread = socketio.start_background_task(target=query_device_ct_light_data)

    emit('server_response', {'data': None, 'msg': 'client %s is connected' % request.sid, 'result': 100})


if __name__ == '__main__':
    socketio.run(app, debug=True, port=6001)
