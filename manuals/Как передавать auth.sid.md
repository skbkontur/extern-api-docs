Есть три способа передачи auth.sid на сервер. Рекомендуется поддерживать все способы.

### Query string  

Параметр auth.sid  

  GET /drive/documents?skip=10&take=10&auth.sid=FE6CFF8BE5E5B548AB1971874886D5C30E85D9BFA41978478FD26D5FD6B66D81
  Host: api.kontur.ru
  Accept: application/json


### HTTP заголовок Authorization  

Схема auth.sid  

  GET /drive/documents?skip=10&take=10
  Host: api.kontur.ru
  Accept: application/json
  Authorization: auth.sid FE6CFF8BE5E5B548AB1971874886D5C30E85D9BFA41978478FD26D5FD6B66D81  

## Cookie

Параметр auth.sid  

  GET /drive/documents?skip=10&take=10
  Host: api.kontur.ru
  Accept: application/json
  Cookie: auth.sid=FE6CFF8BE5E5B548AB1971874886D5C30E85D9BFA41978478FD26D5FD6B66D81

### Примечания

- По приоритетам способы рекомендуется оценивать так:
-- Самый высокий приоритет у Query string, затем Authorization, затем Cookie.  

- Параметры auth.sid следует считать регистронезависимыми в каждом из трех способов.
