import requests as r
import logging
import os
import json
import re
from bs4 import BeautifulSoup
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
    
    def obterDadosResolucao(self,json):
        html = str(json['notes'])

        logging.info("Formatando resolução")
        hr_index = html.find('<hr/>') #finaliza no primeiro hr
        primeira_interacao_html = html[:hr_index].strip() #corta tudo após o hr deixando somente a primeira interação

        match_data = re.search(r'\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2}', primeira_interacao_html) #obter a data
        data = match_data.group(0) if match_data else ''

        match_nome = re.search(r'<strong>(.*?)</strong>', primeira_interacao_html) #buscar o nome do agente
        nome = match_nome.group(1).strip() if match_nome else ''


        soup = BeautifulSoup(primeira_interacao_html, 'html.parser') #Extrai o texto limpo
        texto_completo = soup.get_text(separator="\n").strip()


        indice_inicio_mensagem = texto_completo.lower().find("tempo gasto") #Encontra índice após "Tempo gasto"
        if indice_inicio_mensagem != -1:
            # Pega tudo após "tempo gasto", pulando os dois-pontos e tempo
            texto_pos_tempo = texto_completo[indice_inicio_mensagem:]
            # Pega a próxima linha útil
            linhas = texto_pos_tempo.splitlines()
            try:
                idx = next(i for i, linha in enumerate(linhas) if "tempo gasto" in linha.lower()) #separa a string e busca o tempo gasto
                mensagem = "\n".join(linhas[idx + 1:]).strip() #concatena todas as mensagens após o idx(tempo gasto)
            except StopIteration:
                mensagem = texto_completo.strip()
        else:
            mensagem = texto_completo.strip()

        return mensagem.strip(),data,nome


    
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

            resolucao = {
                "resolucao" : "",
                "resolucao_data" : "",
                "resolucao_agente" : ""
            }

            comments = data.get('comments', [])
            email = data.get('email_tech') if data.get('email_tech') is not None else ""
            
            if data['status'] in ("Resolved", "Closed"):
                resolucao['resolucao'],resolucao["resolucao_data"],resolucao["resolucao_agente"] = self.obterDadosResolucao(data)

            if comments:
                ultima_interacao = comments[-1]
                self.ticketId = None
                return {
                    "email_responsavel": email,
                    "ultima_interacao": ultima_interacao['description'].replace("<p>", "").replace("</p>", ""),
                    "ultima_interacao_data": ultima_interacao['dt_cad'],
                    "ultima_interacao_pessoa": ultima_interacao['name_create']
                } | resolucao
            else:
                self.ticketId = None
                return{
                    "email_responsavel": email,
                    "ultima_interacao": "",
                    "ultima_interacao_data": "",
                    "ultima_interacao_pessoa": ""
                } | resolucao
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
                responsavel = data[0]['grid_service_technician'] if data[0]['grid_service_technician'] is not None else ""
                return {
                    "id_ticket" : f"{data[0]['id_tickets']}",
                    "solicitante" : f"{data[0]['grid_user']}",
                    "status"  : f"{data[0]['grid_waiting']}",
                    "equipe" : f"{data[0]['grid_tech_group']}",
                    "responsavel" : f"{responsavel}"
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

