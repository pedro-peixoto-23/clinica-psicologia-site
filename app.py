from flask import Flask, render_template, request, redirect, session
from db_functions import *
from send_email import enviar_email
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')  # necessário para criptografar os dados dos coockies da sessão


# 1. Funcionalidades do usuário que irá acessar o site

# Rota responsável por retornar o html com a tela inicial
@app.route('/')
def home():
    return render_template('/principais/home.html')


# Retorna o html com as especificações da clínica, mostrando como ela trabalha
@app.route('/especificacoes')
def especificacoes():
    return render_template('/principais/especificacoes.html')


# Essa rota retorna o html com o formulário de agendamento
@app.route('/marcar_consulta')
def marcar_consulta():
    datas_e_horarios = json.dumps(lista_de_dicionarios_com_horarios_utilizados_por_data())
    return render_template('/principais/marcar_consulta.html', datas_e_horarios=datas_e_horarios)


# Essa rota tem a função de receber os dados do formulário de agendamento e verificar se já
# existe alguma consulta já agendada com o cpf inserido pelo usuário, caso exista, retorna
# o html de erro, informando que já foi feito um agendamento com o cpf digitado. Caso não exista,
# insere os dados informados para o agendamento no banco de dados de agendamento e retorna o html
# com a mensagem de consulta agendada com sucesso.
@app.route("/receber_dados_formulario_consulta", methods=['POST'])
def receber_dados_formulario_consulta():
    cpf_usuario = request.form['cpf'].replace(".", "").replace("-", "")

    result = cpf_em_agendamentos(cpf_usuario)
    print(request.form['calendario'])
    if result == None:
        inserir_agendamento(request.form['nome'], cpf_usuario, request.form['email'], request.form['calendario'],
                            request.form['horario'], request.form['servico'])
        enviar_email(request.form['nome'], cpf_usuario, request.form['email'], request.form['calendario'],
                     request.form['horario'], request.form['servico'])
        return redirect('/consulta_agendada')
    else:
        return render_template('/telas-finalizacao-e-erro/erro_ja_tem_agendamento.html')


# Retorna um html informando que a consulta foi agendada com sucesso
@app.route('/consulta_agendada')
def consulta_agendada():
    return render_template('/telas-finalizacao-e-erro/consulta_agendada.html')


# Retorna o html com o formulário que recebe o cpf para verificar os dados de agendamento
@app.route('/verificar_dados_agendamento')
def verificar_dados_agendamento():
    return render_template('/principais/verificar_dados_agendamento.html')


# Essa rota é responsável por verificar o cpf informado no formulário de verificação de dados de
# agendamento e verificar se ele existe no banco de dados, se existir, retorna o html com as informações
# do agendamento. Caso não exista, retorna um html informando que não existe no banco de dados o cpf
# informado.
# Além disso, ele cria uma variável cpf global para que possa ser acessado enquanto ele estiver
# na página html que mostra os dados da consulta, pois será necessário caso ele queira apagar
# a consulta.
@app.route('/receber_cpf_verificacao', methods=['POST'])
def receber_cpf_verificacao():
    global cpf_usuario_verificar_consulta
    cpf_usuario_verificar_consulta = request.form['cpf'].replace(".", "").replace("-", "")
    result = cpf_em_agendamentos(cpf_usuario_verificar_consulta)

    if result == None:
        return render_template('/telas-agendado-nao-agendado/nao_agendado.html')
    else:
        return render_template('/telas-agendado-nao-agendado/ja_agendado.html', consulta_cadastrada=result)


# Essa rota chama a função que retorna um html que pergunta ao usuário se ele deseja realmente apagar
# o agendamento.
@app.route('/verificar_se_quer_apagar')
def verificar_se_quer_apagar():
    return render_template('/telas-finalizacao-e-erro/apagar_ou_nao.html')


# Essa rota chama a função que apaga o agendamento usando a variável global do cpf criada na rota
# /receber_cpf_verificacao e redireciona para a rota que mostra o html informando que o agendamento
# foi apagado com sucesso.
@app.route('/apagar_consulta')
def apagar_consulta():
    agendamento_para_apagar = cpf_usuario_verificar_consulta
    remover_agendamento_cpf(agendamento_para_apagar)
    return redirect('/consulta_apagada')


