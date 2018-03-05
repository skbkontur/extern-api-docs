Api-key необходим для идентификации приложения при работе с API Контур.Экстерна.
Api-key представляет собой GUID.

Существует два способа передачи api-key на сервер.

### HTTP заголовок  

Заголовок X-Kontur-Apikey.

  GET /drive/documents?skip=10&take=10
  Host: api.kontur.ru
  Accept: application/json
  X-Kontur-Apikey: 7d4ea67f-90e8-48bb-b6de-59c4f4a6345a

### Query string   

Параметр с именем api-key.

GET /drive/documents?skip=10&take=10&api-key=7d4ea67f-90e8-48bb-b6de-59c4f4a6345a
Host: api.kontur.ru
Accept: application/json

### Примечания

- Если запросы к сервису идут из вне нашей серверной площадки, то необходимо передавать api-key в HTTP заголовке: X-Kontur-Apikey, чтобы не светить apikey.  

- Параметр query string обладает наиболее высоким приоритетом, затем идет HTTP заголовок X-Kontur-Apikey.
