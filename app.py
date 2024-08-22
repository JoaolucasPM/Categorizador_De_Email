import json
from datetime import datetime
from imap_tools import MailBox, AND
from imap_tools.errors import MailboxUidsError


def load_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = json.load(file)
    return credentials


credentials = load_credentials('credentials.json')

# Acessar o usuário e a senha
username = credentials.get('username')
password = credentials.get('password')


# Carregar categorias do arquivo JSON
with open("categorias.json", "r", encoding="utf-8") as arquivo:
    categorias = json.load(arquivo)


with MailBox('imap.gmail.com').login(username, password) as mailbox:
    # Iterar sobre todas as categorias
    for categoria_info in categorias:
        categoria = categoria_info["Categoria"]
        assunto = categoria_info["Assunto"]

        # Verificar se a pasta da categoria já existe, senão criar
        if not mailbox.folder.exists(categoria):
            try:
                mailbox.folder.create(categoria)
                print(f"Pasta '{categoria}' criada com sucesso.")
            except Exception as e:
                print(f"Erro ao criar a pasta '{categoria}': {e}")

        # Pular se o assunto for vazio ou "sem assunto"
        if not assunto or assunto.lower() == "sem assunto":
            print(f"Pulado: Assunto inválido '{assunto}'")
            continue

        # Consultar os emails na caixa de entrada que têm o assunto desejado
        try:
            emails_com_assunto = mailbox.fetch(AND(subject=assunto))
        except MailboxUidsError as e:
            print(f"Erro ao buscar emails com assunto '{assunto}': {e}")
            continue
        except Exception as e:
            print(f"Erro inesperado ao buscar emails com assunto '{assunto}': {e}")
            continue

        # Iterar sobre os emails encontrados
        for email in emails_com_assunto:
            # Verificar se o email tem um assunto válido
            if not email.subject:
                print("Email sem assunto encontrado, pulando.")
                continue

            try:
                # Mover o email para a pasta correspondente à categoria
                mailbox.move(email.uid, categoria)
                print(f"Email com assunto '{email.subject}' movido para a pasta '{categoria}'")
            except Exception as e:
                print(f"Erro ao mover o email '{email.subject}' para a pasta '{categoria}': {e}")