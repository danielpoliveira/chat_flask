from flask import session,request
from flask_socketio import emit, join_room, leave_room,SocketIO
from .. import socketio

messages = { "room": [] }
clients = []

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')

    clients.append(request.namespace)
    data = []

    exist = False
    for item in messages['room']:      
      if str(room) in item:
        data = item[str(room)]
        exist = True
        break

    if not exist:
      messages["room"].append({ str(room) : []})

    print(messages['room'])
    join_room(room)

    emit('previousMessage', data, room=clients[0])
    emit('status', {'msg': session.get('name') + ' Entrou na sala.'}, room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')

    data = []

    for item in messages['room']:
      if str(room) in item:
        item[str(room)].append({ 'name': session.get('name'),'msg': message['msg']})
        break
    
    data.append({ 
      'name': session.get('name'),
      'msg': message['msg'],
    })

    print(messages)
    
    #emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)
    emit('message', {
        'name': session.get('name'),
        'msg':  message['msg'],
    }, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    clients.remove(request.namespace)
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

