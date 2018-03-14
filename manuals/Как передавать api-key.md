* Api-key необходим для идентификации приложения при работе с API Контур.Экстерна.  
* Api-key представляет собой GUID.  
* В запросах его необходимо передавать при помощи Http-заголовка  **X-Kontur-Apikey**.

Пример:
```
  GET /drive/documents?skip=10&take=10
  Host: api.kontur.ru
  Accept: application/json
  X-Kontur-Apikey: 7d4ea67f-90e8-48bb-b6de-59c4f4a6345a
```
