from datetime import datetime
from flask import session
from flask_socketio import emit

def register_socketio_handlers(sio):
    @sio.on("new_message")
    def on_new_message(data):
        print('sss new_message')
        emit("new_message", data, broadcast=True)

    @sio.on("chat_action")
    def on_chat_action():
        print('sss chat_action')
        sio.emit("chat_action", broadcast=True)

    # @socketio.on("message")
    # def handle_websocket_message(data):
    #     timestamp = datetime.now()
    #     chat_id = session.get("chat_id")
    #     user_id = session.get("user_id")
    #     payload = {
    #         "chat_id": chat_id,
    #         "message": data,
    #         "timestamp": timestamp,
    #         "user_id": user_id
    #     }
    #     emit("new_message", payload, broadcast=True)
 