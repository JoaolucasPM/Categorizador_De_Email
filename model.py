from imap_tools import MailBox, AND
from datetime  import datetime
import json
import re


def load_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = json.load(file)
    return credentials


credentials = load_credentials('credentials.json')
data_inicial = datetime.strptime("20/05/2024", '%d/%m/%Y').date()

# Acessar o usuário e a senha
username = credentials.get('username')
password = credentials.get('password')
lista_email_ = []

def formatar_assunto(assunto):
    assunto_formatado = re.sub(r'[^\x00-\x7F]+', ' ', assunto)
    return assunto_formatado

with MailBox('imap.gmail.com').login(username, password ) as mailbox:

    lista_email = list(mailbox.fetch(AND(date_gte=data_inicial)))

    for l in lista_email:
     assunto = l.subject
     msg     = (l.text)

     lista_email_.append(
        {
        'Assunto': formatar_assunto(assunto), 
        'Mensagem':msg
        }
        )

with open('emails.json', 'w', encoding='utf-8') as f:
    json.dump(lista_email_, f, ensure_ascii=False, indent=4)

print('SUCESSO: JSON(email) GERADO!!!')