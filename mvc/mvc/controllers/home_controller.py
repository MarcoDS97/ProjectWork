from flask import Blueprint


from views.show_home import render_show_home

home_controller = Blueprint('home_controller', __name__)

@home_controller.route('/')
def home():
    return render_show_home()
