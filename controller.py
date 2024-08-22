import google.generativeai as genai
import json



def load_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = json.load(file)
    return credentials

credentials = load_credentials('credentials.json')
API = credentials.get('API')


genai.configure(api_key=API)
model = genai.GenerativeModel(model_name='gemini-1.0-pro')


caminho_arquivo = 'emails.json'  # 

# Abrir o arquivo JSON e carregar o conteúdo como um dicionário Python
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

def IA(p):
    
    chat = model.start_chat(history=[])
    prompt = (
        "Leia os seguintes emails e categorize-os em três categorias distintas com base no conteúdo dos emails "
        "e retorne uma estrutura JSON mas sem exibir os :"
        "\n\n"
        f"{json.dumps(p, ensure_ascii=False, indent=2)}"
        "\n\n"
        "Exemplo de estrutura JSON a ser retornada:"
        "["
        "{"
        '  "Categoria": "nome_da_categoria",'
        '  "Assunto": "assunto_do_email"'
    "}]"
)
    response = chat.send_message(prompt)
    return response.text

categorias_email = IA(dados)

with open('categorias.json', 'r', encoding='utf-8') as arquivo:
    categorias_email = json.load(arquivo)

# Filtrar os itens com assunto nulo
categorias_validas = [item for item in categorias_email if item["Assunto"] is not None]

# Escrever a lista filtrada no arquivo JSON
with open('categorias.json', 'w', encoding='utf-8') as f:
    json.dump(categorias_validas, f, ensure_ascii=False, indent=4)
print('JSON (categorias) criado!!!')