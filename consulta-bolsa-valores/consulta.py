import requests


def consultar_brapi(symbol: str, api_key: str):
    url = f"https://brapi.dev/api/quote?symbol={symbol}"

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

# Uso
api_key = "kWhniTpNuPCHmwHGeQyTiG"
symbol = "PETR4"
consultar_brapi(symbol, api_key)