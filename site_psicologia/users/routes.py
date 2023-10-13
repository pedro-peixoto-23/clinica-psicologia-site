from flask import Blueprint
from site_psicologia.database.db_functions import *
from flask import render_template, redirect, request, url_for
from site_psicologia import send_email
import json

users = Blueprint('users', __name__)

@users.route("/marcar_consulta", methods=["GET", "POST"])
def marcar_consulta():
    erro_cpf = None
    valores = []

    if request.method == "POST":
        cpf_usuario = request.form["cpf"].replace(".", "").replace("-", "")
        result = cpf_em_agendamentos(cpf_usuario)
        if result is None:
            inserir_agendamento(
                request.form["nome"],
                cpf_usuario,
                request.form["email"],
                request.form["calendario"],
                request.form["horario"],
                request.form["servico"],
            )
            send_email.enviar_email(
                request.form["nome"],
                cpf_usuario,
                request.form["email"],
                request.form["calendario"],
                request.form["horario"],
                request.form["servico"],
            )
            return redirect(url_for('users.consulta_agendada'))
        else:
            erro_cpf = True
            valores.append(request.form.get('nome'))
            valores.append(request.form.get('cpf'))
            valores.append(request.form.get('email'))
            valores.append(request.form.get('calendario'))
            valores.append(request.form.get('horario'))
            valores.append(request.form.get('sevico'))
    datas_e_horarios = json.dumps(lista_de_dicionarios_com_horarios_utilizados_por_data())
    return render_template("/principais/marcar_consulta.html", datas_e_horarios=datas_e_horarios, valores=valores, erro_cpf=erro_cpf)


@users.route("/consulta_agendada")
def consulta_agendada():
    return render_template("/telas-finalizacao-e-erro/consulta_agendada.html")


@users.route("/verificar_dados_agendamento", methods=["GET", "POST"])
def verificar_dados_agendamento():
    if request.method == "POST":
        global cpf_usuario_verificar_consulta
        cpf_usuario_verificar_consulta = (
            request.form["cpf"].replace(".", "").replace("-", "")
        )
        result = cpf_em_agendamentos(cpf_usuario_verificar_consulta)

        if result == None:
            return render_template("/telas-agendado-nao-agendado/nao_agendado.html")
        else:
            return render_template( "/telas-agendado-nao-agendado/ja_agendado.html", consulta_cadastrada=result)
    else:
        return render_template("/principais/verificar_dados_agendamento.html")


@users.route("/verificar_se_quer_apagar")
def verificar_se_quer_apagar():
    return render_template("/telas-finalizacao-e-erro/apagar_ou_nao.html")


@users.route("/apagar_consulta")
def apagar_consulta():
    agendamento_para_apagar = cpf_usuario_verificar_consulta
    remover_agendamento_cpf(agendamento_para_apagar)
    return redirect(url_for('users.consulta_apagada'))


@users.route("/consulta_apagada")
def consulta_apagada():
    return render_template("/telas-finalizacao-e-erro/consulta_apagada.html")