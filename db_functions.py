from sqlalchemy import text
from db_connection import engine


def lista_agendamentos():
    with engine.connect() as conn:
        result = conn.execute(text("select * from agendamentos"))
    return result.all()


def cpf_em_agendamentos(cpf_usuario):
    with engine.connect() as conn:
        result = conn.execute(text("select * from agendamentos where cpf = :cpf_usuario"), {"cpf_usuario": cpf_usuario})
        rows = result.all()
        print(rows)
        if (len(rows) > 0):
            return rows[0]
        return None


def inserir_agendamento(nome, cpf, email, data, horario, servico):
    with engine.connect() as conn:
        query = text(
            "insert into agendamentos (nome, cpf, email, servico, data, horario) values (:nome, :cpf, :email, :servico, :data, :horario)")
        conn.execute(query,
                     {"nome": nome, "cpf": cpf, "email": email, "data": data, "horario": horario, "servico": servico})


def remover_agendamento_cpf(cpf):
    with engine.connect() as conn:
        conn.execute(text("delete from agendamentos where cpf = :cpf"), {"cpf": cpf})


def remover_agendamento_id(id):
    with engine.connect() as conn:
        conn.execute(text("delete from agendamentos where id = :id"), {"id": id})


def lista_de_dicionarios_com_horarios_utilizados_por_data():
    with engine.connect() as conn:
        result = conn.execute(text("select distinct data from agendamentos"))

    lista_datas_diferentes = []
    for elemento in result.all():
        lista_datas_diferentes.append(elemento[0])

    lista_datas_diferentes_string = []
    for data in lista_datas_diferentes:
        dia = data.day
        mes = data.month
        ano = data.year

        string = f"{str(ano)}-{str(mes)}-{str(dia)}"

        lista_datas_diferentes_string.append(string)

    lista_dicionarios = []
    for data in lista_datas_diferentes_string:
        with engine.connect() as conn:
            result = conn.execute(text("select horario from agendamentos where data=:data"), {"data": data})
        lista_horarios = []
        for elemento in result.all():
            lista_horarios.append(elemento[0])

        dicionario = {"data": data, "horarios_preenchidos": lista_horarios}
        lista_dicionarios.append(dicionario)

    return lista_dicionarios


def lista_de_funcionarios():
    with engine.connect() as conn:
        result = conn.execute(text("select * from cadastrados"))
    return result.all()


def nome_usuario_e_senha_em_funcionarios(nome_usuario, senha):
    with engine.connect() as conn:
        result = conn.execute(text("select * from cadastrados where nome_usuario = :nome_usuario and senha = :senha"),
                              {"nome_usuario": nome_usuario, "senha": senha})
        rows = result.all()
        if (len(rows) > 0):
            return rows[0]
        return None


def inserir_funcionario(nome_usuario, senha):
    with engine.connect() as conn:
        query = text("insert into cadastrados (nome_usuario, senha) values (:nome_usuario, :senha)")
        conn.execute(query, {"nome_usuario": nome_usuario, "senha": senha})


def remover_funcionario(id):
    with engine.connect() as conn:
        conn.execute(text("delete from cadastrados where id = :id"), {"id": id})


print(lista_agendamentos())
