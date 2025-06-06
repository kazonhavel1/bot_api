import logging
from flask import Flask, request, jsonify
from dependence import sensr as s

logging.basicConfig(
            level=logging.INFO,
            filename="bot.log",
            format="%(asctime)s - %(levelname)s - %(message)s",
            encoding="utf-8"
        )

app = Flask(__name__)

sensr = s.consultaApi()

@app.route('/')
def index():
    response = {
        "mensagem": "Servidor no Ar! Utilize o metodo /ticket/<id do ticket> para iniciar a pesquisa."
    }
    return jsonify(response)

@app.route('/ticket/<ticket>', methods=['GET'])
def api_data(ticket):
    #payload = request.get_json() or {} Obter JSON da Requisição
    historico = None
    dados = None
    try:
        if sensr.tokenValido():
            dados = sensr.obterDadosTicket(ticket)
            if "error" in dados:
                response = dados
                return jsonify(response), 400         
            else:
                historico = sensr.obterHistoricoTicket()                   
            response = dados | historico  
        else:
            response = {
            "error": "Token inválido. Valide o log do servidor."
            }
            return jsonify(response), 400
        return jsonify(response)
    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {e}")
        return jsonify({
            "error" : "Erro interno ao processar a requisição."
        }), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8000,debug=False)