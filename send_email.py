import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

def enviar_email(nome, cpf, email, data, horario, servico):
    corpo_email = f"""
        <h1>Cadastro realizado com sucesso</h1>
        <p>Parabéns, o agendamento foi bem sucedido!</p>
        <hr>
        <h2>Dados de agendamento</h2>
        <p>Nome: {nome}</p>
        <p>CPF: {cpf}</p>
        <p>Email: {email}</p>
        <p>Data: {data}</p>
        <p>Horário: {horario}</p>
        <p>Serviço: {servico}</p>
    """

    # Definindo os campos do email
    msg = EmailMessage()
    msg['Subject'] = f"Agendamento site psicologia - {nome}"
    msg['From'] = os.environ.get('EMAIL_FROM')
    msg['To'] = email

    # Senha do google (meus apps)
    password = os.environ.get('EMAIL_PASSWORD')

    # Indicando que o conteúdo é HTML
    msg.add_header('Content-Type', 'text/html')
    # Definindo o corpo do email como UTF-8
    msg.set_payload(corpo_email.encode('utf-8'))

    try:
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        # Inicia a conexão com o servidor smtp
        smtp.starttls()
        # Faz o login no servidor
        smtp.login(msg['From'], password)
        # Enviando o email
        smtp.sendmail(msg['From'], [msg['To']], msg.as_bytes())
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o email: {e}")