# Essa rota retorna o html que mostra que o agendamento foi apagado com sucesso
@app.route('/consulta_apagada')
def consulta_apagada():
    return render_template('/telas-finalizacao-e-erro/consulta_apagada.html')


# 2. Funcionalidades do banco de dados dos cadastrados para mexer no banco de dados de agendamentos

# Essa rota é responsável por retornar um html com todos os agendamentos. Mas não é possível
# acessar essa rota caso não tenha feito o login na sessão. E caso isso aconteça, redireciona
# para a rota a seguir, que pede o login no banco de dados. Caso já tenha feito o login, retorna
# o html com os agendamentos e também manda para esse html o usuário que está logado, para que
# o usuário veja que está logado na conta.
@app.route("/agendamentos")
def agendamentos():
    if 'usuario' in session:
        result = lista_agendamentos()
        return render_template('agendamentos.html', dados=result, usuario_dentro=session['usuario'])
    else:
        return redirect('/login-banco-dados')


# Essa rota retorna o html de login para acessar os dados dos agendamentos.
@app.route('/login-banco-dados')
def login_banco_dados():
    return render_template('/funcionarios/form-login-funcionarios.html')


# Essa rota é responsável por verificar se os dados de login inseridos na rota anterior são válidos
# ou seja, ele só vai ser redirecionado para o banco com os agendamentos se o login e senha estiver
# no banco de dados de pessoas com permissão para acessar o banco de dados. Caso o login não seja
# bem sucessido, retorna um alerta mostrando que os dados inseridos não são válidos
@app.route('/verificar_login', methods=['POST'])
def verificar_login():
    login = request.form['login']
    senha = request.form['senha']

    result = nome_usuario_e_senha_em_funcionarios(login, senha)

    if result == None:
        return render_template('/funcionarios/form-login-funcionarios.html', sucesso=False)
    else:
        session['usuario'] = login
        session['senha'] = senha
        return redirect('/agendamentos')
    # return render_template('/funcionarios/form-login-funcionarios.html')


# Essa rota é chamada quando é apertado o botão de deletar na lista de agendamentos, e vai com
# ele o id da linha que deseja deletar, desta forma, ela apenas tem a função de verificar no banco de
# dados qual o agendamento que tem esse id e deleta essa linha da tabela. E redireciona novamente
# para a rota de agendamentos.
@app.route("/agendamentos/apagar/<int:id>")
def apagar_agendamento_por_botao_banco_dados(id):
    if 'usuario' in session:
        remover_agendamento_id(id)
        return redirect('/agendamentos')
    else:
        return redirect('/login-banco-dados')


# 3. Funcionalidades para cadastrar novas pessoas que tem acesso ao banco de dados

# Essa rota retorna um arquivo html com uma lista com todas as pessoas permitidas para
# acessarem o banco de dados com os agendamentos
@app.route("/funcionarios")
def funcionarios():
    result = lista_de_funcionarios()
    return render_template('/funcionarios/funcionarios.html', dados=result)


# Essa rota retorna o html com o formulário de cadastro de novas pessoas que podem
# acessar o banco de dados dos agendamentos
@app.route("/funcionarios/cadastro")
def cadastro_funcionario():
    return render_template('/funcionarios/form-cadastrar-funcionario.html')


# Essa rota é responsável por pegar os dados inseridos na rota anterior, verificar se já existe
# no banco de dados e, se não existir, insere no banco de dados a nova pessoa que pode acessar
# o banco de dados com os agendamentos
@app.route('/funcionarios/cadastro/verificar_dados', methods=['POST'])
def verificar_dados_cadastro_funcionario():
    login = request.form['login']
    senha = request.form['senha']

    result = nome_usuario_e_senha_em_funcionarios(login, senha)

    if result == None:
        inserir_funcionario(login, senha)
        return redirect('/funcionarios')
    else:
        return render_template('/funcionarios/funcionarios.html')


# Essa rota traz consigo uma variável "id" quem vem da página html "funcionarios.html" e
# essa rota é responsável por pegar esse "id", procurar no banco quem tem esse id e deletar ele
# e retorna para a página novamente de listagem com as pessoas permitidas.
@app.route("/funcionarios/apagar/<int:id>")
def apagar_pessoas_permitidas(id):
    remover_funcionario(id)
    return redirect('/funcionarios')


# Inicia a aplicação
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
