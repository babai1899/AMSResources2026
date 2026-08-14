from socketio_instance import socketio


@socketio.on(

    "connect",

    namespace="/notifications"

)

def notification_connect():

    print("Notification Connected")


@socketio.on(

    "disconnect",

    namespace="/notifications"

)

def notification_disconnect():

    print("Notification Disconnected")