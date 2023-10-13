from flask import Blueprint
from flask import render_template, request, redirect, url_for
from site_psicologia.database.db_functions import (lista_de_funcionarios, nome_usuario_e_senha_em_funcionarios,
                                                   inserir_funcionario, remover_funcionario)

manager = Blueprint('manager', __name__)


@manager.route("/funcionarios")
def funcionarios():
    result = lista_de_funcionarios()
    return render_template("/funcionarios/funcionarios.html", dados=result)


@manager.route("/funcionarios/cadastro", methods=["GET", "POST"])
def cadastro_funcionario():
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        result = nome_usuario_e_senha_em_funcionarios(login, senha)

        if result == None:
            inserir_funcionario(login, senha)
            return redirect(url_for('manager.funcionarios'))
        else:
            return render_template("/funcionarios/funcionarios.html")
    return render_template("/funcionarios/form-cadastrar-funcionario.html")


@manager.route("/funcionarios/apagar/<int:id>")
def apagar_funcionario(id):
    remover_funcionario(id)
    return redirect(url_for('manager.funcionarios'))
