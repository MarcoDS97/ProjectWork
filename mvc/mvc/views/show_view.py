# views/show_view.py

from flask import render_template

def render_show_page(shows):
    return render_template('show.html', shows=shows)
