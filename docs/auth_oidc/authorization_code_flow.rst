.. _`документации OpenID Провайдера`: https://developer.kontur.ru/Docs/html/schemes/code_flow.html
.. _`POST TokenEndpoint`: https://developer.kontur.ru/doc/openidconnect/method?type=post&path=%2Fconnect%2Ftoken
.. _`страницу входа`: http://auth.kontur.ru/

Аутентификация по коду подтверждения
====================================

Для приложений с серверной частью можно получить Access Token с помощью **authorization code flow**.

Конечный пользователь использует свою учетную запись Контура для аутентификации и выдает разрешение на доступ к выбранным данным. После получения разрешений, приложение отправляет запрос в API Контур.Экстерна.

Алгоритм аутентификации
-----------------------

Аутентификация выполняется в два этапа:

1. Получение authorization code.
2. Получение Access Token.

Получение authorization code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Для получения authorization code отправьте запрос. 

Метод: GET AuthorizationEndpoint.

.. note:: В документации Контур.API пока не реализован метод GET AuthorizationEndpoint. Рекомендуем использовать :download:`коллекцию Postman<../files/authorization code flow.postman_collection.json>` для запросов. 

**Параметры запроса**

Content-type: application/x-www-form-urlencoded

* ``response_type`` – ответ, который нужно получить от OpenID Провайдера. Укажите значение: ``code``;
* ``client_id`` – сервисное имя, выдается вместе с api-key;
* ``scope`` – область действия токена. Укажите следующие значения через пробел: ``openid extern.api``;
* ``redirect_uri`` – URL-адрес, на который будет перенаправлен конечный пользователь после аутентификации;
* ``nonce`` – строка для удостоверения, что запрос связан с будущим Access Token. Данная строка вернется при получении Access Token.

Все параметры имееют тип данных string.

**Ответ**

OpenID Провайдер сначала отправит конечного пользователя на `страницу входа`_, чтобы пользователь мог ввести данные своей учетной записи и выдать разрешения на доступ к данным. После OpenID Провайдер перенаправит пользователя на URL-адрес, указанный в параметре ``redirect_uri``, с временным кодом подтверждения ``code``.

Подробнее про получение authoriztion code смотрите в `документации OpenID Провайдера`_.

**Пример запроса**

.. code-block:: text

    GET /connect/authorize
        ?response_type=code
        &client_id={{client_id}}
        &scope=openid extern.api
        &redirect_uri=http://www.example.com/
        &nonce=n-0S6_WzA2Mj
        &state=af0ifjsldkj HTTP/1.1
    Host: identity.kontur.ru
    Content-type: application/x-www-form-urlencoded

**Пример ответа**

.. code-block:: text

    HTTP/1.1 302 Found
    Location: https://www.example.com
        ?code=SplxlOBeZQQYbYS6WxSbIA
        &state=af0ifjsldkj
        &scope=openid extern.api

Получение Access Token
~~~~~~~~~~~~~~~~~~~~~~

Полученный временный код подтверждения нужно обменять на Access Token.

Метод: `POST TokenEndpoint`_.

**Параметры запроса**

Content-type: application/x-www-form-urlencoded

* ``grant_type`` – тип аутентификации. Укажите значение: ``authorization_code``;
* ``code`` – временный код подтверждения;
* ``client_id`` – сервисное имя, выдается вместе с api-key;
* ``client_secret`` – api-key;
* ``redirect_uri`` – ссылка, на которую получен код подтверждения.

Все параметры имеют тип данных string.

**Ответ**

OpenID Провайдер вернет в ответ Access Token.

**Пример запроса**

.. code-block:: text

    POST /connect/token HTTP/1.1
    Host: identity.kontur.ru
    Content-Type: application/x-www-form-urlencoded

    grant_type=authorization_code
    code=SplxlOBeZQQYbYS6WxSbIA
    client_id={{client_id}}
    client_secret={{client_secret}}
    redirect_uri=http://www.example.com

**Пример ответа**

.. code-block:: text

    200 OK
    Content-type: application/json
    
    {
        "access_token": "AAAAAAAAAAAAAAAAA",
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": "eyJhbGciOifQ.ewogI3pAKfQ.ggW8hq-rvKMzqg"
    }
