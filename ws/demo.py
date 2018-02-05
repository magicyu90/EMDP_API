from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

async_mode = None
socketio = SocketIO(app)
thread = None
thread_lock = Lock()


# @socketio.on('client_event', namespace='/devicestat')
# def client_msg(msg):
#     cmd = msg['cmd']
#     if cmd == 101:
#         emit('server_response', {'cmd': cmd, 'data': 'this is the test data'})

def query_device_running_stat():
    while True:
        socketio.sleep(5)
        print('query device running stat')
        socketio.emit('server_response', {'data': 'This is the server data by Hugo'}, namespace='/devicestat')


@socketio.on('connect', namespace='/devicestat')
def connect():
    print('connected')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=query_device_running_stat)


@socketio.on('connect_event', namespace='/devicestat')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})


@socketio.on('disconnect', namespace='/devicestat')
def shutdown():
    print('disconnect...')
    disconnect()


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=6001)
