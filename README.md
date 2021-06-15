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

- Listar todos os atendimentos -> ```GET /api/help-desks/?organization=<organization_name>```
- Visualisar histórico de 1 atendimento -> ```GET /api/help-desks/<uuid>/history/```
- Enviar Mensagem -> ```POST /api/send-message/```
    - body: ```message: text; help_desk: <uuid_help_desk>; file: (Opcional) BinaryField;```

- Exemplo de um objeto do tipo HelpDesk retornado no JSON:
```json5
{
  "created_at": "2021-06-14T22:10:39.551836-03:00",
  "updated_at": "2021-06-14T22:10:39.551868-03:00",
  "uuid": "<um UUID aqui>",
  "client": {
    "uuid": "<UUID>",
    "created_at": "2021-06-14T22:04:20.149704-03:00",
    "updated_at": "2021-06-14T22:04:20.149734-03:00",
    "name": "Nome do Cliente",
    "phone": "123"
  },
  "last_message": {
    "created_at": "2021-06-15T11:43:03.573855-03:00",
    "updated_at": "2021-06-15T11:43:03.573908-03:00",
    "uuid": "<UUID>",
    "message": "Oi",
    "file": null,
    "type": "received",
    "help_desk": "<UUID>"
  }
}
```

- Exemplo de um objeto do tipo Message retornado no JSON:
```json5
{
    "created_at": "2021-06-15T11:57:16.420655-03:00",
    "updated_at": "2021-06-15T11:57:19.582823-03:00",
    "uuid": "<um UUID aqui>",
    "message": "teste",
    "file": null, // ou um caminho para um arquivo
    "type": "sent", // pode ser sent ou received
    "status": "sent", // pode ser sending ou sent
    "help_desk": "<um UUID aqui>"
  }
```

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

- Para se conectar ao WS, você deve colocar o link a seguir: ```ws://<dominio ou IP>/ws/chat/<organization_name>/```
- Se o domínio ou IP possuir o HTTPS, o protocolo deverá ser o ```wss://```

