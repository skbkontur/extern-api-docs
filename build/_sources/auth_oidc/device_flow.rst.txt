.. _`страницу входа`: http://auth.kontur.ru/
.. _`документации OpenID Провайдер`: https://developer.kontur.ru/doc/html/schemes/device_flow.html
.. _`POST TokenEndpoint`: https://developer.kontur.ru/doc/openidconnect/method?type=post&path=%2Fconnect%2Ftoken

Аутентификация по веб-ссылке
============================

Для приложений без серверной части можно получить Access Token с помощью **device authorization flow**. Этот способ подходит для приложений, которые напрямую взаимодействуют с API Контур.Экстерна, например, для desktop-приложений, как модуль для 1С. 

Конечный пользователь использует свою учетную запись Контура для аутентификации. По кнопке "Войти" в приложении он переходит на `страницу входа`_, вводит данные своей учетной записи и выдает разрешение на доступ к выбранным данным. После возвращается в приложение. 

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

Метод: POST DeviceAuthorizationEndpoint.

.. note:: В документации Контур.API пока не реализован метод POST DeviceAuthorizationEndpoint. Рекомендуем использовать :download:`коллекцию Postman<../files/device flow.postman_collection.json>` для запросов. 

**Параметры тела запроса**

Content-Type: application/x-www-form-unlencoded

* ``client_id`` — сервисное имя, выдается вместе с api-key;
* ``client_secret`` — api-key;
* ``scope`` — область действия токена. Укажите значение: extern.api.

**Ответ**

В ответ OpenID Провайдер вернет временный код подтверждения ``device_code``, код проверки пользователя ``user_code`` и URL-ссылку на `страницу входа`_.

После получения device code приложение должно отправить конечного пользователя на аутентификацию по веб-ссылке и параллельно делать попытки обменять device code на Access Token. 

Количество попыток и время жизни токена вернутся в параметрах ``interval`` и ``expires_in``.

**Пример запроса**

.. code-block:: text

    POST /connect/deviceauthorization HTTP/1.1
    Host: identity.kontur.ru
    Content-type: application/x-www-form-urlencoded
    
    client_id=awesome_device_client
    client_secret=yourClientSecret
    scope=extern.api

**Пример ответа**

.. code-block:: text

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

1. Открыть в браузере ссылку из полученного параметра ``verification_uri_complete``.
2. Передать QR-код со ссылкой из полученного параметра ``verification_uri_complete``. Отсканировав этот код, пользователь перейдет на `страницу входа`_.

Конечный пользователь переходит на `страницу входа`_, вводит данные своей учетной записи и выдает разрешение на доступ к выбранным данным.

Подробнее о формировании ссылки смотрите в `документации OpenID Провайдер`_.

Получение Access Token
~~~~~~~~~~~~~~~~~~~~~~

Параллельно аутентификации по веб-ссылке необходимо регулярно пытаться получить Access Token.

Метод: `POST TokenEndpoint`_. 

**Параметры тела запроса**

Content-Type: application/x-www-form-unlencoded

* ``grant_type`` — тип аутентификации. Укажите значение: ``urn:ietf:params:oauth:grant-type:device_code``;
* ``client_id`` — сервисное имя, выдается вместе с api-key;
* ``client_secret`` — api-key;
* ``scope`` — область действия токена. Укажите значение: ``extern.api``;
* ``device_code`` — полученный код.

**Ответ**

В ответ OpenID Провайдер возвращает приложению Access Token.

**Пример запроса**

.. code-block:: text

    POST/connect/tokenHTTP/1.1
    Host: identity.kontur.ru
    Content-type: application/x-www-form-urlencoded
    
    grant_type=urn:ietf:params:oauth:grant-type:device_code
    client_id=awesome_device_client
    client_secret=yourClientSecret
    device_code=NGU5OWFiNjQ5YmQwNGY3YTdmZTEyNzQ3YzQ1YSA
    scope=extern.api

**Пример ответа**

.. code-block:: text

    HTTP/1.1 200 OK
    Content-Type: application/json
    Cache-Control: no-store
    {
        "access_token":"AYjcyMzY3ZDhiNmJkNTY",
        "id_token": "eyJhbGciOiJSU.CUpImw",
        "refresh_token":"RjY2NjM5NzA2OWJjuE7c",
        "token_type":"Bearer",
        "expires":3600,
        "scope":"extern.api"
    }