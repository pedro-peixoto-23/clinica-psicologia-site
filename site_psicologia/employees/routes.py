from flask import Blueprint
from flask import render_template, request, redirect, url_for, session
from site_psicologia.database.db_functions import (lista_agendamentos, nome_usuario_e_senha_em_funcionarios,
                                                   remover_agendamento_id)

employees = Blueprint('employees', __name__)


@employees.route("/agendamentos")
def agendamentos():
    if "usuario" in session:
        result = lista_agendamentos()
        return render_template("agendamentos.html", dados=result, usuario_dentro=session["usuario"])
    else:
        return redirect(url_for('employees.login_funcionario'))


@employees.route("/login_funcionario", methods=["GET", "POST"])
def login_funcionario():
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        result = nome_usuario_e_senha_em_funcionarios(login, senha)

        if result == None:
            return render_template("/funcionarios/form-login-funcionarios.html", sucesso=False)
        else:
            session["usuario"] = login
            session["senha"] = senha
            return redirect(url_for('employees.agendamentos'))
    return render_template("/funcionarios/form-login-funcionarios.html")


@employees.route("/agendamentos/apagar/<int:id>")
def apagar_agendamento_id(id):
    if "usuario" in session:
        remover_agendamento_id(id)
        return redirect(url_for('employees.agendamentos'))
    else:
        return redirect(url_for('employees.login-banco-dados'))
