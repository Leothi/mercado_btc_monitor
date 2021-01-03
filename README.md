# mercado_btc_monitor
Monitor de preços de BTC na corretora Mercado Bitcoin.

Em construção.

# Features atuais
1) Logger de preço atual.
2) Notificação para preço target (maior ou menor que atual).
3) Mensagem periódica de BOT via Telegram para as opções acima.


# Pré-requisitos para BOT Telegram
* Criar BOT via @BOTFather e pegar seu token:
    https://medium.com/shibinco/create-a-telegram-bot-using-botfather-and-get-the-api-token-900ba00e0f39
* Obter chat_id(s) para conversa(s) com o BOT:
    https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id


# Como utilizar via GCP
* Necessário conhecimento prévio na ferramenta.
* Criar arquivo `app.yaml` no mesmo diretório do Dockerfile com *runtime* e *env* necessários para Dockerfile, *env_variables* com as mesmas variáveis de ambiente citadas acima e número máximo de instâncias = 1, visto que algo maior que esse número pode causar divergência entre os atributos de configuração da classe salvos em memória. Exemplo:

    ```yaml
    runtime: custom
    env: flex
    env_variables:
        BOT_TOKEN: '<token do bot criado>'
        LOGGER_CHAT_ID: '<chat_id para logging do preço atual>'
        TARGET_CHAT_ID: '<chat_id para alerta de target price>'
    automatic_scaling:
        max_num_instances: 1
    ```
* Obs.: não é obrigatório usar dois IDs diferentes para os chats. Pode ser feito somente para separar as funções, controlar separadamente as notificações no celular, etc. Caso queria utilizar o mesmo chat, colocar o ID igual para as duas varíaveis de ambiente.

* Fazer deploy com App Engine (`gcloud app deploy` no diretório do `app.yaml`.
* Setar crons via Cloud Scheduler para os endpoints desejados.


# Como utilizar localmente
* Opção Docker: buildar imagem via Dockerfile depois rodar container publicando na porta 8080.
* Opção sem Docker: instalar pacote via `setup.py`, rodar a aplicação com `run.sh` ou `run_uvicorn.sh`.
* Aplicação roda em `0.0.0.0:8080/docs` por padrão.
* Na opção local, a notificação periódica via Telegram é desabilitada.
* Alterar as seguintes váriáveis de ambiente (recomendado utilizar arquivo `.env` no mesmo diretório de `settings.py`):
    ```.env
    BOT_TOKEN = '<token do bot criado>'
    LOGGER_CHAT_ID = '<chat_id para logging do preço atual>'
    TARGET_CHAT_ID = '<chat_id para alerta de target price>'  
    ```
* Obs.: não é obrigatório usar dois IDs diferentes para os chats. Pode ser feito somente para separar as funções, controlar separadamente as notificações no celular, etc. Caso queria utilizar o mesmo chat, colocar o ID igual para as duas varíaveis de ambiente.


# Algumas ferramentas utilizadas na construção
* Docker
* FastAPI
* Loguru
* Gunicorn
* Uvicorn
* API Telegram
* API de Dados Mercado Bitcoin
* GCP App Engine
* GCP Cloud Scheduler

# Exemplo de funcionamento
## Swagger
![swagger](https://user-images.githubusercontent.com/42444599/103489978-6ca5d400-4df7-11eb-859f-e23d9bbc3cba.png)

## Telegram
![logger](https://user-images.githubusercontent.com/42444599/103447296-e4dd8f80-4c67-11eb-8a89-561253339120.png)
![price_target](https://user-images.githubusercontent.com/42444599/103447301-0179c780-4c68-11eb-9053-77d1e086b915.png)
