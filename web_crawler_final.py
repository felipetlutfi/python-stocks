from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/obter_dados', methods=['GET'])
def obter_dados():
    url = "https://statusinvest.com.br/acoes/variacao/ibovespa"

    # Adiciona um cabeçalho de agente de usuário à solicitação
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Faz a solicitação HTTP para obter o conteúdo da página
    response = requests.get(url, headers=headers)

    # Verifica se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Obtém o conteúdo HTML da página
        html_content = response.content

        # Usa o BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontra o elemento input com os atributos especificados
        input_element = soup.find('input', {'id': 'result', 'name': 'result', 'type': 'hidden'})

        # Verifica se o elemento foi encontrado
        if input_element:
            # Obtém o valor do atributo 'value'
            result_value = input_element.get('value')

            # Converte a string JSON para uma lista de dicionários em Python
            dados = json.loads(result_value)

            # Seleciona apenas os três primeiros elementos da lista
            output_data = [{'code': item['code'], 'resultPercentageValue': item['resultPercentageValue'], 'afterMarket': item['afterMarket']} for item in dados[:3]]

            # Retorna os dados como JSON
            return jsonify(output_data)

        else:
            return jsonify({"error": "Elemento não encontrado."})

    else:
        return jsonify({"error": f"Erro ao acessar a URL. Código de status: {response.status_code}"})

if __name__ == '__main__':
    app.run(debug=True)
