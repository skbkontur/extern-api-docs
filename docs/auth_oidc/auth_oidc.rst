.. _`Документация OpenID Connect`: https://developer.testkontur.ru/doc/openidconnect
.. _`OpenID Connect`: https://openid.net/specs/openid-connect-core-1_0.html
.. _`открытый`: https://identity.testkontur.ru/.well-known/openid-configuration/jwks
.. _`POST tokenendpoint`: https://developer.testkontur.ru/doc/openidconnect/method?type=post&path=%2Fconnect%2Ftoken

Получение и использование Access Token
======================================

Использование Access Token
--------------------------

Стандартный способ передачи Access Token в API Контур.Экстерна — через заголовок (Header parameters) в формате: 

::
    
    Authorization: Bearer <token>

Токен запрашивается через OpenID Connect Provider по адресам:

* Рабочая площадка: https://identity.kontur.ru
* Тестовая площадка: https://identity.testkontur.ru

`Документация OpenID Connect`_. Для удобства тестирования методов получения Access Token используйте файл коллекции Postman:

:download:`файл коллекции аутентификации Postman <../files/auth openid connect.postman_collection.json>`

Основные понятия
----------------

**OpenID Provider (Провайдер)** — аутентификационный сервер, который реализует протокол `OpenID Connect`_. Провайдер имеет `открытый`_ и закрытый ключи. Также Провайдер выдает токены, которыми оперирует OpenID Connect.

Для работы с Провайдером нужно иметь:

* **client_id** — сервисное имя, выдается вместе с :doc:`api-key</auth_oidc/api-key>`,
* **client_secret** — api-key.

**Access Token** — некоторый идентификатор, позволяет идентифицировать пользователя и выполнять действия от его имени в API.

    **Время жизни Access Token 24 часа**. Но токен может быть отозван в любой момент пользователем (например, если он сменил пароль) или Контуром. Истечение срока жизни токена не считается отзывом, он просто перестает действовать.

Получение Access Token
----------------------

Метод: `POST tokenendpoint`_

.. rubric:: Тело запроса:

**Content-Type: application/x-www-form-urlencoded**

* ``client_id`` — сервисное имя, выдается вместе с api-key;
* ``client_secret`` — api-key;
* ``grant_type`` — способ получения токена. Для аутентификации в API Контур.Экстерна используется только три типа: 

    * ``password`` — :ref:`аутентификация по паролю<rst-markup-password>`,
    * ``certificate`` — :ref:`аутентификация по сертификату<rst-markup-certificate>`,
    * ``trusted`` — :ref:`доверительная аутентификация<rst-markup-trusted>` только для Компаний-Партнеров Удостоверяющего Центра.

* ``scope`` — область действия токена. Для отправки запросов в API Контур.Экстерна нужно передать строку вида: ``extern.api``. Для отправки запросов в Extern Test Tools нужно передать в scope строку ``extern.test-tools``.

Следующие параметры запроса зависят от способа получения токена:

* ``username`` — логин пользователя, если grand_type = password,
* ``password`` — пароль пользователя, если grand_type = password,
* ``decrypted_key`` — расшифрованный ключ в кодировке base64, если grand_type = certificate,
* ``thumbprint`` — отпечаток сертификата пользователя, если grand_type = certificate,
* ``token`` — JWT токен с информацией о пользователе, если grand_type = trusted.