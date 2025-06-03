import requests as r
import logging
import os
import json
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv

class consultaApi():

    def __init__(self):
        self.token = None
        load_dotenv()
        logging.basicConfig(
            level=logging.INFO,
            filename="bot.log",
            format="%(asctime)s - %(levelname)s - %(message)s",
            encoding="utf-8"
        )
        self.ticketId = None
        #logging.info(f"mensagem informativa")
        #logging.error(f"mensagem de erro")
    def obterHistoricoTicket(self):
        url = os.getenv("linkhistoricoticket") + f"{self.ticketId}"
        headers = CaseInsensitiveDict()
        headers['x-access-token'] = self.token

        response = r.request("GET",url,headers=headers)
        logging.info("Consultando histórico do ticket")

        if response.status_code == 200 and response.text == "[]":
                logging.error(f"Histórico do Ticket {self.ticketId} não localizado.")
                self.ticketId = None
                return {
                    "error" : "Ticket não localizado."
                }
        elif response.status_code == 200:
            logging.info("Histórico disponibilizado.")
            data = response.json()

            comments = data['comments']

            ultima_interacao = comments[len(comments) - 1]
            self.ticketId = None
            return {
                "email_responsavel" : f"{data['email_tech']}",
                "ultima_interacao" : f"{ultima_interacao['description'].replace("<p>","").replace("</p>","")}",
                "ultima_interacao_data" : f"{ultima_interacao['dt_cad']}",
                "ultima_interacao_pessoa" : f"{ultima_interacao['name_create']}"
            }
        else:
            logging.error(f"Erro {response.status_code} ao consultar o histórico: {response.text}")
            return {
                "error" : f"Erro {response.status_code} ao consultar o histórico: {response.text}"
            }

    def obterDadosTicket(self,ticket):
            url = os.getenv("requisicaoporid")
            headers = CaseInsensitiveDict()
            headers['Content-Type'] = 'application/json'
            headers['Cookie'] = '36cb03=4wbk1NlPhXKatz6NWWppRuq3nDPp0iW6knwMYl6EeMfBhXBbK0glqRtr7/R3ZF3itfmcrQbFPPaGgeAIm80R9umee+AGGSqubC/Gktj1qfsBS6Al682650yRJ+VUcJfZmQAMIaRchigmifStoD2wzXu+k60OWkAfNQRojEFzihEbxkfy'
            headers['x-access-token'] = self.token

            payload = json.dumps({
                "statusFilter": [],
                "job": False,
                "filterColumns": {
                    "grid_id": f"{ticket}"
                }
            })
            logging.info(f"Pesquisando o ticket {ticket}...")
            response = r.request("POST",url,headers=headers, data=payload)

            if response.status_code == 200 and response.text == "[]":
                logging.error(f"Ticket {ticket} não localizado.")
                return {
                    "error" : "Ticket não localizado."
                }
            elif response.status_code == 200:
                data = response.json()
                logging.info("Pesquisa efetuada com sucesso.")
                self.ticketId = data[0]["id_tickets"]
                return {
                    "solicitante" : f"{data[0]['grid_user']}",
                    "status"  : f"{data[0]['grid_waiting']}",
                    "equipe" : f"{data[0]['grid_tech_group']}",
                    "responsavel" : f"{data[0]['grid_service_technician']}"
                }
            else:
                logging.error(f"Erro {response.status_code} ao efetuar a requisição no ticket {ticket}: {response.text}")
                return {
                    "error" : f"Erro {response.status_code} ao efetuar a requisição: {response.text}"
                }

    def obterToken(self):
        headers = CaseInsensitiveDict()
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '36cb03=4wbk1NlPhXKatz6NWWppRuq3nDPp0iW6knwMYl6EeMfBhXBbK0glqRtr7/R3ZF3itfmcrQbFPPaGgeAIm80R9umee+AGGSqubC/Gktj1qfsBS6Al682650yRJ+VUcJfZmQAMIaRchigmifStoD2wzXu+k60OWkAfNQRojEFzihEbxkfy'
        payload = json.dumps({
            "username": f"{os.getenv("mail")}",
            "password": f"{os.getenv("password")}"
        })
        logging.info("Obtendo um novo token")
        url = os.getenv("linktoken")
        response = r.request("POST", url, headers=headers, data=payload)

        if response.status_code != 200:
            logging.error(f"Erro {response.status_code} ao buscar o token. {response.text}")
            return None
        else:
            logging.info(f"Token obtido com sucesso.")
            resultado = response.json()
            return resultado['token']


    def tokenValido(self):
        if not self.token:
            self.token = self.obterToken()                    
            if self.token:
                return True
            else:
                return False
        
        if self.token:
            url = os.getenv("linktestetoken")

            headers = CaseInsensitiveDict()
            headers['Content-Type'] = 'application/json'
            headers['Cookie'] = '36cb03=4wbk1NlPhXKatz6NWWppRuq3nDPp0iW6knwMYl6EeMfBhXBbK0glqRtr7/R3ZF3itfmcrQbFPPaGgeAIm80R9umee+AGGSqubC/Gktj1qfsBS6Al682650yRJ+VUcJfZmQAMIaRchigmifStoD2wzXu+k60OWkAfNQRojEFzihEbxkfy'
            headers['x-access-token'] = self.token

            response = r.request("GET",url,headers=headers)

            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                logging.info("Token expirado. Obtendo um novo...")
                self.token = None
                self.token = self.obterToken()
                if self.token:
                    return True
                else:
                    return False
            else:
                logging.error(f"Erro {response.status_code} ao validar o token: {response.text}")
        return False

