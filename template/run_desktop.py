# import FlaskUI
from flaskwebgui import FlaskUI

# Import APP
from app import app, socketio

# add app and parameters
ui = FlaskUI(app, maximized = True, start_server = 'flask', socketio = socketio, port = 7000)

if __name__ == "__main__":
    # app.run() for debug
    ui.run()
