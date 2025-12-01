import requests
from flask import Flask, jsonify
from functools import lru_cache
import os
import time

app = Flask(__name__)

# ------------------------------------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------------------------------------

# Nunca deixe API KEY hardcoded em produção!
API_KEY = os.getenv("BRAPI_KEY", "kJfyqy8yUVj94SivLsKq4Q")

# Tempo de cache para evitar chamar BRAPI toda hora (em segundos)
CACHE_TTL = 10


# ------------------------------------------------------------------------------
# CACHE SIMPLES EM MEMÓRIA
# ------------------------------------------------------------------------------
_cache = {}

def cache_get(key):
    item = _cache.get(key)
    if item:
        value, timestamp = item
        if time.time() - timestamp < CACHE_TTL:
            return value
    return None

def cache_set(key, value):
    _cache[key] = (value, time.time())


# ------------------------------------------------------------------------------
# CONSULTA À BRAPI COM RESILIÊNCIA
# ------------------------------------------------------------------------------
def consultar_brapi(symbol: str, api_key: str):
    url = f"https://brapi.dev/api/quote/{symbol}"

    headers = {
        "Authorization": api_key,
        "Accept": "application/json"
    }

    # 1) Busca no cache primeiro
    cached = cache_get(symbol)
    if cached:
        return cached

    try:
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            dados = response.json()

            # Armazena o retorno no cache
            cache_set(symbol, dados)

            return dados

        elif response.status_code == 404:
            return {"erro": f"Ação {symbol} não encontrada na BRAPI"}

        else:
            return {
                "erro": "Falha ao consultar BRAPI",
                "status": response.status_code,
                "detalhe": response.text
            }

    except requests.exceptions.Timeout:
        return {"erro": "Timeout ao consultar a BRAPI"}

    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro de rede: {str(e)}"}


# ------------------------------------------------------------------------------
# ROTAS
# ------------------------------------------------------------------------------
@app.route('/ativos/<symbol>', methods=['GET'])
def buscar_ativo(symbol):
    ativo = consultar_brapi(symbol.upper(), API_KEY)
    status = 200 if "erro" not in ativo else 400
    return jsonify(ativo), status


# ------------------------------------------------------------------------------
# EXECUÇÃO LOCAL
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
