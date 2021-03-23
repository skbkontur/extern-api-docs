.. _`POST tokenendpoint`: https://developer.testkontur.ru/doc/openidconnect/method?type=post&path=%2Fconnect%2Ftoken

.. _rst-markup-password:

Аутентификация по паролю
========================

Если пользователь уже использует веб версию Контур.Экстерна, то ему нужно настроить в личном кабинете вход по почте и паролю. Эти данные и нужно передавать в запросе в параметрах ``username`` и ``password``.

Если вам нужно протестировать аутентификацию, но у вас нет учетной записи в Экстерне, напишите нам *extern-api@skbkontur.ru*, мы выдадим вам тестовые данные. 

Метод `POST tokenendpoint`_

**Параметры тела запроса**

**Content-Type: application/x-www-form-urlencoded**

* ``client_id`` — сервисное имя, выдается вместе с api-key;
* ``client_secret`` — api-key;
* ``grant_type`` = password;
* ``scope`` = extern.api;
* ``username`` — логин пользователя;
* ``password`` — пароль пользователя.

**Ответ**

В ответ провайдер возвращает приложению Access Token.

**Пример запроса POST tokenendpoint с аутентификацией по паролю**

.. code-block:: http

    POST https://identity.testkontur.ru/connect/token

    Request Headers
    
    Accept: */*
    Host: identity.testkontur.ru
    Accept-Encoding: gzip, deflate, br
    Connection: keep-alive
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 183

    Request Body
    
    client_id:extern.api
    client_secret:************
    grant_type:password
    scope:extern.api
    username:user@login.ru
    password:password

**Пример ответа POST tokenendpoint**

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8
    Transfer-Encoding: chunked
    Connection: keep-alive
    Cache-Control: no-store, no-cache, max-age=0
    Pragma: no-cache
    X-Kontur-Trace-Id: 9da07e01570f4460bee6777e514d7af0
    Context-Globals: FgAAAHZvc3Rvay50cmFjaW5nLmNvbnRleHRJAAAAOWRhMDdlMDEtNTcwZi00NDYwLWJlZTYtNzc3ZTUxNGQ3YWYwOzljYzkwNmI0LTk2YmUtNGI2NC1iMDQ2LTJiNTJhMWViNGYwORcAAAB2b3N0b2sucmVxdWVzdC5wcmlvcml0eQgAAABPcmRpbmFyeQ==
    X-Kontur-Dont-Retry: True
    Dont-Retry: True
    Content-Encoding: gzip
    
    {
        "access_token":"fb957fedb8cf0a88b5cb25cf9b0570f82d332f202ca58653dfba7c035983b9e1",
        "expires_in":86400,
        "token_type":"Bearer"
    }
