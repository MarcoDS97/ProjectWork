from flask import Flask
from controllers.show_controller import show_controller
from controllers.home_controller import home_controller


app = Flask(__name__)

app.register_blueprint(show_controller)
app.register_blueprint(home_controller)

if __name__ == '__main__':
    app.run(debug=True)
