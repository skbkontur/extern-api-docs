.. _`auth.kontur.ru`: http://auth.kontur.ru/
.. _`документации OpenID Провайдер`: https://developer.testkontur.ru/doc/openidconnect?about=8
.. _`POST TokenEndpoint`: https://developer.testkontur.ru/doc/openidconnect/method?type=post&path=%2Fconnect%2Ftoken

Аутентификация по веб-ссылке
============================

Для приложений без серверной части можно получить Access Token с помощью **device flow**. Этот способ также подходит для приложений, которые напрямую взаимодействуют с API Контур.Экстерна, например, для модуля 1С. 

Конечный пользователь использует свою учетную запись Контура для аутентификации. По кнопке "Войти" в приложении он переходит на страницу `auth.kontur.ru`_ и выдает разрешение на доступ к выбранным данным. После возвращается в приложение. 

Алгоритм аутентификации
-----------------------

Аутентификация выполняется в три этапа:

1. Получение device code.
2. Аутентификация по веб-ссылке.
3. Получение Access Token.

Второй и третий этапы проходят параллельно. 

Получение device code
~~~~~~~~~~~~~~~~~~~~~

Для получения device code необходимо отправить запрос.

Метод: POST DeviceAuthorization.

.. note:: В документации Контур.API пока не реализован метод POST DeviceAuthorization. Рекомендуем использовать :download:`коллекцию Postman<../files/device flow.postman_collection.json>` для запросов. 

**Параметры тела запроса**

**Content-Type: application/x-www-form-unlencoded**

* ``client_id`` – сервисное имя, выдается вместе с api-key;
* ``client_secret`` – api-key;
* ``scope`` – область действия токена. Укажите значение: extern.api.

**Ответ**

В ответ OpenID Провайдер вернет ``device code`` и ссылку на веб-страницу `auth.kontur.ru`_.

После получения device code приложение должно отправить пользователя на аутентификацию по веб-ссылке и параллельно делать попытки обменять device code на Access Token. 

Количество попыток и время жизни токена вернутся в параметрах ``interval`` и ``expires_in``.

**Пример запроса**

.. code-block:: http

    POST /connect/deviceauthorization HTTP/1.1
    Host: identity.kontur.ru
    Content-type: application/x-www-form-urlencoded
    
    client_id=awesome_device_client
    client_secret=yourClientSecret
    scopes=extern.api

**Пример ответа**

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json
    Cache-Control: no-store
    {
        "device_code":"NGU5OWFiNjQ5YmQwNGY3YTdmZTEyNzQ3YzQ1YSA",
        "user_code": "BDWPHQPK",
        "verification_uri": "<https://identity.testkontur.ru/device>",
        "verification_uri_complete": "<https://identity.testkontur.ru/device?user-code=BDWPHQPK>",
        "interval": 3,
        "expires_in": 300
    }
Аутентификация по веб-ссылке
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Передать ссылку конечному пользователю можно двумя способами:

1. Открыть в браузере ссылку из возвращенного параметра ``verification_uri_complete``.
2. Передать QR-код со ссылкой из возвращенного параметра ``verification_uri_complete``.

Подробнее о формировании ссылки смотрите в `документации OpenID Провайдер`_.

Получение Access Token
~~~~~~~~~~~~~~~~~~~~~~

Параллельно аутентификации по веб-ссылке необходимо регулярно пытаться получить Access Token.

Метод: `POST TokenEndpoint`_. 

**Параметры тела запроса**

**Content-Type: application/x-www-form-unlencoded**

* ``grant_type`` – тип аутентификации. Укажите значение: ``urn:ietf:params:oauth:grant-type:device_code``;
* ``client_id`` – сервисное имя, выдается вместе с api-key;
* ``client_secret`` – api-key;
* ``scope`` – область действия токена. Укажите значение: ``extern.api``;
* ``device-code`` – полученный код.

**Ответ**

В ответ OpenID Провайдер возвращает приложению Access Token.

**Пример запроса**

.. code-block:: http

    POST /connect/tokenHTTP/1.1
    Host: identity.kontur.ru
    Content-type: application/x-www-form-urlencoded
    
    grant_type=urn:ietf:params:oauth:grant-type:device_code
    client_id=awesome_device_client
    client_secret=yourClientSecret
    device_code=NGU5OWFiNjQ5YmQwNGY3YTdmZTEyNzQ3YzQ1YSA
    scope=extern.api

**Пример ответа**

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json
    Cache-Control: no-store
    {
        "access_token":"AYjcyMzY3ZDhiNmJkNTY",
        "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjExNjVlMDVlMDgwMDllOTE1MjI3MDY0NzlmOTcwMGJkIiwidHlwIjoiSldUIn0.eyJuYmYiOjE2NTQwMTg1NDIsImV4cCI6MTY1NDAxODg0MiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS50ZXN0a29udHVyLnJ1IiwiYXVkIjoib2lkYy5kZXZpY2VmbG93LmV4YW1wbGUiLCJpYXQiOjE2NTQwMTg1NDIsImF0X2hhc2giOiJKblNIQkVZNFM4YUpOdTIxUkJ2SkxnIiwic3ViIjoiZDZmMzgwMzQtNzJhNy00YjczLTkyNDQtNjU5NWEzNzZkNjMwIiwiYXV0aF90aW1lIjoxNjUzNDYzOTk2LCJpZHAiOiJwb3J0YWwiLCJnaXZlbl9uYW1lIjoi0JTQtdC90LjRgSIsImZhbWlseV9uYW1lIjoi0KHQv9C40YDQuNC00L7QvdC-0LIiLCJtaWRkbGVfbmFtZSI6ItCS0LvQsNC00LjQvNC40YDQvtCy0LjRhyIsIm5hbWUiOiLQodC_0LjRgNC40LTQvtC90L7QsiDQlNC10L3QuNGBINCS0LvQsNC00LjQvNC40YDQvtCy0LjRhyIsImVtYWlsIjoic3Bpcmlkb25vdi5kdkBza2Jrb250dXIucnUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwidXBkYXRlZF9hdCI6MTY1MjkzODYwNiwicGljdHVyZSI6Imh0dHBzOi8vYXBpLnRlc3Rrb250dXIucnUvY2FiaW5ldC92Mi4wL3VzZXJzL2Q2ZjM4MDM0LTcyYTctNGI3My05MjQ0LTY1OTVhMzc2ZDYzMC9hdmF0YXJzL2N1cnJlbnQ_c2l6ZT1MYXJnZSIsImFtciI6WyJwd2QiLCJtZmEiLCJvdHAiXX0.jnMSCN8MridBYNSJfHUQCOEoBgMvdZek_4dsagAAJGiO0D7Cw2F6-37rJgj-4O1fPTItdTy7JekT4iC8GMx0npnsSaR0HvgIAS_O_Og87Lb8LgynzwYPRSiTFSh9XFj10bZ2N8fkD9gtevgkV_BlAVKlTfOqWVwyL32U2PdpfsM5Wh02QwOqkvFGEowwD2P4EavanBGrjMYY1Dm1F_KHKXnypgaTZd3QkCJTpOBO4dwH_d84K6QaHIl5q7MPiyGZGfwluOnIPWPGdWOoWnDTZqaslt86pJETgaIgSCYrEtGyQGCmUXMCv1OHDoBTElKDUnzMg8DuVOzjmEI7CUpImw",
        "refresh_token":"RjY2NjM5NzA2OWJjuE7c",
        "token_type":"Bearer",
        "expires":3600,
        "scope":"extern.api"
    }