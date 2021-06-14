# chat-django

Um chat simples em realtime usando django channels e django rest.

## 🗒 Dependências

- Python >= 3.6

## 🔧 Instalação

- Clone o projeto e crie um virtual env dentro dele ```python -m venv env```.
- Ative o virtualenv ```source env/bin/activate```.
- Instale as dependências ```pip install -r requirements.txt```.
- Crie o arquivo .env ```python contrib/generate_env.py```.
- Instale as migrações ```python manage.py migrate```.
- Crie um superuser ```python manage.py createsuperuser```.
- Rode o projeto ```honcho start```.
- Acesse o admin se quiser cadastrar algo.

## 🎨 Modelagem da aplicação

Este é um simples modelo de DER que exemplifica como a aplicação está feita, caso há essa necessidade de entendimento.

<p align="center">
  <img src="https://github.com/gabrielloliveira/chat-django/blob/master/gh-images/diagrama-core.png" alt="Diagrama DER da aplicação">
</p>

## 📱 Endpoints Importantes

- Listar todos os atendimentos -> ```GET /api/help-desks/```
- Visualisar histórico de 1 atendimento -> ```GET /api/help-desks/<uuid>/history/```
- Enviar Mensagem -> ```POST /api/send-message/```
    - body: ```message: text; help_desk: <uuid_help_desk>; file: BinaryField;```


## 🚀 Websocket

Esse projeto manda atualizacoes de mensagens do chat via websocket. Ele funciona da seguinte forma:

- Para o WS deste projeto, foi adotado um padrão de comunicação baseado em eventos. Para cada evento que é julgado
  importante na plataforma, é enviado uma payload via websocket, seguindo o padrão abaixo:
```json
{
  "type": "<tipo do evento emitido>",
  "data": "<Um JSON em formato de string>"
}
```
- Os tipos de eventos configurados para este projeto são esses 👇:
  - ```update_helpdesk``` (ocorre quando o atendimento foi atualizado)
  - ```new_message``` (quando uma nova mensagem é adicionada em alguma conversa/atendimento)
  - ```update_message``` (quando uma mensagem de alguma conversa é atualizada, como por exemplo, mudar o status da 
    mensagem de enviado para entregue)

- O que é retornado do parâmetro ```data``` do WS é o JSON que a API retorna, convertido para string. 
  - Ex.: O que é retornado no evento de update_help_desk é UM OBJETO desta rota ```GET /api/help-desks/```
  - Para eventos de mensagens, é retornado um objeto presente nesta rota ```GET /api/help-desks/<uuid>/history/```

