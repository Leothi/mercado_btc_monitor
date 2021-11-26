uvicorn --factory --host 0.0.0.0 --port=8081 --reload --no-access-log api.app:get_app
# --no-access-log desabilita o logging padrão do uvicorn para requests - Função própria definida no utils