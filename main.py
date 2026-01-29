import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
import json


# Carregar variáveis de ambiente do arquivo .env]
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

with open("instrucoes.json", "r", encoding="utf-8") as arquivo:
    configuracao = json.load(arquivo)

system_instruction = json.dumps(configuracao, indent=2, ensure_ascii=False)

# system_instruction = 


# configurar modelo
config = types.GenerateContentConfig(
    temperature=0.7,
    top_p=0.95,
    top_k=40,
    max_output_tokens=1000,
    response_mime_type="text/plain",
    system_instruction=system_instruction # Instrução de sistema entra na config agora
)

def iniciar_chat():
    chat = client.chats.create(
        model="gemini-2.5-flash-lite", # Ou "gemini-1.5-flash"
        config=config
    )
    print("Bem-vindo ao Codeman! Como posso ajudar você com Python e RPA hoje?")
    print("Digite 'sair' para encerrar a sessão.")

    while True:
        try:
            user_input = input("Você: ").strip()
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando a sessão. Até a próxima!")
                break

            if not user_input:
                continue
            
            print('\n codeman: ', end='')

            response = chat.send_message_stream(user_input)

            for chunk in response:
                print(chunk.text, end='')    
            print('\n' + '-'*50 + '\n')

        except Exception as e:
            print(f"Erro ao processar a solicitação: {e}")

if __name__ == "__main__":
    iniciar_chat()