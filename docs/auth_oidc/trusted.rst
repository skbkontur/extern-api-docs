.. _`POST tokenendpoint`: https://developer.testkontur.ru/doc/openidconnect/method?type=post&path=%2Fconnect%2Ftoken
.. _`PUT register-external-service-id`: https://developer.kontur.ru/doc/auth/method?type=put&path=%2Fauth%2Fv5.16%2Fregister-external-service-id
.. _`RSA`: https://ru.wikipedia.org/wiki/RSA
.. _`документации OpenID Connect`: https://developer.testkontur.ru/doc/openidconnect
.. _`jwt.io`: https://jwt.io/

.. _rst-markup-trusted:

Доверительная аутентификация
=============================

.. warning:: Данный вид аутентификации доступен только для **Компаний-Партнеров Удостоверяющего Центра**.

Компания-Партнер Удостоверяющего Центра
  Это организация, которая имеет у себя аккредитованное рабочее место Удостоверяющего центра. Она самостоятельно может удостоверить личность пользователя, проверить документы и создать запрос на сертификат.

* Доверительная аутентификация позволяет получить Access Token, используя аутентификацию пользователя в доверенной системе Компании-Партнера. 
* Доверительная аутентификация выполняется в один запрос. Для этого доверенная система формирует JWT токен и передает его Провайдеру.
  
Для того, чтобы воспользоваться доверительной аутентификацией, необходимо при **первом** входе пользователя произвести связывание пользователей в системе Партнера и в Экстерне. 

Связывание пользователей
------------------------

Для доверительной аутентификации пользователя необходимо, чтобы пользователь Экстерна был связан с пользователем доверенной системы партнера. Связь может происходить следующим образом:

* вручную техподдержкой на стороне Экстерна по запросу Компании-Партнера,
* доверенной системе разрешается самостоятельно связывать определенных пользователей Экстерна с любым своим пользователем по номеру телефона. Для этого требуется отдельное разрешение, которое нужно получить Компании-Партнеру.

Метод связывания пользователей (при наличии разрешения): `PUT register-external-service-id`_

**Параметры запроса**:

* ``ServiceUserId`` — идентификатор пользователя в доверенной системе.
* ``Phone`` — телефон пользователя в формате '10 цифр без кода страны', который был указан при выпуске сертификата пользователя. 

Получение Access Token
----------------------

Для получения Access Token в запросе `POST tokenendpoint`_ нужно предать в теле запроса в параметре ``token`` JWT токен с информацией о пользователе.

Метод: `POST tokenendpoint`_

**Параметры тела запроса:**

**Content-Type: application/x-www-form-urlencoded**

* ``client_id`` — сервисное имя, выдается вместе с api-key;
* ``client_secret`` — api-key;
* ``grant_type`` = trusted;
* ``scope`` = extern.api;
* ``token`` — JWT токен с информации о пользователе. JWT токен доверенная система должна сформировать на своей стороне. Подробнее в `документации OpenID Connect`_ → Доверительная аутентификация.

Требования к JWT токену:

    * Токен можно использовать только 1 раз.
    * Общее время жизни токена не должно превышать 24 часов.
    * Размер значения клейма jti (идентификатор токена) не должен превышать 36 байт.
    * Издатель токена (iss) должен совпадать с clientId сервиса, инициирующего запрос.
    * Обязательные клеймы, которые должны присутствовать в токене:

        * exp - время истечения токена в unix time stamp. 
        * sub - идентификатор пользователя во внешней системе. 
        * jti - уникальный идентификатор токена.
        * iss - издатель токена, т.е. сервис, желающий получить аутентификацию пользователя.

Токен должен быть подписан ключом (или сертификатом) доверенной системы. Допускается использование криптографии `RSA`_. Сертификат и ключ для данного алгоритма криптографии можно получить, например, в ОС Windows :doc:`с использованием OpenSSL</manuals/using-OpenSSL-and-RSA>`.

В JWT токене обязательно в клейме ``sub`` передавать тот идентификатор, который указывали при связывании пользователей в параметре ``ServiceUserId``. 

