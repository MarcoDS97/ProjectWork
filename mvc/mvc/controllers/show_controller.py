from flask import Blueprint, jsonify

from models.show import Show
from views.show_view import render_show_page

show_controller = Blueprint('show_controller', __name__)

@show_controller.route('/data/shows', methods=['GET'])
def get_data_shows():
    shows = Show.get_all()
    return jsonify([s.to_dict() for s in shows])

@show_controller.route('/shows', methods=['GET'])
def show_shows():
    risposta = get_data_shows()
    lista_show = risposta.json
    return render_show_page(lista_show)