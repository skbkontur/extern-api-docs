.. _`POST tokenendpoint`: https://developer.testkontur.ru/doc/openidconnect/method?type=post&path=%2Fconnect%2Ftoken
.. _`POST Certificate`: https://developer.testkontur.ru/doc/openidconnect/method?type=post&path=%2Fauthentication%2Fcertificate

.. _rst-markup-certificate:

Аутентификация по сертификату
=============================

.. important:: Аутентификация по сертификату двухшаговая.

1. Инициализация
----------------

* Пользователь присылает объект идентификации — открытый ключ сертификата (*public_key*). 
* Для переданного client_id генерируется случайное значение — *rnd*. Сервер шифрует *rnd* (получаем *enc(rnd)*) на сертификат пользователя и отправляет его в ответе.

Метод: `POST Certificate`_

**Параметры тела запроса:**

**Content-Type: application/x-www-form-urlencoded**

* ``client_id`` — сервисное имя, выдается вместе с api-key;
* ``client_secret`` — api-key;
* ``public_key`` — сертификат в PEM-формате;
* ``free`` — булевый флаг проверки валидности сертификата (true — не проверять сертификат на валидность, по умолчанию — false).

**Ответ**:

* ``encrypted_key`` — случайная зашифрованная строка. Возвращается в кодировке base64.

2. Подтверждение
----------------

В encrypted_key лежат данные в формате base64, их нужно декодировать. Полученный результат нужно дешифровать с помощью сертификата (получаем *dec(enc(rnd))*).

Расшифрованный результат *dec(enc(rnd))* отправляется в OpenId Provider в формате base64 (параметр ``decrypted_key``) вместе с отпечатком сертификата (параметр ``thumbprint``). 

Метод: `POST tokenendpoint`_

**Параметры тела запроса:**

**Content-Type: application/x-www-form-urlencoded**

* ``client_id`` — сервисное имя, выдается вместе с api-key;
* ``client_secret`` — api-key;
* ``grant_type`` = certificate;
* ``scope`` = extern.api;
* ``decrypted_key`` — расшифрованный ключ в кодировке base64;
* ``thumbprint`` — отпечаток сертификата пользователя.

**Ответ**:

В ответ провайдер возвращает приложению Access Token.

Пример аутентификации по сертификату
------------------------------------

**1. Инициализация. Пример запроса POST certificate**

.. code-block:: http

    POST https://identity.testkontur.ru/authentication/certificate
    
    Request Headers
    
    Accept: */*
    Host: identity.testkontur.ru
    Accept-Encoding: gzip, deflate, br
    Connection: keep-alive
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 3444
    
    Request Body
    
    client_id:extern.api
    client_secret:*********
    public_key:MIIJnzCCCUyg...81jlw7m/+g==
    free:true

**Пример ответа POST certificate**

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8
    Transfer-Encoding: chunked
    Connection: keep-alive
    X-Kontur-Trace-Id: 27bb7faa48294cf49ae6007d70905468
    Context-Globals: FwAAAHZvc3Rvay5yZXF1ZXN0LnByaW9yaXR5CAAAAE9yZGluYXJ5FgAAAHZvc3Rvay50cmFjaW5nLmNvbnRleHRJAAAAMjdiYjdmYWEtNDgyOS00Y2Y0LTlhZTYtMDA3ZDcwOTA1NDY4OzBiY2QwOThhLTU5MjYtNDJlNC05NjAzLTJiMTM2MDdlODk5ZQ==
    X-Kontur-Dont-Retry: True
    Dont-Retry: True
    Content-Encoding: gzip
    
    Response Body
    
    {
        "encrypted_key":"MIIDo2QE...Q4X4OA==",
        "trusted_thumbprints":null
    }

**2. Подтверждение. Пример запроса POST tokenendpoint с аутентификацией по сертификату**

.. code-block:: http

    POST https://identity.testkontur.ru/connect/token
    
    Request Headers
    
    Accept: */*
    Host: identity.testkontur.ru
    Accept-Encoding: gzip, deflate, br
    Connection: keep-alive
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 574
    
    Request Body
    
    client_id:extern.api
    client_secret:******
    grant_type:certificate
    scope:extern.api
    decrypted_key:gs1mx/rvAD6MSOpe...DBbvLuC9NWMKeE85rYsGXQ==
    thumbprint:517a26be6b0e2b84d8eb95614ececb121c441c89

**Пример ответа POST tokenendpoint**

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8
    Transfer-Encoding: chunked
    Connection: keep-alive
    Cache-Control: no-store, no-cache, max-age=0
    Pragma: no-cache
    X-Kontur-Trace-Id: aef5da881a7c43a5913f6ccfe5a9af29
    Context-Globals: FgAAAHZvc3Rvay50cmFjaW5nLmNvbnRleHRJAAAAYWVmNWRhODgtMWE3Yy00M2E1LTkxM2YtNmNjZmU1YTlhZjI5O2JhZjU5MzAzLWNjZjItNDBmYi04NjYwLWI3YWUzZjRkMzQ0ORcAAAB2b3N0b2sucmVxdWVzdC5wcmlvcml0eQgAAABPcmRpbmFyeQ==
    X-Kontur-Dont-Retry: True
    Dont-Retry: True
    Content-Encoding: gzip
    
    Response Body
    
    {
        "access_token":"340edee15505ef619f22f5963306d87ffc9b7d920c12b6aa8d9b67cbdce5688d",
        "expires_in":86400,
        "token_type":"Bearer"
    }