.. container:: toggle

    .. container:: header

        Пример генерации JWT с использованием библиотеки `jwt.io`_ и RSA сертификата.

    .. code-block:: c#

        {
            X509Certificate2 certificate;
        
            certificate = new X509Certificate2(@"C:\PathToCertificate\certificate.pfx", "123");
            var internalUserId = "0a9b268a-063b-4e3a-8ad3-4a9a61a2303b"; //любой идентификатор, который был передан для связывания пользователей
            var internalTokenId = Guid.NewGuid().ToString();
        
            // NuGet-пакет System.IdentityModel.Tokens.Jwt
        
            var claims = new ClaimsIdentity(new[]
            {
                new Claim("sub", internalUserId), // идентификатор пользователя в доверенной системе
                new Claim("jti", internalTokenId) // идентификатор токена в доверенной системе. должен меняться при каждом запросе, произвольная строка
            });
        
            var tokenDescriptor = new SecurityTokenDescriptor
            {
                Subject = claims,
                Issuer = clientId, // имя доверенной системы == сервисное имя, выданное вместе с api-key
                Expires = DateTime.UtcNow.AddMinutes(5), // время прекращения действия токена
                SigningCredentials = new X509SigningCredentials(certificate) // сертификат
            };
        
            var tokenHandler = new JwtSecurityTokenHandler();
            var token = tokenHandler.CreateToken(tokenDescriptor);
            jwtTokenString = tokenHandler.WriteToken(token); // преобразование в формат header.payload.sign
        
            var jwt = new JwtSecurityToken(jwtTokenString);
            var v = jwt.ToString();
        }


Пример доверительной аутентификации
-----------------------------------

**Пример запроса POST tokenendpoint с доверительной аутентификацией**

.. code-block:: http

    POST https://identity.testkontur.ru/connect/token

    Request Headers

    Accept: */*
    Host: identity.testkontur.ru
    Accept-Encoding: gzip, deflate, br
    Connection: keep-alive
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 860
    
    Request Body

    client_id:extern.api
    client_secret:*****
    grant_type:trusted
    scope:extern.api
    token:eyJhbGciOiJSUzI1NiIsImtpZCI6IjA2RDkwRTg3RTUzREE5QkQzNjIxQjRFQkZGQUY1REFCNkI2NTBDRTMiLCJ4NXQiOiJCdGtPaC1VOXFiMDJJYlRyXzY5ZHEydGxET00iLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiIwYTliMjY4YS0wNjNiLTRlM2EtOGFkMy00YTlhNjFhMjMwM2IiLCJqdGkiOiIxMmVkMWU1NC0xYjIzLTQzODctODJlNS0xZDEzYmNhNGQ4NjYiLCJuYmYiOjE2MDA3NzcxMzMsImV4cCI6MTYwMDc3NzQzMywiaWF0IjoxNjAwNzc3MTMzLCJpc3MiOiJLZUFwaS5UcnVzdGVkLlNlcnZpY2UifQ.UO4-9OzWj14WTjct1E2_SpB7pfaAdPlTu9r_ocNt9bgfeyMxZuFcfWeWTJd5PpdDQA1vXV1EccMO14Qojry0KawJrZVRC2sXZPwrmF0j0v7vK1prnlabaYBsSeO-1vY0EaboIC3Zr5Igw_4xK8R22e4ysY6TS7gBaSQpGF1yjRCB3I6OWPCSWcj81g8GWTiqkuxAgmkMBO6loHrNqdAeG8b-cMt5ycdA9PeFEjeeMZ3F2-A-CWw92OgfqVKgokrfotjnvpdIVZfQC6mCxvYuI4zhEGO_Qz9s_RgbZHifuKmUc89aZROHmEuzh3PHYP25PQ-2-3NzNLyBfF7b6ZJgXg
    
**Пример ответа POST tokenendpoint**

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8
    Transfer-Encoding: chunked
    Connection: keep-alive
    Cache-Control: no-store, no-cache, max-age=0
    Pragma: no-cache
    X-Kontur-Trace-Id: 5ea7d9c5570c41cb966c9f7af263b2a8
    Context-Globals: FwAAAHZvc3Rvay5yZXF1ZXN0LnByaW9yaXR5CAAAAE9yZGluYXJ5FgAAAHZvc3Rvay50cmFjaW5nLmNvbnRleHRJAAAANWVhN2Q5YzUtNTcwYy00MWNiLTk2NmMtOWY3YWYyNjNiMmE4OzJhN2ZjMWRiLTdjNzQtNGVmMy1hMzg2LTJiYWVhNmQ5MWUyOA==
    X-Kontur-Dont-Retry: True
    Dont-Retry: True
        
    Response Body
        
    Content-Encoding: gzip
    {
        "access_token":"a126187d9c71984e2b979ab7008cb16f124d97bbe9c256f7081dec3eedc2601f",
        "expires_in":86400,
        "token_type":"Bearer"
    }