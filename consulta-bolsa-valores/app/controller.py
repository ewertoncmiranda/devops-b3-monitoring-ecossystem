import requests
from flask import Flask, jsonify
app = Flask(__name__)
# Uso
api_key = "kJfyqy8yUVj94SivLsKq4Q"


@app.route('/ativos/<symbol>', methods=['GET'])
def buscar_ativo(symbol):
    ativo = consultar_brapi(symbol,api_key)
    return jsonify(ativo), 200



def consultar_brapi(symbol: str, api_key: str):
    url = f"https://brapi.dev/api/quote/{symbol}"
    headers = {
        "Authorization": api_key,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dados = response.json()
        print("Resposta da API BRAPI:")
        print(dados)
        return dados
    else:
        print(f"Erro: {response.status_code} - {response.text}")
        return None

# Executa a API
if __name__ == '__main__':
    app.run(debug=True)
