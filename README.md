# mercado_btc_monitor
Monitor de preços de BTC na corretora Mercado Bitcoin.

Em construção.

# Features atuais
1) Logger de preço atual;
2) Notificação para preço target (maior ou menor que atual);
3) Mensagem periódica de BOT via Telegram para as opções acima.


# Pré-requisitos para BOT Telegram
* Criar BOT via @BOTFather;
* Obter token do BOT;
* Obter chat_id(s) para conversa(s) com o BOT.


# Como utilizar via GCP
* Necessário conhecimento prévio na ferramenta;
* Criar arquivo `app.yaml` no mesmo diretório do Dockerfile com *runtime* e *env* necessários para Dockerfile e *env_variables* com as mesmas variáveis de ambiente citadas acima. Exemplo:

    ```yaml
    runtime: custom
    env: flex
    env_variables:
        BOT_TOKEN: '<token do bot criado>'
        LOGGER_CHAT_ID: '<chat_id para logging do preço atual>'
        TARGET_CHAT_ID: '<chat_id para alerta de target price>'
    ```

* Fazer deploy com a ferramenta desejada (feito pelo App Engine);
* Setar crons via Cloud Scheduler para os endpoints desejados.


# Como utilizar localmente
* Opção Docker: buildar imagem via Dockerfile depois rodar container publicando na porta 8080;
* Opção sem Docker: instalar pacote via `setup.py`, rodar a aplicação com `run.sh` ou `run_uvicorn.sh`;
* Aplicação roda em `0.0.0.0:8080/docs` por padrão;
* Na opção local, a notificação periódica via Telegram é desabilitada.
* Alterar as seguintes váriáveis de ambiente (recomendado utilizar arquivo `.env` no mesmo diretório de `settings.py`):
    ```.env
    BOT_TOKEN = '<token do bot criado>'
    LOGGER_CHAT_ID = '<chat_id para logging do preço atual>'
    TARGET_CHAT_ID = '<chat_id para alerta de target price>'
    ```


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
![swagger](https://user-images.githubusercontent.com/42444599/103447287-c5466700-4c67-11eb-8752-21f3c6e639b5.png)

## Telegram
![logger](https://user-images.githubusercontent.com/42444599/103447296-e4dd8f80-4c67-11eb-8a89-561253339120.png)
![price_target](https://user-images.githubusercontent.com/42444599/103447301-0179c780-4c68-11eb-9053-77d1e086b915.png)
