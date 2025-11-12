from messengerApp import create_app
from messengerApp.extensions import socketio
 
app = create_app()
if __name__ == "__main__":
    socketio.run(app, debug=True)
    # app.run(debug=True)