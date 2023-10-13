from flask import Blueprint
from flask import render_template

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("/principais/home.html")


@main.route("/especificacoes")
def especificacoes():
    return render_template("/principais/especificacoes.html")
