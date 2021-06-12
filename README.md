# chat-django

Um chat simples em realtime usando django channels e django rest.

## Dependências

- Python >= 3.6

## Instalação

- Clone o projeto e crie um virtual env dentro dele ```python -m venv env```.
- Ative o virtualenv ```source env/bin/activate```.
- Instale as dependências ```pip install -r requirements.txt```.
- Crie o arquivo .env ```python contrib/generate_env.py```.
- Instale as migrações ```python manage.py migrate```.
- Crie um superuser ```python manage.py createsuperuser```.
- Rode o projeto ```honcho start```.
- Acesse o admin se quiser cadastrar algo.

## Endpoints Importantes

- Listar todos os atendimentos -> ```GET /api/help-desks/```
- Visualisar histórico de 1 atendimento -> ```GET /api/help-desks/<uuid>/history/```
- Enviar Mensagem -> ```POST /api/send-message/```
    - body: ```message: text; help_desk: <uuid_help_desk>; file: BinaryField;```