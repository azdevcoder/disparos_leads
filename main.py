import os
import time
import requests
import urllib.parse

# Configurações da sua API de WhatsApp (Exemplo usando uma API genérica)
API_URL = os.getenv("WHATSAPP_API_URL") # Ex: https://api.z-api.io/instancia/send-text
API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")

def buscar_contatos_pendentes():
    # Aqui substituímos a leitura do CSV pela busca no Banco de Dados ou Google Sheets
    # Exemplo de retorno esperado:
    return [
        {"id": 1, "title": "Gih modas", "phone": "5511942454686", "enviado": False},
        {"id": 2, "title": "Jessica Modas", "phone": "5511948948733", "enviado": False}
    ]

def marcar_como_enviado(contato_id):
    # Função para dar o UPDATE no banco de dados ou no Google Sheets
    print(f"Status atualizado para enviado no ID: {contato_id}")

def disparar_mensagens():
    contatos = buscar_contatos_pendentes()
    
    for contato in contatos:
        mensagem = f"Bom dia tudo bem?\nMe chamo André da AzDev Coder\nvisitei sua empresa no google..."
        
        payload = {
            "phone": contato['phone'],
            "message": mensagem
        }
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Faz o disparo pela API via HTTP POST em vez de PyAutoGUI
        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                print(f"Mensagem enviada com sucesso para {contato['title']}")
                marcar_como_enviado(contato['id'])
            else:
                print(f"Erro ao enviar para {contato['title']}: {response.text}")
                
        except Exception as e:
            print(f"Falha de conexão: {e}")
            
        time.sleep(10) # Pausa estratégica para evitar bloqueios por spam

if __name__ == "__main__":
    disparar_mensagens()
