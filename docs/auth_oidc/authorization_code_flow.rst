.. _`документации OpenID Провайдера`: https://developer.kontur.ru/Docs/html/schemes/auth_and_authorize.html#rst-murkup-authorize-by-code
.. _`POST TokenEndpoint`: https://developer.testkontur.ru/doc/openidconnect/method?type=post&path=%2Fconnect%2Ftoken
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

**Content-type: application/x-www-form-urlencoded**

* ``response_type`` – ответ, который нужно получить от OpenID Провайдера. Укажите значение: ``code``;
* ``client_id`` – сервисное имя, выдается вместе с api-key;
* ``scope`` – область действия токена. Укажите следующие значения через пробел: ``openid extern.api``;
* ``redirect_uri`` – ссылка, на которую будет перенаправлен конечный пользователь после аутентификации;
* ``nonce`` – строка для удостоверения, что запрос связан с будущим Access Token. Данная строка вернется при получении Access Token.

**Ответ**

OpenID Провайдер перенаправит пользователя на адрес, указанный в параметре ``redirect_uri``, с кодом подтверждения code.

Подробнее про получение authoriztion code смотрите в `документации OpenID Провайдера`_.

**Пример запроса**

.. code-block:: http

    http://identity.testkontur.ru/connect/authorize?
    response_type=code
    &scope=openid extern.api
    &client_id=yourClientId
    &redirect_uri=http://www.example.com/
    &state=af0ifjsldkj
    &nonce=n-0S6_WzA2Mj

Получение Access Token
~~~~~~~~~~~~~~~~~~~~~~

Полученный код подтверждения нужно обменять на Access Token.

Метод: `POST TokenEndpoint`_.

**Параметры запроса**

Content-type: application/x-www-form-urlencoded

* ``grant_type`` – тип аутентификации. Укажите значение: ``authorization_code``;
* ``code`` – код подтверждения;
* ``client_id`` – сервисное имя, выдается вместе с api-key;
* ``client_secret`` – api-key;
* ``riderect_uri`` – ссылка, на которую получен код подтверждения.

**Ответ**

OpenID Провайдер вернет в ответ Access Token.

**Пример запроса**

.. code-block:: http

    POST /token
    Content-type: application/x-www-form-urlencoded
    
    grant_type=authorization_code
    code=SplxlOBeZQQYbYS6WxSbIA
    client_id=yourClientId
    client_secret=yourClientSecret
    redirect_uri=http://www.example.com

**Пример ответа**

.. code-block:: http

    200 OK
    Content-type: application/json
    
    {
        "access_token": "AAAAAAAAAAAAAAAAA",
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": "eyJhbGciOifQ.ewogI3pAKfQ.ggW8hq-rvKMzqg"
    }
